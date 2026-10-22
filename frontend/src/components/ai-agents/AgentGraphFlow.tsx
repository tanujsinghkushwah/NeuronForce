"use client";

import React, { useState } from "react";
import {
  Sparkles,
  Database,
  GitFork,
  Zap,
  Mail,
  Award,
  ShieldAlert,
  FileText,
  Calendar,
  Briefcase,
  Users,
  Megaphone,
  CheckCircle2,
  Clock,
  RotateCw,
  Layers,
  ArrowDown,
} from "lucide-react";
import { GraphNodeStep } from "../../types/crm";
import NodeDetailModal from "./NodeDetailModal";

interface AgentGraphFlowProps {
  steps: GraphNodeStep[];
  isExecuting: boolean;
  activeNodeId?: string | null;
  targetSubagent?: string | null;
  actionType?: string | null;
}

export default function AgentGraphFlow({
  steps,
  isExecuting,
  activeNodeId,
  targetSubagent,
  actionType,
}: AgentGraphFlowProps) {
  const [selectedStep, setSelectedStep] = useState<GraphNodeStep | null>(null);

  // Helper to find step info for a node
  const getStep = (nodeId: string): GraphNodeStep | undefined => {
    return steps.find((s) => s.node === nodeId || s.node.includes(nodeId));
  };

  const PIPELINE_ORDER = [
    "prompt_ingestion",
    "context_retrieval",
    "intent_router",
    "synthesizer",
  ];

  const getNodeState = (
    nodeId: string,
  ): "idle" | "running" | "completed" | "skipped" => {
    // 1. If currently executing, prioritize live execution state
    if (isExecuting) {
      if (activeNodeId === nodeId) return "running";
      if (
        nodeId.startsWith("subagent_") &&
        targetSubagent &&
        nodeId.includes(targetSubagent)
      ) {
        return "running";
      }
      if (
        nodeId.startsWith("action_") &&
        actionType &&
        nodeId.includes(actionType)
      ) {
        return "running";
      }
      // If the execution has progressed past this stage in the linear pipeline
      const currentIdx = PIPELINE_ORDER.indexOf(activeNodeId || "");
      const thisIdx = PIPELINE_ORDER.indexOf(nodeId);
      if (currentIdx > -1 && thisIdx > -1 && thisIdx < currentIdx) {
        return "completed";
      }
      return "idle";
    }

    // 2. Real completed step returned from backend or past session inspection
    const step = getStep(nodeId);
    if (step) return "completed";

    return "idle";
  };

  const handleNodeClick = (nodeId: string, fallbackLabel: string) => {
    const step = getStep(nodeId);
    if (step) {
      setSelectedStep(step);
    } else {
      setSelectedStep({
        node: nodeId,
        status: getNodeState(nodeId),
        label: fallbackLabel,
        latency_ms: 0,
        summary: `${fallbackLabel} is ready in the workflow. It executes automatically when relevant prompts are received.`,
        data: { step: fallbackLabel, status: "Ready" },
      });
    }
  };

  const isAnySubagentActive = [
    "subagent_lead_scoring",
    "subagent_email_draft",
    "subagent_deal_risk",
    "subagent_churn_prediction",
    "subagent_meeting_summary",
  ].some((id) => getNodeState(id) !== "idle");

  const isAnyActionActive = [
    "action_schedule_meeting",
    "action_create_deal",
    "action_create_contact",
    "action_create_campaign",
  ].some((id) => getNodeState(id) !== "idle");

  return (
    <div className="agent-graph-pane flex flex-col h-full min-h-0 bg-[#080d1a] border border-indigo-500/20 rounded-2xl overflow-hidden shadow-xl">
      {/* Top Header */}
      <div className="agent-graph-header p-3 px-4 border-b border-white/10 bg-slate-900/80 flex items-center justify-between flex-wrap gap-2 shrink-0">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-cyan-400">
            <GitFork className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="text-xs font-bold text-white tracking-wide">
                Agent Reasoning Workflow
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-medium border border-emerald-500/30">
                Live Flow
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Visual tracking of autonomous AI decisions &amp; CRM actions
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {isExecuting ? (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-cyan-500/15 border border-cyan-500/30 text-cyan-300 text-[11px] font-medium">
              <RotateCw className="w-3 h-3 animate-spin text-cyan-400" />
              <span>Analyzing...</span>
            </div>
          ) : steps.length > 0 ? (
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[11px] font-medium">
              <CheckCircle2 className="w-3 h-3" />
              <span>{steps.length} Steps Completed</span>
            </div>
          ) : (
            <div className="text-[11px] text-slate-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-500" />
              <span>Ready for request</span>
            </div>
          )}
        </div>
      </div>

      {/* Main Graph Flow Canvas - Zero scroll layout: fits completely in single view */}
      <div className="agent-graph-canvas flex-1 min-h-0 p-3 flex flex-col items-center overflow-hidden relative">
        {/* Step 1: Request Understanding */}
        <NodeCard
          stepNumber="1"
          title="Request Understanding"
          subtitle="Interpreting prompt goals, intent & target details"
          icon={Sparkles}
          color="from-blue-600 to-indigo-600"
          state={getNodeState("prompt_ingestion")}
          step={getStep("prompt_ingestion")}
          onClick={() =>
            handleNodeClick("prompt_ingestion", "Request Understanding")
          }
        />
        <ConnectorLine
          active={
            getNodeState("prompt_ingestion") === "completed" ||
            activeNodeId === "prompt_ingestion" ||
            activeNodeId === "context_retrieval"
          }
        />

        {/* Step 2: CRM Data Retrieval */}
        <NodeCard
          stepNumber="2"
          title="CRM Data Gathering"
          subtitle="Checking customer, deal & calendar records"
          icon={Database}
          color="from-cyan-600 to-blue-600"
          state={getNodeState("context_retrieval")}
          step={getStep("context_retrieval")}
          badgeText={
            getStep("context_retrieval")?.data?.matching_contacts_count !==
            undefined
              ? `${getStep("context_retrieval")?.data?.matching_contacts_count} Contacts · ${getStep("context_retrieval")?.data?.matching_deals_count} Deals`
              : "Live CRM Sync"
          }
          onClick={() =>
            handleNodeClick("context_retrieval", "CRM Data Gathering")
          }
        />
        <ConnectorLine
          active={
            getNodeState("context_retrieval") === "completed" ||
            activeNodeId === "context_retrieval" ||
            activeNodeId === "intent_router"
          }
        />

        {/* Step 3: Decision Router */}
        <NodeCard
          stepNumber="3"
          title="Intelligent Decision Router"
          subtitle="Directing to the best specialized agent or CRM tool"
          icon={GitFork}
          color="from-purple-600 to-indigo-600"
          state={getNodeState("intent_router")}
          step={getStep("intent_router")}
          badgeText={
            targetSubagent
              ? `Agent: ${targetSubagent.replace("_", " ").toUpperCase()}`
              : actionType
                ? `Action: ${actionType.replace("_", " ").toUpperCase()}`
                : "Routing"
          }
          onClick={() => handleNodeClick("intent_router", "Decision Router")}
        />
        <ConnectorLine
          active={
            getNodeState("intent_router") === "completed" ||
            activeNodeId === "intent_router" ||
            isAnySubagentActive ||
            isAnyActionActive
          }
        />

        {/* Step 4: Compact Dual-Branch Container (Specialized Agents vs CRM Actions) */}
        <div className="grid grid-cols-2 gap-3 max-w-xl mx-auto w-full shrink-0">
          {/* Branch A: Specialized Agents */}
          <div
            className={`agent-branch-box agent-branch-specialized p-2.5 rounded-xl transition-all border ${
              isAnySubagentActive
                ? "bg-indigo-950/40 border-indigo-400/50 shadow-md shadow-indigo-500/10"
                : "bg-slate-900/40 border-white/5"
            } flex flex-col space-y-1.5`}
          >
            <div className="flex items-center justify-between px-1 pb-1 border-b border-white/5">
              <span className="text-[10px] font-bold tracking-wider text-indigo-300 flex items-center gap-1">
                <Layers className="w-3 h-3 text-indigo-400" />
                Specialized Agents
              </span>
              <span className="text-[9px] text-slate-400">5 Ready</span>
            </div>

            <div className="space-y-1">
              <MicroAgentNode
                nodeId="subagent_lead_scoring"
                name="Lead Scoring"
                icon={Zap}
                color="text-indigo-400"
                state={getNodeState("subagent_lead_scoring")}
                step={getStep("subagent_lead_scoring")}
                onClick={() =>
                  handleNodeClick("subagent_lead_scoring", "Lead Scoring Agent")
                }
              />

              <MicroAgentNode
                nodeId="subagent_email_draft"
                name="Email Drafter"
                icon={Mail}
                color="text-purple-400"
                state={getNodeState("subagent_email_draft")}
                step={getStep("subagent_email_draft")}
                onClick={() =>
                  handleNodeClick("subagent_email_draft", "Email Drafter")
                }
              />

              <MicroAgentNode
                nodeId="subagent_deal_risk"
                name="Deal Risk Analysis"
                icon={Award}
                color="text-cyan-400"
                state={getNodeState("subagent_deal_risk")}
                step={getStep("subagent_deal_risk")}
                onClick={() =>
                  handleNodeClick("subagent_deal_risk", "Deal Risk Assessment")
                }
              />

              <MicroAgentNode
                nodeId="subagent_churn_prediction"
                name="Churn Sentinel"
                icon={ShieldAlert}
                color="text-rose-400"
                state={getNodeState("subagent_churn_prediction")}
                step={getStep("subagent_churn_prediction")}
                onClick={() =>
                  handleNodeClick("subagent_churn_prediction", "Churn Sentinel")
                }
              />

              <MicroAgentNode
                nodeId="subagent_meeting_summary"
                name="Meeting Summarizer"
                icon={FileText}
                color="text-amber-400"
                state={getNodeState("subagent_meeting_summary")}
                step={getStep("subagent_meeting_summary")}
                onClick={() =>
                  handleNodeClick(
                    "subagent_meeting_summary",
                    "Meeting Summarizer",
                  )
                }
              />
            </div>
          </div>

          {/* Branch B: CRM Action Tools */}
          <div
            className={`agent-branch-box agent-branch-actions p-2.5 rounded-xl transition-all border ${
              isAnyActionActive
                ? "bg-cyan-950/40 border-cyan-400/50 shadow-md shadow-cyan-500/10"
                : "bg-slate-900/40 border-white/5"
            } flex flex-col space-y-1.5`}
          >
            <div className="flex items-center justify-between px-1 pb-1 border-b border-white/5">
              <span className="text-[10px] font-bold tracking-wider text-cyan-300 flex items-center gap-1">
                <Briefcase className="w-3 h-3 text-cyan-400" />
                Direct CRM Actions
              </span>
              <span className="text-[9px] text-slate-400">4 Tools</span>
            </div>

            <div className="space-y-1">
              <MicroAgentNode
                nodeId="action_schedule_meeting"
                name="Calendar Scheduler"
                icon={Calendar}
                color="text-emerald-400"
                state={getNodeState("action_schedule_meeting")}
                step={getStep("action_schedule_meeting")}
                onClick={() =>
                  handleNodeClick(
                    "action_schedule_meeting",
                    "Calendar Scheduler",
                  )
                }
              />

              <MicroAgentNode
                nodeId="action_create_deal"
                name="Pipeline Deals"
                icon={Award}
                color="text-indigo-400"
                state={
                  getNodeState("action_create_deal") !== "idle"
                    ? getNodeState("action_create_deal")
                    : getNodeState("action_update_deal")
                }
                step={
                  getStep("action_create_deal") || getStep("action_update_deal")
                }
                onClick={() =>
                  handleNodeClick("action_create_deal", "Pipeline Deals")
                }
              />

              <MicroAgentNode
                nodeId="action_create_contact"
                name="Contact &amp; Leads"
                icon={Users}
                color="text-blue-400"
                state={
                  getNodeState("action_create_contact") !== "idle"
                    ? getNodeState("action_create_contact")
                    : getNodeState("action_update_contact")
                }
                step={
                  getStep("action_create_contact") ||
                  getStep("action_update_contact")
                }
                onClick={() =>
                  handleNodeClick("action_create_contact", "Contact Manager")
                }
              />

              <MicroAgentNode
                nodeId="action_create_campaign"
                name="Marketing Campaigns"
                icon={Megaphone}
                color="text-pink-400"
                state={getNodeState("action_create_campaign")}
                step={getStep("action_create_campaign")}
                onClick={() =>
                  handleNodeClick(
                    "action_create_campaign",
                    "Marketing Campaigns",
                  )
                }
              />

              <div className="py-1 px-2 rounded-lg bg-white/[0.02] border border-white/5 text-[10px] text-slate-400 flex items-center justify-center gap-1">
                <span>Direct CRM Sync</span>
              </div>
            </div>
          </div>
        </div>

        {/* Step 5: Outcome & CRM Sync */}
        <ConnectorLine
          active={
            getNodeState("synthesizer") === "completed" ||
            activeNodeId === "synthesizer"
          }
        />
        <NodeCard
          stepNumber="4"
          title="Outcome &amp; Database Sync"
          subtitle="Finalizing response &amp; synchronizing CRM state"
          icon={CheckCircle2}
          color="from-emerald-600 to-teal-500"
          state={getNodeState("synthesizer")}
          step={getStep("synthesizer")}
          onClick={() =>
            handleNodeClick("synthesizer", "Outcome & Database Sync")
          }
        />
      </div>

      {/* Node Inspector Modal */}
      {selectedStep && (
        <NodeDetailModal
          step={selectedStep}
          onClose={() => setSelectedStep(null)}
        />
      )}
    </div>
  );
}

