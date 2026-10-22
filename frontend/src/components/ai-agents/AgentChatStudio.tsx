"use client";

import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import {
  Send,
  Sparkles,
  Bot,
  User as UserIcon,
  RotateCw,
  Terminal,
  Calendar,
  Award,
  Users,
  Megaphone,
  Check,
  Copy,
  ChevronRight,
  Zap,
  Mail,
  ShieldAlert,
  FileText,
  Clock,
  Trash2,
  ExternalLink,
} from "lucide-react";
import { AgentChatMessage, AIAgentChatResponse } from "../../types/crm";

interface AgentChatStudioProps {
  messages: AgentChatMessage[];
  isExecuting: boolean;
  onSendMessage: (text: string) => Promise<void>;
  onClearChat: () => void;
  onSelectGraphRun?: (response: AIAgentChatResponse) => void;
  modelName?: string;
  initialInput?: string;
}

const QUICK_PROMPTS = [
  {
    label: "📅 Schedule Demo",
    prompt: "Schedule a product demo with Sarah Chen for tomorrow at 2:00 PM",
  },
  {
    label: "💼 Create Deal",
    prompt: "Create a $220,000 deal for Acme Corp in Proposal stage",
  },
  {
    label: "🎯 Score Lead",
    prompt:
      "Score lead Elena Rostova from HyperScale for enterprise buyer intent",
  },
  {
    label: "✉️ Draft Email",
    prompt:
      "Draft a follow-up email to Sarah Chen regarding architecture review",
  },
  {
    label: "🛡️ Deal Risk",
    prompt:
      "Analyze deal risk and win probability for TechCorp Enterprise Platform",
  },
  {
    label: "⚠️ Churn Alert",
    prompt: "Identify enterprise accounts with elevated churn risk",
  },
  {
    label: "📝 Meeting Notes",
    prompt:
      "Summarize meeting notes and action items for Stark Industries review",
  },
  {
    label: "👥 Add Contact",
    prompt:
      "Add new lead David Vance at CyberDyne Systems with email david@cyberdyne.io",
  },
  {
    label: "📢 Create Campaign",
    prompt: "Create a Q4 Expansion email campaign targeting SaaS leaders",
  },
];

