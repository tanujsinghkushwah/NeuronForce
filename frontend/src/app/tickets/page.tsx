"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/Header";
import { api } from "@/lib/api";
import {
  Ticket,
  TicketStats,
  TicketPriority,
  TicketStatus,
  TicketCategory,
} from "@/types/crm";
import {
  LifeBuoy,
  Plus,
  AlertTriangle,
  Clock,
  CheckCircle2,
  Filter,
  Search,
  MessageSquare,
  Sparkles,
  UserCheck,
  Send,
  ShieldAlert,
  ChevronRight,
  RefreshCw,
  Tag,
  ArrowUpRight,
  SlidersHorizontal,
  Flame,
  Check,
} from "lucide-react";

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [stats, setStats] = useState<TicketStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState(() => {
    if (typeof window !== "undefined") {
      return new URLSearchParams(window.location.search).get("search") || "";
    }
    return "";
  });
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

  // New Ticket Modal
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newPriority, setNewPriority] = useState<TicketPriority>("medium");
  const [newCategory, setNewCategory] = useState<TicketCategory>("general");
  const [newReporterName, setNewReporterName] = useState("");
  const [newReporterEmail, setNewReporterEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Message reply in drawer
  const [replyText, setReplyText] = useState("");
  const [isInternalNote, setIsInternalNote] = useState(false);
  const [sendingReply, setSendingReply] = useState(false);
  const [triagingAI, setTriagingAI] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [ticketsData, statsData] = await Promise.all([
        api.getTickets(),
        api.getTicketStats().catch(() => null),
      ]);
      setTickets(ticketsData);
      if (statsData) setStats(statsData);
      if (selectedTicket) {
        const refreshed = ticketsData.find((t) => t.id === selectedTicket.id);
        if (refreshed) setSelectedTicket(refreshed);
      }
    } catch (err) {
      console.error("Failed to load tickets:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    try {
      setSubmitting(true);
      const created = await api.createTicket({
        title: newTitle,
        description: newDesc,
        priority: newPriority,
        category: newCategory,
        reporter_name: newReporterName || "Internal User",
        reporter_email: newReporterEmail || "support@neuronforce.ai",
        ai_triage: true,
      });
      setIsCreateOpen(false);
      setNewTitle("");
      setNewDesc("");
      await loadData();
      setSelectedTicket(created);
    } catch (err) {
      console.error("Failed to create ticket:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleSendReply = async () => {
    if (!selectedTicket || !replyText.trim()) return;
    try {
      setSendingReply(true);
      await api.addTicketMessage(selectedTicket.id, {
        body: replyText,
        author_name: "Alex Rivera (RevOps Lead)",
        author_email: "alex.rivera@neuronforce.ai",
        is_internal: isInternalNote,
      });
      setReplyText("");
      const updated = await api.getTicket(selectedTicket.id);
      setSelectedTicket(updated);
      setTickets((prev) =>
        prev.map((t) => (t.id === updated.id ? updated : t)),
      );
    } catch (err) {
      console.error("Failed to send reply:", err);
    } finally {
      setSendingReply(false);
    }
  };

  const handleUpdateStatus = async (status: TicketStatus) => {
    if (!selectedTicket) return;
    try {
      const updated = await api.updateTicket(selectedTicket.id, { status });
      setSelectedTicket(updated);
      setTickets((prev) =>
        prev.map((t) => (t.id === updated.id ? updated : t)),
      );
      loadData();
    } catch (err) {
      console.error("Failed to update status:", err);
    }
  };

  const handleRunAITriage = async () => {
    if (!selectedTicket) return;
    try {
      setTriagingAI(true);
      const res = await api.runTicketAITriage(selectedTicket.id);
      const updated = await api.getTicket(selectedTicket.id);
      setSelectedTicket(updated);
      setTickets((prev) =>
        prev.map((t) => (t.id === updated.id ? updated : t)),
      );
    } catch (err) {
      console.error("AI triage failed:", err);
    } finally {
      setTriagingAI(false);
    }
  };

  const filteredTickets = tickets.filter((t) => {
    const matchesSearch =
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.ticket_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (t.reporter_name &&
        t.reporter_name.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesStatus = statusFilter === "all" || t.status === statusFilter;
    const matchesPriority =
      priorityFilter === "all" || t.priority === priorityFilter;
    return matchesSearch && matchesStatus && matchesPriority;
  });

  const getPriorityBadge = (p: TicketPriority) => {
    switch (p) {
      case "critical":
        return "bg-red-500/15 text-red-400 border border-red-500/30";
      case "high":
        return "bg-amber-500/15 text-amber-400 border border-amber-500/30";
      case "medium":
        return "bg-indigo-500/15 text-indigo-400 border border-indigo-500/30";
      default:
        return "bg-slate-500/15 text-slate-400 border border-slate-500/30";
    }
  };

  const getStatusBadge = (s: TicketStatus) => {
    switch (s) {
      case "open":
        return "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30";
      case "in_progress":
        return "bg-cyan-500/15 text-cyan-400 border border-cyan-500/30";
      case "resolved":
        return "bg-blue-500/15 text-blue-400 border border-blue-500/30";
      case "closed":
        return "bg-slate-500/15 text-slate-400 border border-slate-500/30";
      default:
        return "bg-purple-500/15 text-purple-400 border border-purple-500/30";
    }
  };

  return (
    <div className="flex-1 flex flex-col min-h-screen overflow-x-hidden">
      <Header />

      <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
        {/* Page Top Banner */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-2 border-b border-white/10">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <LifeBuoy className="w-5 h-5" />
              </span>
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Service Cloud{" "}
                <span className="text-indigo-400 font-normal">
                  / Cases & SLAs
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Autonomous customer service case management, real-time SLA breach
              timers, and Gemini-powered triage.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={loadData}
              disabled={loading}
              className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition-all border border-white/10"
              title="Refresh tickets"
            >
              <RefreshCw
                className={`w-4 h-4 ${loading ? "animate-spin" : ""}`}
              />
            </button>

            <button
              onClick={() => setIsCreateOpen(true)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/30"
            >
              <Plus className="w-4 h-4" />
              <span>New Support Case</span>
            </button>
          </div>
        </div>

        {/* Top KPI Metrics Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Total Active Cases</span>
              <LifeBuoy className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="text-2xl font-bold text-white mt-2">
              {stats?.total ?? tickets.length}
            </div>
            <div className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
              <span>{stats?.open ?? 0} open</span> •{" "}
              <span>{stats?.in_progress ?? 0} in progress</span>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Critical Incidents</span>
              <Flame className="w-4 h-4 text-red-400 animate-pulse" />
            </div>
            <div className="text-2xl font-bold text-red-400 mt-2">
              {stats?.critical ??
                tickets.filter((t) => t.priority === "critical").length}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              1-hour SLA target
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>SLA Breached / At Risk</span>
              <Clock className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-bold text-amber-400 mt-2">
              {stats?.sla_breached ??
                tickets.filter((t) => t.sla_breached).length}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              Requires immediate action
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Resolution Rate</span>
              <CheckCircle2 className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-2xl font-bold text-cyan-400 mt-2">
              {stats?.resolution_rate ?? 0}%
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              {stats?.resolved ?? 0} cases resolved
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="p-3 rounded-2xl bg-white/[0.02] border border-white/10 flex flex-col md:flex-row items-center justify-between gap-3">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by title, TKT-ID, or reporter..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-white/5 border border-white/10 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 transition-all"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto overflow-x-auto pb-1 md:pb-0">
            {/* Status pills */}
            {(["all", "open", "in_progress", "resolved"] as const).map((s) => (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium capitalize transition-all whitespace-nowrap ${
                  statusFilter === s
                    ? "bg-indigo-600 text-white"
                    : "bg-white/5 text-slate-400 hover:text-white hover:bg-white/10"
                }`}
              >
                {s.replace("_", " ")}
              </button>
            ))}

            <div className="h-4 w-px bg-white/10 mx-1 hidden md:block" />

            {/* Priority pills */}
            {(["all", "critical", "high", "medium", "low"] as const).map(
              (p) => (
                <button
                  key={p}
                  onClick={() => setPriorityFilter(p)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium capitalize transition-all whitespace-nowrap ${
                    priorityFilter === p
                      ? "bg-slate-200 text-slate-900 font-semibold"
                      : "bg-white/5 text-slate-400 hover:text-white hover:bg-white/10"
                  }`}
                >
                  {p}
                </button>
              ),
            )}
          </div>
        </div>

        {/* Tickets Grid / List */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Tickets List (2 cols) */}
          <div className="lg:col-span-2 space-y-3">
            {loading ? (
              <div className="p-12 text-center text-slate-500 text-sm">
                <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-400" />
                Loading service cases...
              </div>
            ) : filteredTickets.length === 0 ? (
              <div className="p-12 text-center rounded-2xl bg-white/[0.02] border border-white/10 text-slate-400 text-sm">
                No tickets match the selected filters.
              </div>
            ) : (
              filteredTickets.map((ticket) => {
                const isSelected = selectedTicket?.id === ticket.id;
                return (
                  <div
                    key={ticket.id}
                    onClick={() => setSelectedTicket(ticket)}
                    className={`p-4 rounded-2xl border transition-all cursor-pointer backdrop-blur-xl group ${
                      isSelected
                        ? "bg-indigo-950/30 border-indigo-500/50 shadow-lg shadow-indigo-950/50"
                        : "bg-white/[0.02] border-white/10 hover:border-white/20 hover:bg-white/[0.04]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-indigo-400">
                            {ticket.ticket_number}
                          </span>
                          <span
                            className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${getPriorityBadge(ticket.priority)}`}
                          >
                            {ticket.priority}
                          </span>
                          <span
                            className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${getStatusBadge(ticket.status)}`}
                          >
                            {ticket.status.replace("_", " ")}
                          </span>
                          <span className="text-[10px] text-slate-400 bg-white/5 px-2 py-0.5 rounded-full uppercase">
                            {ticket.category}
                          </span>
                        </div>

                        <h3 className="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">
                          {ticket.title}
                        </h3>

                        {ticket.description && (
                          <p className="text-xs text-slate-400 line-clamp-1">
                            {ticket.description}
                          </p>
                        )}
                      </div>

                      <ChevronRight
                        className={`w-4 h-4 text-slate-500 transition-transform ${isSelected ? "translate-x-1 text-indigo-400" : ""}`}
                      />
                    </div>

                    <div className="mt-3 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
                      <div className="flex items-center gap-3">
                        <span className="flex items-center gap-1">
                          <UserCheck className="w-3.5 h-3.5 text-slate-500" />
                          {ticket.assigned_to || "Unassigned"}
                        </span>
                        <span>•</span>
                        <span>
                          {ticket.reporter_name ||
                            ticket.reporter_email ||
                            "Direct"}
                        </span>
                      </div>

                      <div className="flex items-center gap-3">
                        {ticket.sla_breached ? (
                          <span className="text-red-400 font-medium flex items-center gap-1 text-[11px]">
                            <ShieldAlert className="w-3.5 h-3.5" />
                            SLA Breached
                          </span>
                        ) : ticket.sla_due_at ? (
                          <span className="text-slate-400 flex items-center gap-1 text-[11px]">
                            <Clock className="w-3.5 h-3.5 text-slate-500" />
                            SLA due soon
                          </span>
                        ) : null}

                        <span className="flex items-center gap-1 text-[11px] text-slate-500">
                          <MessageSquare className="w-3 h-3" />
                          {ticket.messages?.length || 0}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Right Column: Ticket Inspector / Copilot Drawer (1 col) */}
          <div className="lg:col-span-1">
            {selectedTicket ? (
              <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-2xl space-y-5 sticky top-20">
                <div className="flex items-center justify-between pb-3 border-b border-white/10">
                  <div>
                    <span className="font-mono text-xs text-indigo-400 font-bold">
                      {selectedTicket.ticket_number}
                    </span>
                    <h2 className="text-sm font-bold text-white mt-0.5">
                      {selectedTicket.title}
                    </h2>
                  </div>

                  <div className="flex items-center gap-1">
                    <button
                      onClick={handleRunAITriage}
                      disabled={triagingAI}
                      className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 border border-cyan-500/30 transition-all text-xs flex items-center gap-1"
                      title="Run Gemini AI Triage"
                    >
                      <Sparkles
                        className={`w-3.5 h-3.5 ${triagingAI ? "animate-spin" : ""}`}
                      />
                      <span className="text-[10px] font-semibold">Triage</span>
                    </button>
                  </div>
                </div>

                {/* Status Switcher */}
                <div className="space-y-1.5">
                  <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
                    Case Lifecycle Status
                  </span>
                  <div className="grid grid-cols-4 gap-1">
                    {(
                      [
                        "open",
                        "in_progress",
                        "resolved",
                        "closed",
                      ] as TicketStatus[]
                    ).map((st) => (
                      <button
                        key={st}
                        onClick={() => handleUpdateStatus(st)}
                        className={`py-1.5 px-1 rounded-lg text-[10px] font-bold uppercase transition-all ${
                          selectedTicket.status === st
                            ? "bg-indigo-600 text-white shadow-md"
                            : "bg-white/5 text-slate-400 hover:text-white hover:bg-white/10"
                        }`}
                      >
                        {st.replace("_", " ")}
                      </button>
                    ))}
                  </div>
                </div>

                {/* AI Copilot Triage Box */}
                {selectedTicket.ai_triage &&
                  Object.keys(selectedTicket.ai_triage).length > 0 && (
                    <div className="p-3.5 rounded-xl bg-gradient-to-br from-indigo-950/40 via-purple-950/20 to-slate-900/60 border border-indigo-500/30 space-y-2">
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center gap-1.5 text-cyan-400 font-semibold">
                          <Sparkles className="w-3.5 h-3.5" />
                          <span>Agentforce AI Triage</span>
                        </div>
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono">
                          Urgency: {selectedTicket.ai_triage.urgency_score ?? 7}
                          /10
                        </span>
                      </div>

                      <div className="text-[11px] text-slate-300 space-y-1">
                        <p>
                          <strong className="text-slate-400">Sentiment:</strong>{" "}
                          <span className="capitalize">
                            {selectedTicket.ai_triage.sentiment ||
                              selectedTicket.sentiment ||
                              "Neutral"}
                          </span>
                        </p>
                        {selectedTicket.ai_triage
                          .estimated_resolution_hours && (
                          <p>
                            <strong className="text-slate-400">
                              Est. Resolution:
                            </strong>{" "}
                            {
                              selectedTicket.ai_triage
                                .estimated_resolution_hours
                            }{" "}
                            hours
                          </p>
                        )}
                      </div>

                      {selectedTicket.ai_suggested_response && (
                        <div className="pt-2 border-t border-indigo-500/20">
                          <div className="flex items-center justify-between text-[10px] text-indigo-300 mb-1">
                            <span>Suggested Fast-Response:</span>
                            <button
                              onClick={() =>
                                setReplyText(
                                  selectedTicket.ai_suggested_response || "",
                                )
                              }
                              className="text-cyan-400 hover:text-cyan-300 underline"
                            >
                              Use Draft
                            </button>
                          </div>
                          <p className="text-[11px] text-slate-300 italic bg-black/30 p-2 rounded-lg border border-white/5">
                            "{selectedTicket.ai_suggested_response}"
                          </p>
                        </div>
                      )}
                    </div>
                  )}

                {/* Thread Messages */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
                    <span>Conversation & Notes</span>
                    <span className="text-[10px] text-slate-500 font-normal">
                      {selectedTicket.messages?.length || 0} items
                    </span>
                  </div>

                  <div className="max-h-60 overflow-y-auto space-y-2 pr-1">
                    {selectedTicket.messages &&
                    selectedTicket.messages.length > 0 ? (
                      selectedTicket.messages.map((m) => (
                        <div
                          key={m.id}
                          className={`p-2.5 rounded-xl text-xs space-y-1 ${
                            m.is_internal
                              ? "bg-amber-500/10 border border-amber-500/20 text-amber-200"
                              : m.is_ai_generated
                                ? "bg-cyan-950/30 border border-cyan-500/20 text-cyan-200"
                                : "bg-white/5 border border-white/5 text-slate-300"
                          }`}
                        >
                          <div className="flex items-center justify-between text-[10px] text-slate-400">
                            <span className="font-semibold text-white">
                              {m.author_name}
                              {m.is_internal && (
                                <span className="text-amber-400 ml-1.5 font-normal">
                                  (Internal Note)
                                </span>
                              )}
                              {m.is_ai_generated && (
                                <span className="text-cyan-400 ml-1.5 font-normal">
                                  (AI Generated)
                                </span>
                              )}
                            </span>
                            <span>
                              {new Date(m.created_at).toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })}
                            </span>
                          </div>
                          <p className="text-[11px] leading-relaxed">
                            {m.body}
                          </p>
                        </div>
                      ))
                    ) : (
                      <div className="text-center p-4 text-xs text-slate-500">
                        No replies yet in this thread.
                      </div>
                    )}
                  </div>
                </div>

                {/* Reply Input Box */}
                <div className="space-y-2 pt-2 border-t border-white/10">
                  <div className="flex items-center justify-between text-xs">
                    <label className="text-[11px] text-slate-400 font-medium">
                      Add Message or Note
                    </label>
                    <button
                      type="button"
                      onClick={() => setIsInternalNote(!isInternalNote)}
                      className={`text-[10px] px-2 py-0.5 rounded-full transition-all ${
                        isInternalNote
                          ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                          : "bg-white/5 text-slate-400 hover:text-white"
                      }`}
                    >
                      {isInternalNote
                        ? "✓ Internal Note"
                        : "+ Mark as Internal"}
                    </button>
                  </div>

                  <textarea
                    rows={3}
                    placeholder={
                      isInternalNote
                        ? "Write an internal team note..."
                        : "Write customer response..."
                    }
                    value={replyText}
                    onChange={(e) => setReplyText(e.target.value)}
                    className="w-full p-2.5 rounded-xl bg-white/5 border border-white/10 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none"
                  />

                  <div className="flex justify-end">
                    <button
                      onClick={handleSendReply}
                      disabled={sendingReply || !replyText.trim()}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-xs transition-all shadow-md shadow-indigo-600/30"
                    >
                      <Send className="w-3 h-3" />
                      <span>
                        {sendingReply
                          ? "Sending..."
                          : isInternalNote
                            ? "Post Note"
                            : "Send Reply"}
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-8 rounded-2xl bg-white/[0.02] border border-white/10 text-center text-slate-500 text-xs">
                Select a ticket from the list to view live conversation threads,
                SLA timers, and AI Copilot triage.
              </div>
            )}
          </div>
        </div>

        {/* Create Ticket Modal */}
        {isCreateOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md">
            <div className="w-full max-w-lg rounded-2xl bg-[#0c1222] border border-white/15 p-6 space-y-4 shadow-2xl">
              <div className="flex items-center justify-between pb-2 border-b border-white/10">
                <div className="flex items-center gap-2">
                  <LifeBuoy className="w-5 h-5 text-indigo-400" />
                  <h3 className="text-base font-bold text-white">
                    Create New Support Case
                  </h3>
                </div>
                <button
                  onClick={() => setIsCreateOpen(false)}
                  className="text-slate-400 hover:text-white text-xs p-1"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleCreateTicket} className="space-y-4 text-xs">
                <div>
                  <label className="block text-slate-300 font-medium mb-1">
                    Case Subject *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Single Sign-On Okta metadata sync error"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">
                    Description
                  </label>
                  <textarea
                    rows={3}
                    placeholder="Detailed symptoms, error codes, and customer impact..."
                    value={newDesc}
                    onChange={(e) => setNewDesc(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 font-medium mb-1">
                      Priority
                    </label>
                    <select
                      value={newPriority}
                      onChange={(e) =>
                        setNewPriority(e.target.value as TicketPriority)
                      }
                      className="w-full px-3 py-2 rounded-xl bg-[#0f172a] border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                    >
                      <option value="critical">Critical (1 hr SLA)</option>
                      <option value="high">High (4 hr SLA)</option>
                      <option value="medium">Medium (24 hr SLA)</option>
                      <option value="low">Low (72 hr SLA)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-300 font-medium mb-1">
                      Category
                    </label>
                    <select
                      value={newCategory}
                      onChange={(e) =>
                        setNewCategory(e.target.value as TicketCategory)
                      }
                      className="w-full px-3 py-2 rounded-xl bg-[#0f172a] border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                    >
                      <option value="technical">Technical / API</option>
                      <option value="billing">Billing / Invoicing</option>
                      <option value="bug">Software Bug</option>
                      <option value="onboarding">Onboarding / SSO</option>
                      <option value="general">General Support</option>
                      <option value="feature_request">Feature Request</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 font-medium mb-1">
                      Reporter Name
                    </label>
                    <input
                      type="text"
                      placeholder="e.g. Sarah Chen"
                      value={newReporterName}
                      onChange={(e) => setNewReporterName(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-slate-300 font-medium mb-1">
                      Reporter Email
                    </label>
                    <input
                      type="email"
                      placeholder="e.g. sarah.chen@techcorp.io"
                      value={newReporterEmail}
                      onChange={(e) => setNewReporterEmail(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-[11px] text-slate-300 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-cyan-400 shrink-0" />
                  <span>
                    Gemini AI Triage will automatically assign priority score
                    and draft a recommended response upon creation.
                  </span>
                </div>

                <div className="flex justify-end gap-2 pt-2 border-t border-white/10">
                  <button
                    type="button"
                    onClick={() => setIsCreateOpen(false)}
                    className="px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs transition-all"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting || !newTitle.trim()}
                    className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-xs transition-all shadow-lg shadow-indigo-600/30"
                  >
                    {submitting ? "Creating..." : "Create Case"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
