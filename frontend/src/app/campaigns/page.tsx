"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/Header";
import { api } from "@/lib/api";
import {
  Campaign,
  CampaignStats,
  CampaignTemplate,
  CampaignType,
  CampaignStatus,
} from "@/types/crm";
import {
  Megaphone,
  Plus,
  Send,
  Sparkles,
  BarChart3,
  Mail,
  TrendingUp,
  Users,
  Clock,
  CheckCircle2,
  AlertCircle,
  Copy,
  ChevronRight,
  RefreshCw,
  Search,
  DollarSign,
  Layers,
  ArrowUpRight,
} from "lucide-react";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [stats, setStats] = useState<CampaignStats | null>(null);
  const [templates, setTemplates] = useState<CampaignTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState(() => {
    if (typeof window !== "undefined") {
      return new URLSearchParams(window.location.search).get("search") || "";
    }
    return "";
  });
  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(
    null,
  );

  // New Campaign Modal
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newType, setNewType] = useState<CampaignType>("email");
  const [newSubject, setNewSubject] = useState("");
  const [newPreview, setNewPreview] = useState("");
  const [newBody, setNewBody] = useState("");
  const [newIndustry, setNewIndustry] = useState("");
  const [enableABTest, setEnableABTest] = useState(false);
  const [abSubject, setAbSubject] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Action states
  const [sendingId, setSendingId] = useState<number | null>(null);
  const [optimizingId, setOptimizingId] = useState<number | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [campaignsData, statsData, templatesData] = await Promise.all([
        api.getCampaigns(),
        api.getCampaignStats().catch(() => null),
        api.getCampaignTemplates().catch(() => []),
      ]);
      setCampaigns(campaignsData);
      if (statsData) setStats(statsData);
      if (templatesData) setTemplates(templatesData);
      if (selectedCampaign) {
        const refreshed = campaignsData.find(
          (c) => c.id === selectedCampaign.id,
        );
        if (refreshed) setSelectedCampaign(refreshed);
      }
    } catch (err) {
      console.error("Failed to load campaigns:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleApplyTemplate = (tpl: CampaignTemplate) => {
    setNewName(tpl.name);
    setNewType(tpl.type);
    setNewSubject(tpl.subject);
    setNewPreview(tpl.preview_text);
    setNewBody(tpl.body_text);
    if (tpl.suggested_audience?.industry) {
      setNewIndustry(tpl.suggested_audience.industry);
    }
  };

  const handleCreateCampaign = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim() || !newSubject.trim()) return;
    try {
      setSubmitting(true);
      const created = await api.createCampaign({
        name: newName,
        type: newType,
        subject: newSubject,
        preview_text: newPreview,
        body_text: newBody,
        body_html: `<p>${newBody.replace(/\n/g, "<br/>")}</p>`,
        audience_filter: newIndustry ? { industry: newIndustry } : {},
        ab_test_enabled: enableABTest,
        ab_variant_subject: enableABTest ? abSubject : undefined,
      });
      setIsCreateOpen(false);
      setNewName("");
      setNewSubject("");
      setNewPreview("");
      setNewBody("");
      await loadData();
      setSelectedCampaign(created);
    } catch (err) {
      console.error("Failed to create campaign:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleSendCampaign = async (campaignId: number) => {
    try {
      setSendingId(campaignId);
      const updated = await api.sendCampaign(campaignId);
      setCampaigns((prev) =>
        prev.map((c) => (c.id === updated.id ? updated : c)),
      );
      if (selectedCampaign?.id === campaignId) setSelectedCampaign(updated);
      await loadData();
    } catch (err) {
      console.error("Failed to send campaign:", err);
    } finally {
      setSendingId(null);
    }
  };

  const handleOptimizeAI = async (campaignId: number) => {
    try {
      setOptimizingId(campaignId);
      const updated = await api.optimizeCampaignAI(campaignId);
      setCampaigns((prev) =>
        prev.map((c) => (c.id === updated.id ? updated : c)),
      );
      if (selectedCampaign?.id === campaignId) setSelectedCampaign(updated);
    } catch (err) {
      console.error("Failed to optimize campaign:", err);
    } finally {
      setOptimizingId(null);
    }
  };

  const filteredCampaigns = campaigns.filter((c) => {
    const matchesSearch =
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (c.subject &&
        c.subject.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesStatus = statusFilter === "all" || c.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusBadge = (status: CampaignStatus) => {
    switch (status) {
      case "active":
        return "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30";
      case "completed":
        return "bg-blue-500/15 text-blue-400 border border-blue-500/30";
      case "scheduled":
        return "bg-purple-500/15 text-purple-400 border border-purple-500/30";
      case "draft":
        return "bg-slate-500/15 text-slate-400 border border-slate-500/30";
      default:
        return "bg-slate-500/15 text-slate-400 border border-slate-500/30";
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
              <span className="p-1.5 rounded-lg bg-pink-500/10 text-pink-400 border border-pink-500/20">
                <Megaphone className="w-5 h-5" />
              </span>
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Marketing Cloud{" "}
                <span className="text-pink-400 font-normal">
                  / Email Campaigns & Journeys
                </span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Multi-channel campaign orchestration, AI-optimized subject lines,
              audience targeting, and real-time revenue attribution.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={loadData}
              disabled={loading}
              className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition-all border border-white/10"
              title="Refresh campaigns"
            >
              <RefreshCw
                className={`w-4 h-4 ${loading ? "animate-spin" : ""}`}
              />
            </button>

            <button
              onClick={() => setIsCreateOpen(true)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-medium text-sm transition-all shadow-lg shadow-pink-600/30"
            >
              <Plus className="w-4 h-4" />
              <span>Create Campaign</span>
            </button>
          </div>
        </div>

        {/* Top KPI Metrics Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Total Campaigns</span>
              <Megaphone className="w-4 h-4 text-pink-400" />
            </div>
            <div className="text-2xl font-bold text-white mt-2">
              {stats?.total ?? campaigns.length}
            </div>
            <div className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
              <span>{stats?.active ?? 0} active</span> •{" "}
              <span>{stats?.completed ?? 0} sent</span>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Total Delivered Emails</span>
              <Mail className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="text-2xl font-bold text-cyan-400 mt-2">
              {(stats?.total_emails_sent ?? 0).toLocaleString()}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              Enterprise delivery rate &gt; 98.4%
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Average Open Rate</span>
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-bold text-emerald-400 mt-2">
              {((stats?.avg_open_rate ?? 0.35) * 100).toFixed(1)}%
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              Avg click rate:{" "}
              {((stats?.avg_click_rate ?? 0.12) * 100).toFixed(1)}%
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between text-slate-400 text-xs">
              <span>Attributed Revenue</span>
              <DollarSign className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-bold text-amber-400 mt-2">
              ${(stats?.total_revenue_attributed ?? 0).toLocaleString()}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              Pipeline influenced directly
            </div>
          </div>
        </div>

        {/* Filter & Search Bar */}
        <div className="p-3 rounded-2xl bg-white/[0.02] border border-white/10 flex flex-col md:flex-row items-center justify-between gap-3">
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search campaigns by name or subject line..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-white/5 border border-white/10 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-pink-500 transition-all"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto overflow-x-auto pb-1 md:pb-0">
            {(
              ["all", "active", "completed", "scheduled", "draft"] as const
            ).map((s) => (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium capitalize transition-all whitespace-nowrap ${
                  statusFilter === s
                    ? "bg-pink-600 text-white shadow-md shadow-pink-600/30"
                    : "bg-white/5 text-slate-400 hover:text-white hover:bg-white/10"
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Main Campaigns List + Inspector Drawer Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Campaigns List (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            {loading ? (
              <div className="p-12 text-center text-slate-500 text-sm">
                <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-pink-400" />
                Loading email campaigns...
              </div>
            ) : filteredCampaigns.length === 0 ? (
              <div className="p-12 text-center rounded-2xl bg-white/[0.02] border border-white/10 text-slate-400 text-sm">
                No campaigns found for the selected filter.
              </div>
            ) : (
              filteredCampaigns.map((camp) => {
                const isSelected = selectedCampaign?.id === camp.id;
                return (
                  <div
                    key={camp.id}
                    onClick={() => setSelectedCampaign(camp)}
                    className={`p-5 rounded-2xl border transition-all cursor-pointer backdrop-blur-xl group ${
                      isSelected
                        ? "bg-pink-950/25 border-pink-500/50 shadow-lg shadow-pink-950/40"
                        : "bg-white/[0.02] border-white/10 hover:border-white/20 hover:bg-white/[0.04]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="space-y-1.5 flex-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span
                            className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${getStatusBadge(camp.status)}`}
                          >
                            {camp.status}
                          </span>
                          <span className="text-[10px] text-pink-300 bg-pink-500/10 px-2 py-0.5 rounded-full uppercase font-medium">
                            {camp.type.replace("_", " ")}
                          </span>
                          {camp.ai_score && (
                            <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-2 py-0.5 rounded-full flex items-center gap-1">
                              <Sparkles className="w-2.5 h-2.5" />
                              AI Score: {camp.ai_score}/100
                            </span>
                          )}
                        </div>

                        <h3 className="text-base font-bold text-white group-hover:text-pink-300 transition-colors">
                          {camp.name}
                        </h3>

                        {camp.subject && (
                          <p className="text-xs text-slate-300 italic flex items-center gap-1.5">
                            <span className="text-slate-500">Subject:</span>"
                            {camp.subject}"
                          </p>
                        )}
                      </div>

                      <div className="flex items-center gap-2">
                        {camp.status === "draft" && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleSendCampaign(camp.id);
                            }}
                            disabled={sendingId === camp.id}
                            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-pink-600 hover:bg-pink-500 disabled:opacity-50 text-white text-xs font-semibold shadow-md shadow-pink-600/30 transition-all"
                          >
                            <Send className="w-3 h-3" />
                            <span>
                              {sendingId === camp.id ? "Sending..." : "Launch"}
                            </span>
                          </button>
                        )}

                        <ChevronRight
                          className={`w-4 h-4 text-slate-500 transition-transform ${isSelected ? "translate-x-1 text-pink-400" : ""}`}
                        />
                      </div>
                    </div>

                    {/* Metrics Bar */}
                    <div className="grid grid-cols-4 gap-3 mt-4 pt-4 border-t border-white/5 text-xs">
                      <div>
                        <span className="text-slate-500 text-[10px] block">
                          Audience
                        </span>
                        <span className="text-white font-semibold flex items-center gap-1 mt-0.5">
                          <Users className="w-3 h-3 text-slate-400" />
                          {camp.recipient_count?.toLocaleString() ||
                            "All leads"}
                        </span>
                      </div>

                      <div>
                        <span className="text-slate-500 text-[10px] block">
                          Open Rate
                        </span>
                        <span className="text-emerald-400 font-semibold mt-0.5 block">
                          {(camp.open_rate * 100).toFixed(1)}%
                        </span>
                        <div className="w-full bg-white/10 h-1 rounded-full mt-1 overflow-hidden">
                          <div
                            className="bg-emerald-500 h-full rounded-full"
                            style={{
                              width: `${Math.min(camp.open_rate * 100, 100)}%`,
                            }}
                          />
                        </div>
                      </div>

                      <div>
                        <span className="text-slate-500 text-[10px] block">
                          Click Rate
                        </span>
                        <span className="text-cyan-400 font-semibold mt-0.5 block">
                          {(camp.click_rate * 100).toFixed(1)}%
                        </span>
                        <div className="w-full bg-white/10 h-1 rounded-full mt-1 overflow-hidden">
                          <div
                            className="bg-cyan-500 h-full rounded-full"
                            style={{
                              width: `${Math.min(camp.click_rate * 100 * 2.5, 100)}%`,
                            }}
                          />
                        </div>
                      </div>

                      <div>
                        <span className="text-slate-500 text-[10px] block">
                          Revenue Attributed
                        </span>
                        <span className="text-amber-400 font-semibold mt-0.5 block">
                          ${(camp.revenue_attributed || 0).toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* Right Column: Campaign Detail / AI Optimization Inspector */}
          <div className="lg:col-span-1">
            {selectedCampaign ? (
              <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-2xl space-y-5 sticky top-20">
                <div className="flex items-center justify-between pb-3 border-b border-white/10">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-pink-400">
                      Campaign Inspector
                    </span>
                    <h2 className="text-sm font-bold text-white mt-0.5">
                      {selectedCampaign.name}
                    </h2>
                  </div>

                  <button
                    onClick={() => handleOptimizeAI(selectedCampaign.id)}
                    disabled={optimizingId === selectedCampaign.id}
                    className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500/20 border border-cyan-500/30 transition-all text-xs flex items-center gap-1"
                    title="Run Gemini Campaign Optimizer"
                  >
                    <Sparkles
                      className={`w-3.5 h-3.5 ${optimizingId === selectedCampaign.id ? "animate-spin" : ""}`}
                    />
                    <span className="text-[10px] font-semibold">
                      AI Optimize
                    </span>
                  </button>
                </div>

                {/* Performance Highlights */}
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                    <span className="text-slate-400 text-[10px]">
                      Delivered
                    </span>
                    <div className="text-base font-bold text-white mt-1">
                      {selectedCampaign.emails_delivered?.toLocaleString() || 0}
                    </div>
                  </div>
                  <div className="p-3 rounded-xl bg-white/5 border border-white/5">
                    <span className="text-slate-400 text-[10px]">
                      Unique Clicks
                    </span>
                    <div className="text-base font-bold text-cyan-400 mt-1">
                      {selectedCampaign.emails_clicked?.toLocaleString() || 0}
                    </div>
                  </div>
                </div>

                {/* AI Insights & Quality Score */}
                {selectedCampaign.ai_insights &&
                  Object.keys(selectedCampaign.ai_insights).length > 0 && (
                    <div className="p-3.5 rounded-xl bg-gradient-to-br from-pink-950/40 via-purple-950/20 to-slate-900/60 border border-pink-500/30 space-y-2.5">
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center gap-1.5 text-pink-400 font-semibold">
                          <Sparkles className="w-3.5 h-3.5" />
                          <span>AI Optimization Insights</span>
                        </div>
                        {selectedCampaign.ai_score && (
                          <span className="text-[10px] px-2 py-0.5 rounded-full bg-pink-500/20 text-pink-300 font-mono">
                            Score: {selectedCampaign.ai_score}/100
                          </span>
                        )}
                      </div>

                      {selectedCampaign.ai_insights.recommendation && (
                        <p className="text-[11px] text-slate-200 bg-black/30 p-2.5 rounded-lg border border-white/5">
                          <strong className="text-cyan-400">
                            Recommendation:
                          </strong>{" "}
                          {selectedCampaign.ai_insights.recommendation}
                        </p>
                      )}

                      {selectedCampaign.ai_insights.strengths &&
                        selectedCampaign.ai_insights.strengths.length > 0 && (
                          <div className="space-y-1">
                            <span className="text-[10px] text-emerald-400 font-semibold uppercase tracking-wider">
                              Strengths
                            </span>
                            <ul className="text-[11px] text-slate-300 space-y-0.5 pl-2 list-disc list-inside">
                              {selectedCampaign.ai_insights.strengths.map(
                                (s, idx) => (
                                  <li key={idx}>{s}</li>
                                ),
                              )}
                            </ul>
                          </div>
                        )}
                    </div>
                  )}

                {/* Email Content Preview */}
                <div className="space-y-2">
                  <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
                    Email Copy Preview
                  </span>
                  <div className="p-3 rounded-xl bg-white/[0.02] border border-white/10 text-xs space-y-2">
                    <div>
                      <span className="text-slate-500 text-[10px]">
                        Subject Line:
                      </span>
                      <p className="text-white font-medium">
                        {selectedCampaign.subject || "None"}
                      </p>
                    </div>
                    {selectedCampaign.preview_text && (
                      <div>
                        <span className="text-slate-500 text-[10px]">
                          Preview Text:
                        </span>
                        <p className="text-slate-400">
                          {selectedCampaign.preview_text}
                        </p>
                      </div>
                    )}
                    {selectedCampaign.body_text && (
                      <div>
                        <span className="text-slate-500 text-[10px]">
                          Body Snippet:
                        </span>
                        <p className="text-slate-300 text-[11px] whitespace-pre-line bg-black/20 p-2 rounded-lg mt-1 border border-white/5">
                          {selectedCampaign.body_text}
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Quick Action Button */}
                {selectedCampaign.status === "draft" && (
                  <button
                    onClick={() => handleSendCampaign(selectedCampaign.id)}
                    disabled={sendingId === selectedCampaign.id}
                    className="w-full py-2.5 rounded-xl bg-pink-600 hover:bg-pink-500 disabled:opacity-50 text-white font-semibold text-xs shadow-lg shadow-pink-600/30 transition-all flex items-center justify-center gap-2"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>
                      {sendingId === selectedCampaign.id
                        ? "Sending Campaign..."
                        : "Launch Campaign"}
                    </span>
                  </button>
                )}
              </div>
            ) : (
              <div className="p-8 rounded-2xl bg-white/[0.02] border border-white/10 text-center text-slate-500 text-xs">
                Select a campaign to inspect click-through analytics,
                deliverability rates, and AI content optimization.
              </div>
            )}
          </div>
        </div>

        {/* Create Campaign Modal */}
        {isCreateOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-md">
            <div className="w-full max-w-2xl rounded-2xl bg-[#0c1222] border border-white/15 p-6 space-y-5 shadow-2xl max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between pb-2 border-b border-white/10">
                <div className="flex items-center gap-2">
                  <Megaphone className="w-5 h-5 text-pink-400" />
                  <h3 className="text-base font-bold text-white">
                    Create Marketing Campaign
                  </h3>
                </div>
                <button
                  onClick={() => setIsCreateOpen(false)}
                  className="text-slate-400 hover:text-white text-xs p-1"
                >
                  ✕
                </button>
              </div>

              {/* Template Picker */}
              {templates.length > 0 && (
                <div className="space-y-2">
                  <label className="text-xs text-slate-300 font-medium">
                    Or Start From High-Converting Template:
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {templates.map((tpl) => (
                      <button
                        key={tpl.id}
                        type="button"
                        onClick={() => handleApplyTemplate(tpl)}
                        className="p-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-left transition-all group"
                      >
                        <span className="text-xs font-semibold text-pink-300 block group-hover:text-pink-200">
                          {tpl.name}
                        </span>
                        <span className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                          {tpl.subject}
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <form
                onSubmit={handleCreateCampaign}
                className="space-y-4 text-xs"
              >
                <div>
                  <label className="block text-slate-300 font-medium mb-1">
                    Campaign Internal Name *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Q4 Executive AI Transformation Briefing"
                    value={newName}
                    onChange={(e) => setNewName(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-300 font-medium mb-1">
                      Campaign Channel
                    </label>
                    <select
                      value={newType}
                      onChange={(e) =>
                        setNewType(e.target.value as CampaignType)
                      }
                      className="w-full px-3 py-2 rounded-xl bg-[#0f172a] border border-white/10 text-white focus:outline-none focus:border-pink-500"
                    >
                      <option value="email">Email Broadcast</option>
                      <option value="nurture_sequence">Nurture Sequence</option>
                      <option value="announcement">Product Announcement</option>
                      <option value="promotional">Promotional Offer</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-slate-300 font-medium mb-1">
                      Target Industry Filter
                    </label>
                    <select
                      value={newIndustry}
                      onChange={(e) => setNewIndustry(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-[#0f172a] border border-white/10 text-white focus:outline-none focus:border-pink-500"
                    >
                      <option value="">All Industries (Entire Database)</option>
                      <option value="Technology">Technology & SaaS</option>
                      <option value="Healthcare">Healthcare</option>
                      <option value="Finance">Financial Services</option>
                      <option value="Retail">Retail & E-commerce</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">
                    Email Subject Line *
                  </label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Exclusive Invite: Scaling Revenue Operations with Autonomous AI Agents"
                    value={newSubject}
                    onChange={(e) => setNewSubject(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">
                    Preview Text / Snippet
                  </label>
                  <input
                    type="text"
                    placeholder="Brief preview line shown in email client inbox..."
                    value={newPreview}
                    onChange={(e) => setNewPreview(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-medium mb-1">
                    Email Body Content
                  </label>
                  <textarea
                    rows={4}
                    placeholder="Use {{first_name}} and {{company}} tokens for hyper-personalization..."
                    value={newBody}
                    onChange={(e) => setNewBody(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500 resize-none font-mono text-[11px]"
                  />
                </div>

                {/* A/B Testing Toggle */}
                <div className="p-3 rounded-xl bg-white/[0.02] border border-white/10 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-300 font-medium">
                      Enable A/B Subject Line Test
                    </span>
                    <input
                      type="checkbox"
                      checked={enableABTest}
                      onChange={(e) => setEnableABTest(e.target.checked)}
                      className="rounded accent-pink-600"
                    />
                  </div>
                  {enableABTest && (
                    <input
                      type="text"
                      placeholder="Variant B Subject: How top teams are automating 65% of CRM data entry"
                      value={abSubject}
                      onChange={(e) => setAbSubject(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-pink-500 mt-2"
                    />
                  )}
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
                    disabled={
                      submitting || !newName.trim() || !newSubject.trim()
                    }
                    className="px-4 py-2 rounded-xl bg-pink-600 hover:bg-pink-500 disabled:opacity-50 text-white font-medium text-xs transition-all shadow-lg shadow-pink-600/30"
                  >
                    {submitting ? "Creating..." : "Save Campaign Draft"}
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