// ─── Sub-Components ─────────────────────────────────────────────────────────

function NodeCard({
  stepNumber,
  title,
  subtitle,
  icon: Icon,
  color,
  state,
  step,
  badgeText,
  onClick,
}: {
  stepNumber: string;
  title: string;
  subtitle: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  state: "idle" | "running" | "completed" | "skipped";
  step?: GraphNodeStep;
  badgeText?: string;
  onClick: () => void;
}) {
  const isRunning = state === "running";
  const isCompleted = state === "completed";

  return (
    <div
      onClick={onClick}
      className={`agent-node-card w-full max-w-md p-2.5 px-3 rounded-xl border transition-all cursor-pointer relative group shrink-0 ${
        isRunning
          ? "bg-indigo-950/70 border-cyan-400 shadow-lg shadow-cyan-500/20 ring-1 ring-cyan-400"
          : isCompleted
            ? "bg-slate-900/90 border-emerald-500/50 hover:border-emerald-400 shadow-sm shadow-emerald-500/10"
            : "bg-slate-900/60 border-white/10 hover:border-white/20 hover:bg-slate-900/90"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div
            className={`w-8 h-8 rounded-lg bg-gradient-to-tr ${color} flex items-center justify-center text-white shadow-md relative shrink-0`}
          >
            <Icon className="w-4 h-4" />
            {isRunning && (
              <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-cyan-500"></span>
              </span>
            )}
          </div>

          <div>
            <div className="flex items-center gap-1.5 flex-wrap">
              <span className="text-[10px] px-1.5 py-0.2 rounded bg-white/5 border border-white/10 text-slate-300 font-medium">
                Step {stepNumber}
              </span>
              <h5 className="text-xs font-bold text-white group-hover:text-cyan-300 transition-colors">
                {title}
              </h5>
              {badgeText && (
                <span className="text-[9px] px-1.5 py-0.2 rounded bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 font-medium">
                  {badgeText}
                </span>
              )}
            </div>
            <p className="text-[11px] text-slate-400 line-clamp-1">
              {subtitle}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5 shrink-0">
          {isCompleted ? (
            <div className="flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
              <CheckCircle2 className="w-3 h-3" />
              <span>Done</span>
            </div>
          ) : isRunning ? (
            <div className="flex items-center gap-1 text-[11px] font-medium text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded-md border border-cyan-500/30">
              <RotateCw className="w-3 h-3 animate-spin" />
              <span>Active</span>
            </div>
          ) : (
            <span className="text-[10px] text-slate-500 px-1.5">Ready</span>
          )}
        </div>
      </div>
    </div>
  );
}

function MicroAgentNode({
  nodeId,
  name,
  icon: Icon,
  color,
  state,
  step,
  onClick,
}: {
  nodeId: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  state: "idle" | "running" | "completed" | "skipped";
  step?: GraphNodeStep;
  onClick: () => void;
}) {
  const isRunning = state === "running";
  const isCompleted = state === "completed";

  return (
    <div
      onClick={onClick}
      className={`agent-micro-node py-1 px-2.5 rounded-lg border text-xs flex items-center justify-between transition-all cursor-pointer ${
        isRunning
          ? "bg-indigo-950/90 border-cyan-400 shadow-sm shadow-cyan-500/20 ring-1 ring-cyan-400 text-white"
          : isCompleted
            ? "bg-slate-900 border-emerald-500/50 text-white font-medium"
            : "bg-slate-900/50 border-white/5 hover:border-white/10 text-slate-400 hover:text-white"
      }`}
    >
      <div className="flex items-center gap-1.5 truncate pr-1">
        <Icon className={`w-3.5 h-3.5 shrink-0 ${color}`} />
        <span className="text-[11px] truncate">{name}</span>
      </div>

      <div className="shrink-0">
        {isCompleted ? (
          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
        ) : isRunning ? (
          <RotateCw className="w-3 h-3 animate-spin text-cyan-400" />
        ) : (
          <span className="w-1.5 h-1.5 rounded-full bg-slate-700 block" />
        )}
      </div>
    </div>
  );
}

function ConnectorLine({ active }: { active: boolean }) {
  return (
    <div className="agent-connector-line flex-1 w-full min-h-[16px] flex flex-col items-center relative select-none">
      {/* Continuous connecting stem spanning from the bottom of top container to the top of bottom container */}
      <div
        className={`agent-connector-stem w-[2px] h-full relative transition-all duration-300 ${
          active
            ? "bg-cyan-400 shadow-[0_0_8px_rgba(6,182,212,0.7)]"
            : "bg-slate-700/80"
        }`}
      >
        {active && (
          <span className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
        )}
      </div>

      {/* Directed chevron arrow head touching the destination container */}
      <div className="agent-connector-arrow absolute -bottom-1 left-1/2 -translate-x-1/2 flex items-center justify-center pointer-events-none z-10">
        <svg
          className={`w-3.5 h-2.5 transition-colors duration-300 ${
            active
              ? "text-cyan-400 drop-shadow-[0_0_6px_rgba(6,182,212,0.8)]"
              : "text-slate-500"
          }`}
          viewBox="0 0 14 10"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M2 2 L7 7.5 L12 2"
            stroke="currentColor"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
    </div>
  );
}
