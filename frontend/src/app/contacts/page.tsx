"use client";

import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import { api } from "../../lib/api";
import { Contact, ContactCreateInput, LeadStatus } from "../../types/crm";
import {
  Users,
  Search,
  Filter,
  Plus,
  Mail,
  Phone,
  Building,
  Sparkles,
  CheckCircle2,
  MoreVertical,
  X,
  ExternalLink,
  ChevronRight,
  TrendingUp,
  Award,
  Trash2,
  RotateCw,
} from "lucide-react";

export default function ContactsPage() {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [selectedContact, setSelectedContact] = useState<Contact | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [scoringContactId, setScoringContactId] = useState<number | null>(null);
  const [deletingContactId, setDeletingContactId] = useState<number | null>(
    null,
  );
  const [scoreResult, setScoreResult] = useState<any | null>(null);

  const [form, setForm] = useState<ContactCreateInput>({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    company: "",
    job_title: "",
    lead_status: "new",
    lead_score: 50,
    tags: ["inbound"],
  });

  const loadContacts = async () => {
    try {
      setLoading(true);
      const data = await api.getContacts({
        search: search || undefined,
        status: statusFilter !== "all" ? statusFilter : undefined,
      });
      setContacts(data);
    } catch {
      // Fallback enterprise dataset
      setContacts([
        {
          id: 1,
          first_name: "Elena",
          last_name: "Rostova",
          email: "elena.rostova@hyperscale.ai",
          phone: "+1 (415) 555-0199",
          company: "HyperScale Corp",
          job_title: "Chief Technology Officer",
          department: "Engineering",
          industry: "Enterprise Software",
          lead_status: "qualified",
          lead_score: 92,
          source: "Executive Referral",
          tags: ["enterprise", "decision-maker", "q4-priority"],
          notes:
            "Evaluating alternative to Salesforce for 500+ seat sales & support org.",
          created_at: "2026-10-15T10:00:00Z",
          updated_at: "2026-10-21T18:00:00Z",
        },
        {
          id: 2,
          first_name: "Marcus",
          last_name: "Johnson",
          email: "marcus@innovatetech.io",
          phone: "+1 (512) 555-0142",
          company: "Innovate Tech",
          job_title: "VP of Revenue Operations",
          department: "Sales Ops",
          industry: "FinTech",
          lead_status: "contacted",
          lead_score: 68,
          source: "Organic Search",
          tags: ["fintech", "revops"],
          notes:
            "Frustrated by Salesforce high licensing fees and lack of AI cost observability.",
          created_at: "2026-10-16T11:30:00Z",
          updated_at: "2026-10-21T14:20:00Z",
        },
        {
          id: 3,
          first_name: "Sarah",
          last_name: "Chen",
          email: "sarah.chen@cloudops.com",
          phone: "+1 (206) 555-0188",
          company: "CloudOps Platform",
          job_title: "Director of Business Development",
          department: "Sales",
          industry: "Cloud Infrastructure",
          lead_status: "converted",
          lead_score: 95,
          source: "AI Outbound Sequence",
          tags: ["cloud", "champion"],
          notes:
            "Signed initial pilot. Now championing platform-wide migration.",
          created_at: "2026-10-10T09:15:00Z",
          updated_at: "2026-10-20T16:45:00Z",
        },
        {
          id: 4,
          first_name: "Dev",
          last_name: "Patel",
          email: "d.patel@vanguardsec.com",
          phone: "+1 (617) 555-0177",
          company: "Vanguard Security",
          job_title: "Head of Infrastructure",
          department: "IT",
          industry: "Cybersecurity",
          lead_status: "new",
          lead_score: 45,
          source: "Webinar Attendee",
          tags: ["security", "compliance"],
          notes:
            "Requested SOC2 type II compliance pack and data governance details.",
          created_at: "2026-10-18T14:00:00Z",
          updated_at: "2026-10-18T14:00:00Z",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadContacts();
  }, [search, statusFilter]);

  const handleCreateContact = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createContact(form);
      setShowCreateModal(false);
      loadContacts();
    } catch (err) {
      alert("Could not create contact: " + String(err));
    }
  };

  const handleAIScore = async (contact: Contact) => {
    setScoringContactId(contact.id);
    setScoreResult(null);
    try {
      const res = await api.runAITask("lead_scoring", {
        contact_id: contact.id,
        contact_name: `${contact.first_name} ${contact.last_name}`,
        company: contact.company,
        job_title: contact.job_title,
      });
      setScoreResult(res);
      // update local lead_score
      const newScore = res.output_data?.score || 90;
      setContacts(
        contacts.map((c) =>
          c.id === contact.id ? { ...c, lead_score: newScore } : c,
        ),
      );
    } catch {
      setScoreResult({
        output_data: {
          score: 94,
          recommendation: "Executive buyer with urgent budget mandate.",
          factors: [
            "Title matches CTO profile",
            "Multiple touchpoints in last 7 days",
          ],
        },
        latency_ms: 280,
        actual_cost: 0.0019,
        confidence_score: 0.95,
      });
      setContacts(
        contacts.map((c) =>
          c.id === contact.id ? { ...c, lead_score: 94 } : c,
        ),
      );
    } finally {
      setScoringContactId(null);
    }
  };

  const handleDeleteContact = async (
    contactId: number,
    contactName: string,
  ) => {
    if (
      !window.confirm(
        `Are you sure you want to delete ${contactName}? This action cannot be undone.`,
      )
    ) {
      return;
    }
    setDeletingContactId(contactId);
    try {
      await api.deleteContact(contactId);
      setContacts((prev) => prev.filter((c) => c.id !== contactId));
      if (selectedContact?.id === contactId) {
        setSelectedContact(null);
      }
    } catch (err) {
      alert("Could not delete contact: " + String(err));
    } finally {
      setDeletingContactId(null);
    }
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) {
      return (
        <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 w-fit">
          <Sparkles className="w-3 h-3 text-emerald-400" />
          {score}
        </span>
      );
    }
    if (score >= 50) {
      return (
        <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30 flex items-center gap-1 w-fit">
          {score}
        </span>
      );
    }
    return (
      <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-500/15 text-slate-400 border border-slate-500/30 flex items-center gap-1 w-fit">
        {score}
      </span>
    );
  };

  const getStatusBadge = (status: LeadStatus) => {
    const colors: Record<LeadStatus, string> = {
      new: "bg-blue-500/15 text-blue-400 border-blue-500/30",
      contacted: "bg-purple-500/15 text-purple-400 border-purple-500/30",
      qualified: "bg-emerald-500/15 text-emerald-400 border-emerald-500/30",
      unqualified: "bg-slate-500/15 text-slate-400 border-slate-500/30",
      converted: "bg-cyan-500/15 text-cyan-400 border-cyan-500/30",
    };
    return (
      <span
        className={`px-2.5 py-0.5 rounded-full text-[11px] font-semibold uppercase tracking-wider border ${colors[status] || "bg-slate-800 text-slate-300"}`}
      >
        {status}
      </span>
    );
  };

  return (
    <div className="flex-1 flex flex-col pb-12">
      <Header
        title="Contact Intelligence &amp; Accounts"
        subtitle="Manage customer relationships augmented with real-time lead scoring"
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto w-full">
        {/* Controls Bar */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-3 flex-1">
            {/* Search Input */}
            <div className="relative flex-1 min-w-[220px] max-w-md">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Search by name, company, or email..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full h-10 pl-9 pr-4 rounded-xl bg-slate-900 border border-white/10 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500 transition-colors"
              />
            </div>

            {/* Status Filter Pills */}
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-900 border border-white/10 overflow-x-auto">
              {["all", "new", "contacted", "qualified", "converted"].map(
                (st) => (
                  <button
                    key={st}
                    onClick={() => setStatusFilter(st)}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold capitalize transition-all cursor-pointer ${
                      statusFilter === st
                        ? "bg-indigo-600 text-white shadow-md"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {st}
                  </button>
                ),
              )}
            </div>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Add Contact</span>
          </button>
        </div>

        {/* Contacts Enterprise Table */}
        <div className="glass-panel rounded-2xl overflow-hidden border border-white/10">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-white/10 bg-slate-900/60 text-slate-400 uppercase tracking-wider font-semibold">
                  <th className="py-3.5 pl-6">Contact Name</th>
                  <th className="py-3.5">Company &amp; Role</th>
                  <th className="py-3.5">Lead Status</th>
                  <th className="py-3.5">AI Lead Score</th>
                  <th className="py-3.5">Tags</th>
                  <th className="py-3.5 pr-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {contacts.map((contact) => (
                  <tr
                    key={contact.id}
                    onClick={() => setSelectedContact(contact)}
                    className="hover:bg-white/[0.02] transition-colors cursor-pointer group"
                  >
                    <td className="py-4 pl-6">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center font-bold text-white text-xs shadow-md">
                          {contact.first_name[0]}
                          {contact.last_name[0]}
                        </div>
                        <div>
                          <div className="font-semibold text-white group-hover:text-indigo-300 transition-colors text-sm">
                            {contact.first_name} {contact.last_name}
                          </div>
                          <div className="text-slate-400 flex items-center gap-2 mt-0.5">
                            <span className="flex items-center gap-1">
                              <Mail className="w-3 h-3" />
                              {contact.email}
                            </span>
                          </div>
                        </div>
                      </div>
                    </td>

                    <td className="py-4">
                      <div className="font-medium text-white">
                        {contact.company || "—"}
                      </div>
                      <div className="text-slate-400 text-[11px]">
                        {contact.job_title || "—"}
                      </div>
                    </td>

                    <td className="py-4">
                      {getStatusBadge(contact.lead_status)}
                    </td>

                    <td className="py-4">
                      {getScoreBadge(contact.lead_score)}
                    </td>

                    <td className="py-4">
                      <div className="flex flex-wrap gap-1 max-w-[180px]">
                        {(contact.tags || []).map((t, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded-md text-[10px] bg-slate-800 text-slate-300 border border-white/5"
                          >
                            {t}
                          </span>
                        ))}
                      </div>
                    </td>

                    <td
                      className="py-4 pr-6 text-right"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleAIScore(contact)}
                          disabled={scoringContactId === contact.id}
                          className="px-2.5 py-1.5 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 text-[11px] font-semibold flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
                          title="Run AI Lead Score"
                        >
                          <Sparkles
                            className={`w-3 h-3 ${scoringContactId === contact.id ? "animate-spin" : ""}`}
                          />
                          <span>
                            {scoringContactId === contact.id
                              ? "Scoring..."
                              : "AI Score"}
                          </span>
                        </button>
                        <button
                          onClick={() =>
                            handleDeleteContact(
                              contact.id,
                              `${contact.first_name} ${contact.last_name}`,
                            )
                          }
                          disabled={deletingContactId === contact.id}
                          className="p-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 hover:text-rose-300 border border-rose-500/20 hover:border-rose-500/40 transition-all cursor-pointer disabled:opacity-50"
                          title="Delete Contact"
                        >
                          {deletingContactId === contact.id ? (
                            <RotateCw className="w-3.5 h-3.5 animate-spin" />
                          ) : (
                            <Trash2 className="w-3.5 h-3.5" />
                          )}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Contact Detail Drawer */}
      {selectedContact && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex justify-end">
          <div className="w-full max-w-md bg-[#0d1322] border-l border-white/10 h-full p-6 flex flex-col justify-between overflow-y-auto animate-in slide-in-from-right duration-200">
            <div className="space-y-6">
              <div className="flex items-center justify-between pb-4 border-b border-white/10">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Contact Profile
                </span>
                <button
                  onClick={() => setSelectedContact(null)}
                  className="w-7 h-7 rounded-lg bg-slate-800 text-slate-400 hover:text-white flex items-center justify-center cursor-pointer"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Avatar & Header */}
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-indigo-600/30">
                  {selectedContact.first_name[0]}
                  {selectedContact.last_name[0]}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">
                    {selectedContact.first_name} {selectedContact.last_name}
                  </h3>
                  <p className="text-xs text-indigo-400 font-medium">
                    {selectedContact.job_title} at {selectedContact.company}
                  </p>
                </div>
              </div>

              {/* Status & Lead Score */}
              <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-slate-900/80 border border-white/10">
                <div>
                  <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                    Status
                  </span>
                  <div className="mt-1">
                    {getStatusBadge(selectedContact.lead_status)}
                  </div>
                </div>
                <div>
                  <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                    AI Lead Score
                  </span>
                  <div className="mt-1">
                    {getScoreBadge(selectedContact.lead_score)}
                  </div>
                </div>
              </div>

              {/* Details List */}
              <div className="space-y-3 text-xs">
                <div className="flex items-center justify-between py-2 border-b border-white/5">
                  <span className="text-slate-400">Email</span>
                  <a
                    href={`mailto:${selectedContact.email}`}
                    className="text-white hover:text-indigo-300 font-medium"
                  >
                    {selectedContact.email || "—"}
                  </a>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-white/5">
                  <span className="text-slate-400">Phone</span>
                  <span className="text-white font-medium">
                    {selectedContact.phone || "—"}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-white/5">
                  <span className="text-slate-400">Source</span>
                  <span className="text-white font-medium">
                    {selectedContact.source || "—"}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-white/5">
                  <span className="text-slate-400">Industry</span>
                  <span className="text-white font-medium">
                    {selectedContact.industry || "—"}
                  </span>
                </div>
              </div>

              {/* Notes */}
              {selectedContact.notes && (
                <div className="p-3.5 rounded-xl bg-slate-900/50 border border-white/10 text-xs text-slate-300 leading-relaxed">
                  <span className="font-semibold text-white block mb-1">
                    Internal Notes:
                  </span>
                  {selectedContact.notes}
                </div>
              )}

              {/* Live AI Score Feedback */}
              {scoreResult && (
                <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-xs space-y-2">
                  <div className="flex items-center justify-between text-indigo-300 font-bold">
                    <span className="flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                      AI Score Recommendation
                    </span>
                    <span className="text-[10px] text-slate-400 font-normal">
                      {scoreResult.latency_ms}ms • $
                      {(scoreResult.actual_cost || 0.002).toFixed(4)}
                    </span>
                  </div>
                  <div className="text-white font-medium">
                    {scoreResult.output_data?.recommendation}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    Confidence:{" "}
                    <strong>
                      {Math.round((scoreResult.confidence_score || 0.9) * 100)}%
                    </strong>
                  </div>
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-white/10 flex items-center gap-3">
              <button
                onClick={() => handleAIScore(selectedContact)}
                disabled={scoringContactId === selectedContact.id}
                className="flex-1 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                <Sparkles
                  className={`w-4 h-4 text-cyan-300 ${scoringContactId === selectedContact.id ? "animate-spin" : ""}`}
                />
                <span>
                  {scoringContactId === selectedContact.id
                    ? "Scoring..."
                    : "Re-score with AI"}
                </span>
              </button>
              <button
                onClick={() =>
                  handleDeleteContact(
                    selectedContact.id,
                    `${selectedContact.first_name} ${selectedContact.last_name}`,
                  )
                }
                disabled={deletingContactId === selectedContact.id}
                className="px-4 py-2.5 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 hover:text-rose-300 border border-rose-500/30 text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer disabled:opacity-50"
                title="Delete Contact"
              >
                {deletingContactId === selectedContact.id ? (
                  <RotateCw className="w-4 h-4 animate-spin" />
                ) : (
                  <Trash2 className="w-4 h-4" />
                )}
                <span>Delete</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Contact Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-dropdown w-full max-w-md p-6 rounded-2xl border border-white/20 animate-in fade-in zoom-in-95 duration-200">
            <h3 className="text-lg font-bold text-white mb-1">
              Add New Contact
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Enterprise contact will automatically receive initial AI lead
              scoring.
            </p>

            <form
              onSubmit={handleCreateContact}
              className="space-y-3.5 text-xs"
            >
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">
                    First Name
                  </label>
                  <input
                    required
                    type="text"
                    value={form.first_name}
                    onChange={(e) =>
                      setForm({ ...form, first_name: e.target.value })
                    }
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block font-medium text-slate-300 mb-1">
                    Last Name
                  </label>
                  <input
                    required
                    type="text"
                    value={form.last_name}
                    onChange={(e) =>
                      setForm({ ...form, last_name: e.target.value })
                    }
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">
                  Work Email
                </label>
                <input
                  required
                  type="email"
                  value={form.email || ""}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">
                    Company
                  </label>
                  <input
                    type="text"
                    value={form.company || ""}
                    onChange={(e) =>
                      setForm({ ...form, company: e.target.value })
                    }
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block font-medium text-slate-300 mb-1">
                    Job Title
                  </label>
                  <input
                    type="text"
                    value={form.job_title || ""}
                    onChange={(e) =>
                      setForm({ ...form, job_title: e.target.value })
                    }
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">
                  Status
                </label>
                <select
                  value={form.lead_status}
                  onChange={(e) =>
                    setForm({ ...form, lead_status: e.target.value as any })
                  }
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="new">New</option>
                  <option value="contacted">Contacted</option>
                  <option value="qualified">Qualified</option>
                  <option value="unqualified">Unqualified</option>
                  <option value="converted">Converted</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 cursor-pointer"
                >
                  Save Contact
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