export default function AgentChatStudio({
  messages,
  isExecuting,
  onSendMessage,
  onClearChat,
  onSelectGraphRun,
  modelName = "google/gemini-2.5-flash-lite",
  initialInput = "",
}: AgentChatStudioProps) {
  const [inputText, setInputText] = useState(initialInput);
  const chatScrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (initialInput) {
      setInputText(initialInput);
    }
  }, [initialInput]);

  useEffect(() => {
    // Only auto-scroll the internal chat container if there are messages or an active execution
    if (!chatScrollContainerRef.current) return;
    if (messages.length === 0 && !isExecuting) return;

    requestAnimationFrame(() => {
      if (chatScrollContainerRef.current) {
        chatScrollContainerRef.current.scrollTo({
          top: chatScrollContainerRef.current.scrollHeight,
          behavior: "smooth",
        });
      }
    });
  }, [messages, isExecuting]);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputText.trim() || isExecuting) return;
    const msg = inputText.trim();
    setInputText("");
    onSendMessage(msg);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="agent-studio-pane flex flex-col h-full min-h-0 bg-[#080d1a] border border-indigo-500/20 rounded-2xl overflow-hidden shadow-xl">
      {/* Studio Header */}
      <div className="agent-studio-header p-4 px-5 border-b border-white/10 bg-slate-900/80 flex items-center justify-between flex-wrap gap-2 shrink-0">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-indigo-600/30">
            <Sparkles className="w-3.5 h-3.5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                Autonomous Sales Agent Studio
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-mono border border-emerald-500/20 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                Live Agent Core
              </span>
            </div>
            <div className="text-[11px] text-slate-400 flex items-center gap-1.5 mt-0.5 font-mono">
              <Terminal className="w-3 h-3 text-cyan-400" />
              <span>
                Model:{" "}
                <span className="text-indigo-300 font-semibold">
                  {modelName}
                </span>
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={onClearChat}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors cursor-pointer text-xs flex items-center gap-1"
              title="Clear conversation"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span className="text-[11px] hidden sm:inline">Reset</span>
            </button>
          )}
        </div>
      </div>

      {/* Quick Prompt Chips */}
      <div className="agent-quick-prompts p-2.5 px-4 bg-slate-950/70 border-b border-white/5 overflow-x-auto flex items-center gap-2 scrollbar-none shrink-0">
        <span className="text-[10px] uppercase font-bold text-slate-400 shrink-0">
          Quick Prompts:
        </span>
        {QUICK_PROMPTS.map((qp, idx) => (
          <button
            key={idx}
            onClick={() => {
              setInputText(qp.prompt);
            }}
            className="agent-quick-prompt-btn text-[11px] px-2.5 py-1 rounded-full bg-white/5 hover:bg-indigo-600/20 hover:text-indigo-300 hover:border-indigo-500/30 border border-white/10 text-slate-300 whitespace-nowrap transition-all cursor-pointer shrink-0"
          >
            {qp.label}
          </button>
        ))}
      </div>

      {/* Messages Timeline */}
      <div
        ref={chatScrollContainerRef}
        className="agent-chat-timeline flex-1 min-h-0 p-5 overflow-y-auto space-y-4"
      >
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
            <div className="agent-empty-icon w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <Bot className="w-6 h-6 text-cyan-400" />
            </div>
            <h5 className="text-sm font-bold text-white">
              Autonomous Sales Agent is Ready
            </h5>
            <p className="text-xs text-slate-400 max-w-sm leading-relaxed">
              Describe what you need in plain English. The agent will retrieve
              live CRM context, make decisions via LangGraph, and execute real
              actions or specialized workflows.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-md w-full pt-2">
              <button
                onClick={() =>
                  onSendMessage(
                    "Schedule a product demo with Sarah Chen for tomorrow at 2:00 PM",
                  )
                }
                className="agent-sample-btn p-2.5 rounded-xl bg-slate-900/80 border border-white/10 hover:border-indigo-500/40 text-left text-xs text-slate-300 transition-colors cursor-pointer group"
              >
                <div className="font-semibold text-white group-hover:text-indigo-300">
                  📅 Schedule Meeting
                </div>
                <div className="text-[10px] text-slate-500">
                  Auto-books calendar slot
                </div>
              </button>
              <button
                onClick={() =>
                  onSendMessage(
                    "Create a $220,000 deal for Acme Corp in Proposal stage",
                  )
                }
                className="agent-sample-btn p-2.5 rounded-xl bg-slate-900/80 border border-white/10 hover:border-indigo-500/40 text-left text-xs text-slate-300 transition-colors cursor-pointer group"
              >
                <div className="font-semibold text-white group-hover:text-indigo-300">
                  💼 Create Deal
                </div>
                <div className="text-[10px] text-slate-500">
                  Mutates pipeline state
                </div>
              </button>
              <button
                onClick={() =>
                  onSendMessage(
                    "Score lead Elena Rostova from HyperScale for enterprise buyer intent",
                  )
                }
                className="agent-sample-btn p-2.5 rounded-xl bg-slate-900/80 border border-white/10 hover:border-indigo-500/40 text-left text-xs text-slate-300 transition-colors cursor-pointer group"
              >
                <div className="font-semibold text-white group-hover:text-indigo-300">
                  🎯 Lead Scoring
                </div>
                <div className="text-[10px] text-slate-500">
                  Predicts buyer intent
                </div>
              </button>
              <button
                onClick={() =>
                  onSendMessage(
                    "Draft a follow-up email to Sarah Chen regarding architecture review",
                  )
                }
                className="agent-sample-btn p-2.5 rounded-xl bg-slate-900/80 border border-white/10 hover:border-indigo-500/40 text-left text-xs text-slate-300 transition-colors cursor-pointer group"
              >
                <div className="font-semibold text-white group-hover:text-indigo-300">
                  ✉️ Draft Email
                </div>
                <div className="text-[10px] text-slate-500">
                  Contextual sales outreach
                </div>
              </button>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === "user" ? "items-end" : "items-start"}`}
            >
              <div
                className={`flex items-start gap-3 max-w-[92%] ${msg.sender === "user" ? "flex-row-reverse" : ""}`}
              >
                <div
                  className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ${
                    msg.sender === "user"
                      ? "bg-indigo-600 text-white"
                      : "bg-gradient-to-tr from-cyan-600 to-indigo-600 text-white shadow-sm"
                  }`}
                >
                  {msg.sender === "user" ? (
                    <UserIcon className="w-3.5 h-3.5" />
                  ) : (
                    <Bot className="w-3.5 h-3.5" />
                  )}
                </div>

                <div className="flex flex-col space-y-2">
                  <div
                    className={`agent-message-bubble p-4 rounded-2xl text-xs leading-relaxed ${
                      msg.sender === "user"
                        ? "bg-indigo-600 text-white rounded-tr-none"
                        : "bg-slate-900/90 border border-indigo-500/20 text-slate-200 rounded-tl-none shadow-md"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{msg.text}</div>

                    {/* Rich Interactive Action Result Cards */}
                    {(() => {
                      const toolList =
                        msg.response?.tool_results &&
                        msg.response.tool_results.length > 0
                          ? msg.response.tool_results
                          : msg.response?.tool_result
                            ? [msg.response.tool_result]
                            : [];
                      return toolList.map((tr, idx) =>
                        tr && tr.success ? (
                          <div
                            key={`action-${idx}`}
                            className="mt-3 pt-3 border-t border-white/10"
                          >
                            <ActionResultCard toolResult={tr} />
                          </div>
                        ) : null,
                      );
                    })()}

                    {/* Specialized Sub-Agent Output Cards */}
                    {(() => {
                      const subList =
                        msg.response?.subagent_results &&
                        msg.response.subagent_results.length > 0
                          ? msg.response.subagent_results
                          : msg.response?.subagent_result
                            ? [msg.response.subagent_result]
                            : [];
                      return subList.map((sr, idx) =>
                        sr ? (
                          <div
                            key={`subagent-${idx}`}
                            className="mt-3 pt-3 border-t border-white/10"
                          >
                            <SubagentResultCard
                              subagent={msg.response?.target_subagent || ""}
                              data={sr}
                            />
                          </div>
                        ) : null,
                      );
                    })()}
                  </div>

                  {/* Metadata and Inspect Trigger */}
                  {msg.response && (
                    <div className="flex items-center gap-3 px-1 text-[10px] text-slate-400 font-mono">
                      <span>{msg.timestamp}</span>
                      <span>·</span>
                      <span className="text-cyan-400">
                        {msg.response.telemetry.total_latency_ms || 350}ms
                      </span>
                      <span>·</span>
                      <span className="text-emerald-400">
                        {Math.round(
                          (msg.response.confidence_score || 0.9) * 100,
                        )}
                        % confidence
                      </span>
                      {onSelectGraphRun && (
                        <>
                          <span>·</span>
                          <button
                            onClick={() => onSelectGraphRun(msg.response!)}
                            className="text-indigo-400 hover:text-indigo-300 underline cursor-pointer"
                          >
                            Inspect Flow ({msg.response.graph_steps.length}{" "}
                            nodes)
                          </button>
                        </>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}

        {isExecuting && (
          <div className="flex items-start gap-3">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center text-white shrink-0 shadow-sm animate-pulse">
              <Bot className="w-3.5 h-3.5" />
            </div>
            <div className="agent-reasoning-banner p-3.5 rounded-2xl rounded-tl-none bg-slate-900/90 border border-cyan-500/30 text-xs text-cyan-300 flex items-center gap-2">
              <RotateCw className="w-3.5 h-3.5 animate-spin text-cyan-400" />
              <span>Agent reasoning through LangGraph nodes...</span>
            </div>
          </div>
        )}
      </div>

      {/* Chat Input Bar */}
      <form
        onSubmit={handleSubmit}
        className="agent-input-bar p-3.5 px-4 bg-slate-900/90 border-t border-white/10 flex items-center gap-2 shrink-0"
      >
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Instruct the agent (e.g., 'Schedule meeting with Sarah Chen' or 'Score Elena Rostova')..."
          rows={1}
          className="agent-input-textarea flex-1 bg-slate-950/80 border border-white/10 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none font-sans"
        />
        <button
          type="submit"
          disabled={!inputText.trim() || isExecuting}
          className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white text-xs font-bold shadow-md shadow-indigo-600/30 transition-all cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed shrink-0 flex items-center gap-1.5 active:scale-95"
        >
          {isExecuting ? (
            <RotateCw className="w-3.5 h-3.5 animate-spin" />
          ) : (
            <>
              <span>Send</span>
              <Send className="w-3.5 h-3.5" />
            </>
          )}
        </button>
      </form>
    </div>
  );
}

// ─── Embedded Action Result Card ────────────────────────────────────────────

function ActionResultCard({ toolResult }: { toolResult: Record<string, any> }) {
  const action = toolResult.action;

  if (action === "schedule_meeting" && toolResult.event) {
    const e = toolResult.event;
    return (
      <div className="agent-action-card agent-action-meeting p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/30 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center shrink-0">
            <Calendar className="w-4 h-4" />
          </div>
          <div>
            <div className="font-semibold text-white text-[11px]">
              {e.title}
            </div>
            <div className="text-[10px] text-slate-400">
              {new Date(e.start_time).toLocaleString()} ·{" "}
              {e.location || "Google Meet"}
            </div>
          </div>
        </div>
        <Link
          href="/calendar"
          className="px-2.5 py-1 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white text-[10px] font-semibold flex items-center gap-1 transition-colors shrink-0"
        >
          <span>View Calendar</span>
          <ExternalLink className="w-2.5 h-2.5" />
        </Link>
      </div>
    );
  }

  if (
    (action === "create_deal" || action === "update_deal") &&
    toolResult.deal
  ) {
    const d = toolResult.deal;
    return (
      <div className="agent-action-card agent-action-deal p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
            <Award className="w-4 h-4" />
          </div>
          <div>
            <div className="font-semibold text-white text-[11px]">
              {d.title}
            </div>
            <div className="text-[10px] text-slate-400">
              ${Number(d.value).toLocaleString()} · {d.company} · Stage:{" "}
              <span className="text-emerald-400 uppercase font-mono">
                {d.stage}
              </span>
            </div>
          </div>
        </div>
        <Link
          href="/deals"
          className="px-2.5 py-1 rounded-lg bg-emerald-600/30 hover:bg-emerald-600 text-emerald-300 hover:text-white text-[10px] font-semibold flex items-center gap-1 transition-colors shrink-0"
        >
          <span>View Deals</span>
          <ExternalLink className="w-2.5 h-2.5" />
        </Link>
      </div>
    );
  }

  if (
    (action === "create_contact" || action === "update_contact") &&
    toolResult.contact
  ) {
    const c = toolResult.contact;
    return (
      <div className="agent-action-card agent-action-contact p-3 rounded-xl bg-blue-950/40 border border-blue-500/30 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0">
            <Users className="w-4 h-4" />
          </div>
          <div>
            <div className="font-semibold text-white text-[11px]">{c.name}</div>
            <div className="text-[10px] text-slate-400">
              {c.company || "Contact"} · {c.email} · Status:{" "}
              <span className="text-cyan-400 font-mono">
                {c.lead_status || "New"}
              </span>
            </div>
          </div>
        </div>
        <Link
          href="/contacts"
          className="px-2.5 py-1 rounded-lg bg-blue-600/30 hover:bg-blue-600 text-blue-300 hover:text-white text-[10px] font-semibold flex items-center gap-1 transition-colors shrink-0"
        >
          <span>View Contacts</span>
          <ExternalLink className="w-2.5 h-2.5" />
        </Link>
      </div>
    );
  }

  if (action === "create_campaign" && toolResult.campaign) {
    const cmp = toolResult.campaign;
    return (
      <div className="agent-action-card agent-action-campaign p-3 rounded-xl bg-pink-950/40 border border-pink-500/30 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-pink-500/20 text-pink-400 flex items-center justify-center shrink-0">
            <Megaphone className="w-4 h-4" />
          </div>
          <div>
            <div className="font-semibold text-white text-[11px]">
              {cmp.name}
            </div>
            <div className="text-[10px] text-slate-400">
              Subject: {cmp.subject} · Status:{" "}
              <span className="text-pink-400 font-mono">{cmp.status}</span>
            </div>
          </div>
        </div>
        <Link
          href="/campaigns"
          className="px-2.5 py-1 rounded-lg bg-pink-600/30 hover:bg-pink-600 text-pink-300 hover:text-white text-[10px] font-semibold flex items-center gap-1 transition-colors shrink-0"
        >
          <span>View Campaigns</span>
          <ExternalLink className="w-2.5 h-2.5" />
        </Link>
      </div>
    );
  }

  return null;
}

// ─── Sub-Agent Result Widget ───────────────────────────────────────────────

function SubagentResultCard({
  subagent,
  data,
}: {
  subagent: string;
  data: Record<string, any>;
}) {
  const [copied, setCopied] = useState(false);

  // Email Drafter Card
  if (data.body && (data.subject || data.recipient)) {
    const handleCopy = () => {
      navigator.clipboard.writeText(`Subject: ${data.subject}\n\n${data.body}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    };

    const dispatch = data.dispatch_status;

    return (
      <div className="agent-subagent-card agent-subagent-email p-3 rounded-xl bg-purple-950/40 border border-purple-500/30 space-y-2.5">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase font-bold text-purple-300 flex items-center gap-1.5">
            <Mail className="w-3.5 h-3.5 text-purple-400" />
            <span>Personalized Outreach Email</span>
            {data.email_address && (
              <span className="text-purple-300/80 font-mono font-normal">
                ({data.email_address})
              </span>
            )}
          </span>
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 text-[10px] px-2 py-0.5 rounded bg-white/10 hover:bg-white/20 text-white cursor-pointer transition-colors"
          >
            {copied ? (
              <Check className="w-3 h-3 text-emerald-400" />
            ) : (
              <Copy className="w-3 h-3" />
            )}
            <span>{copied ? "Copied" : "Copy Email"}</span>
          </button>
        </div>

        {/* Dispatch & Delivery Badge */}
        {dispatch && (
          <div
            className={`px-2.5 py-1.5 rounded-lg text-[10px] flex items-center justify-between gap-2 ${
              dispatch.sent_live
                ? "bg-emerald-950/60 border border-emerald-500/30 text-emerald-300"
                : "bg-slate-950/70 border border-indigo-500/20 text-slate-400"
            }`}
          >
            <span className="flex items-center gap-1.5 leading-snug">
              <span>
                {dispatch.sent_live
                  ? "🚀 Live Dispatch:"
                  : "📥 Activity Logged:"}
              </span>
              <span
                className={
                  dispatch.sent_live
                    ? "text-emerald-200 font-medium"
                    : "text-slate-300"
                }
              >
                {dispatch.delivery_status}
              </span>
            </span>
            {dispatch.sent_live && (
              <span className="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold uppercase text-[9px] shrink-0">
                SENT
              </span>
            )}
          </div>
        )}

        <div className="text-[11px] font-semibold text-white">
          Subject: <span className="text-purple-200">{data.subject}</span>
        </div>
        <div className="text-[10px] text-slate-300 whitespace-pre-wrap p-2.5 rounded-lg bg-slate-950/60 border border-white/5 font-sans leading-relaxed">
          {data.body}
        </div>
      </div>
    );
  }

  // Lead Scoring Widget
  if (data.score !== undefined && data.factors) {
    return (
      <div className="agent-subagent-card agent-subagent-lead p-3 rounded-xl bg-indigo-950/40 border border-indigo-500/30 flex items-center justify-between gap-4">
        <div>
          <span className="text-[10px] uppercase font-bold text-indigo-300 flex items-center gap-1 mb-1">
            <Zap className="w-3 h-3 text-cyan-400" />
            Buyer Intent Rating
          </span>
          <div className="text-xs text-white font-semibold">
            {data.lead_name || "Prospect"} ({data.company || "Enterprise"})
          </div>
          <div className="text-[10px] text-slate-400 mt-0.5">
            {data.recommendation}
          </div>
        </div>

        <div className="flex flex-col items-center justify-center px-3 py-1.5 rounded-xl bg-indigo-600/20 border border-indigo-500/40 shrink-0">
          <div className="text-lg font-black text-cyan-300">{data.score}</div>
          <span className="text-[9px] uppercase font-bold text-indigo-300">
            {data.tier || "HOT"}
          </span>
        </div>
      </div>
    );
  }

  // Churn Sentinel Widget
  if (data.at_risk_accounts || data.total_arr_at_risk) {
    return (
      <div className="agent-subagent-card agent-subagent-churn p-3 rounded-xl bg-rose-950/40 border border-rose-500/30 space-y-1.5">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase font-bold text-rose-300 flex items-center gap-1">
            <ShieldAlert className="w-3 h-3" />
            Account Retention Risk
          </span>
          <span className="text-[10px] font-mono text-rose-300">
            ARR at Risk: ${Number(data.total_arr_at_risk || 0).toLocaleString()}
          </span>
        </div>
        {data.recommended_retention_playbook && (
          <ul className="text-[10px] text-slate-300 space-y-1 list-disc pl-4">
            {data.recommended_retention_playbook
              .slice(0, 2)
              .map((p: string, i: number) => (
                <li key={i}>{p}</li>
              ))}
          </ul>
        )}
      </div>
    );
  }

  return null;
}
