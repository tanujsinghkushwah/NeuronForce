'use client';

import React, { useState } from 'react';
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
  Info,
  Layers,
  ArrowRight
} from 'lucide-react';
import { GraphNodeStep } from '../../types/crm';
import NodeDetailModal from './NodeDetailModal';

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
  actionType
}: AgentGraphFlowProps) {
  const [selectedStep, setSelectedStep] = useState<GraphNodeStep | null>(null);

  // Helper to find step info for a node
  const getStep = (nodeId: string): GraphNodeStep | undefined => {
    return steps.find(s => s.node === nodeId || s.node.includes(nodeId));
  };

  const getNodeState = (nodeId: string): 'idle' | 'running' | 'completed' | 'skipped' => {
    const step = getStep(nodeId);
    if (step) return 'completed';
    if (isExecuting) {
      if (activeNodeId === nodeId) return 'running';
      // If we are executing and this node matches target subagent or action
      if (nodeId.startsWith('subagent_') && targetSubagent && nodeId.includes(targetSubagent)) {
        return 'running';
      }
      if (nodeId.startsWith('action_') && actionType && nodeId.includes(actionType)) {
        return 'running';
      }
    }
    return 'idle';
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
        summary: `Node '${fallbackLabel}' in LangGraph workflow. Awaiting execution trigger.`,
        data: { description: `LangGraph StateGraph node: ${nodeId}` }
      });
    }
  };

  const totalGraphLatency = steps.reduce((acc, curr) => acc + (curr.latency_ms || 0), 0);

  return (
    <div className="flex flex-col h-full min-h-0 bg-[#080d1a] border border-indigo-500/20 rounded-2xl overflow-hidden shadow-xl">
      {/* Top Telemetry Header */}
      <div className="p-3.5 px-4 border-b border-white/10 bg-slate-900/80 flex items-center justify-between flex-wrap gap-2 shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-cyan-400">
            <GitFork className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                LangGraph Multi-Agent Flow
              </h4>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 font-mono border border-cyan-500/30">
                v1.2 StateGraph
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Interactive execution topology &amp; token routing
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {isExecuting ? (
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 text-xs font-medium">
              <RotateCw className="w-3.5 h-3.5 animate-spin text-cyan-400" />
              <span>Traversing Graph...</span>
            </div>
          ) : steps.length > 0 ? (
            <div className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>{steps.length} Nodes · {totalGraphLatency}ms</span>
            </div>
          ) : (
            <div className="text-[11px] text-slate-500 font-mono">
              Graph Idle · Awaiting Prompt
            </div>
          )}
        </div>
      </div>

      {/* Main Graph Flow Canvas */}
      <div className="flex-1 min-h-0 p-4 overflow-y-auto space-y-3 relative selection:bg-indigo-500/30">
        {/* Step 1: Prompt Ingestion Node */}
        <div className="flex flex-col items-center">
          <NodeCard
            nodeId="prompt_ingestion"
            title="Prompt Ingestion"
            subtitle="Input Sanitization &amp; Token Counting"
            icon={Sparkles}
            color="from-blue-600 to-indigo-600"
            state={getNodeState('prompt_ingestion')}
            step={getStep('prompt_ingestion')}
            onClick={() => handleNodeClick('prompt_ingestion', 'Prompt Ingestion')}
          />
          <ConnectorLine active={getNodeState('prompt_ingestion') === 'completed' || isExecuting} />
        </div>

        {/* Step 2: Context Retrieval Node */}
        <div className="flex flex-col items-center">
          <NodeCard
            nodeId="context_retrieval"
            title="CRM Context Extractor"
            subtitle="Local DB SQLite Entity Queries"
            icon={Database}
            color="from-cyan-600 to-blue-600"
            state={getNodeState('context_retrieval')}
            step={getStep('context_retrieval')}
            badgeText={
              getStep('context_retrieval')?.data?.matching_contacts_count !== undefined
                ? `${getStep('context_retrieval')?.data?.matching_contacts_count} Contacts · ${getStep('context_retrieval')?.data?.matching_deals_count} Deals`
                : 'Contacts / Deals / Events'
            }
            onClick={() => handleNodeClick('context_retrieval', 'CRM Context Retrieval')}
          />
          <ConnectorLine active={getNodeState('context_retrieval') === 'completed' || isExecuting} />
        </div>

        {/* Step 3: Intent Router Node */}
        <div className="flex flex-col items-center">
          <NodeCard
            nodeId="intent_router"
            title="Orchestrator Decision Router"
            subtitle="Intent Classification &amp; Entity Parser"
            icon={GitFork}
            color="from-purple-600 to-indigo-600"
            state={getNodeState('intent_router')}
            step={getStep('intent_router')}
            badgeText={
              targetSubagent
                ? `Route: ${targetSubagent.replace('_', ' ').toUpperCase()}`
                : actionType
                ? `Action: ${actionType.replace('_', ' ').toUpperCase()}`
                : 'Dynamic Branching'
            }
            onClick={() => handleNodeClick('intent_router', 'Decision Router')}
          />
          <ConnectorLine active={getNodeState('intent_router') === 'completed' || isExecuting} />
        </div>

        {/* Step 4: Split Branches (Sub-Agents vs CRM Actions) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-xl mx-auto w-full pt-1">
          {/* Branch A: Specialized Sub-Agents Container */}
          <div className="p-3.5 rounded-2xl bg-slate-900/40 border border-indigo-500/20 flex flex-col space-y-2.5">
            <div className="flex items-center justify-between px-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-300 flex items-center gap-1.5">
                <Layers className="w-3 h-3 text-indigo-400" />
                Branch A: Specialized Agents
              </span>
              <span className="text-[10px] font-mono text-slate-400">5 Active</span>
            </div>

            <div className="space-y-2">
              <MicroAgentNode
                nodeId="subagent_lead_scoring"
                name="Lead Scoring Agent"
                icon={Zap}
                color="text-indigo-400"
                state={getNodeState('subagent_lead_scoring')}
                step={getStep('subagent_lead_scoring')}
                onClick={() => handleNodeClick('subagent_lead_scoring', 'Lead Scoring Sub-Agent')}
              />

              <MicroAgentNode
                nodeId="subagent_email_draft"
                name="Personalized Email Drafter"
                icon={Mail}
                color="text-purple-400"
                state={getNodeState('subagent_email_draft')}
                step={getStep('subagent_email_draft')}
                onClick={() => handleNodeClick('subagent_email_draft', 'Email Drafter Sub-Agent')}
              />

              <MicroAgentNode
                nodeId="subagent_deal_risk"
                name="Deal Risk &amp; Probability"
                icon={Award}
                color="text-cyan-400"
                state={getNodeState('subagent_deal_risk')}
                step={getStep('subagent_deal_risk')}
                onClick={() => handleNodeClick('subagent_deal_risk', 'Deal Risk Sub-Agent')}
              />

              <MicroAgentNode
                nodeId="subagent_churn_prediction"
                name="Customer Churn Sentinel"
                icon={ShieldAlert}
                color="text-rose-400"
                state={getNodeState('subagent_churn_prediction')}
                step={getStep('subagent_churn_prediction')}
                onClick={() => handleNodeClick('subagent_churn_prediction', 'Churn Sentinel Sub-Agent')}
              />

              <MicroAgentNode
                nodeId="subagent_meeting_summary"
                name="Executive Meeting Summarizer"
                icon={FileText}
                color="text-amber-400"
                state={getNodeState('subagent_meeting_summary')}
                step={getStep('subagent_meeting_summary')}
                onClick={() => handleNodeClick('subagent_meeting_summary', 'Meeting Summarizer Sub-Agent')}
              />
            </div>
          </div>

          {/* Branch B: CRM Action Tools Container */}
          <div className="p-3.5 rounded-2xl bg-slate-900/40 border border-cyan-500/20 flex flex-col space-y-2.5">
            <div className="flex items-center justify-between px-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-300 flex items-center gap-1.5">
                <Briefcase className="w-3 h-3 text-cyan-400" />
                Branch B: CRM Action Tools
              </span>
              <span className="text-[10px] font-mono text-slate-400">Direct DB CRUD</span>
            </div>

            <div className="space-y-2">
              <MicroAgentNode
                nodeId="action_schedule_meeting"
                name="Calendar Meeting Scheduler"
                icon={Calendar}
                color="text-emerald-400"
                state={getNodeState('action_schedule_meeting')}
                step={getStep('action_schedule_meeting')}
                onClick={() => handleNodeClick('action_schedule_meeting', 'Calendar Scheduler Tool')}
              />

              <MicroAgentNode
                nodeId="action_create_deal"
                name="Pipeline Deal Creator"
                icon={Award}
                color="text-indigo-400"
                state={getNodeState('action_create_deal') !== 'idle' ? getNodeState('action_create_deal') : getNodeState('action_update_deal')}
                step={getStep('action_create_deal') || getStep('action_update_deal')}
                onClick={() => handleNodeClick('action_create_deal', 'Deal Pipeline Tool')}
              />

              <MicroAgentNode
                nodeId="action_create_contact"
                name="Contact &amp; Lead Manager"
                icon={Users}
                color="text-blue-400"
                state={getNodeState('action_create_contact') !== 'idle' ? getNodeState('action_create_contact') : getNodeState('action_update_contact')}
                step={getStep('action_create_contact') || getStep('action_update_contact')}
                onClick={() => handleNodeClick('action_create_contact', 'Contact Manager Tool')}
              />

              <MicroAgentNode
                nodeId="action_create_campaign"
                name="Marketing Campaign Creator"
                icon={Megaphone}
                color="text-pink-400"
                state={getNodeState('action_create_campaign')}
                step={getStep('action_create_campaign')}
                onClick={() => handleNodeClick('action_create_campaign', 'Campaign Creator Tool')}
              />
            </div>
          </div>
        </div>

        {/* Step 5: Synthesizer Node */}
        <div className="flex flex-col items-center pt-2">
          <ConnectorLine active={getNodeState('synthesizer') === 'completed' || isExecuting} />
          <NodeCard
            nodeId="synthesizer"
            title="Response Synthesis &amp; Telemetry"
            subtitle="Executive Markdown + Action Confirmation"
            icon={Sparkles}
            color="from-emerald-600 to-teal-500"
            state={getNodeState('synthesizer')}
            step={getStep('synthesizer')}
            onClick={() => handleNodeClick('synthesizer', 'Response Synthesizer')}
          />
        </div>
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
  nodeId,
  title,
  subtitle,
  icon: Icon,
  color,
  state,
  step,
  badgeText,
  onClick
}: {
  nodeId: string;
  title: string;
  subtitle: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  state: 'idle' | 'running' | 'completed' | 'skipped';
  step?: GraphNodeStep;
  badgeText?: string;
  onClick: () => void;
}) {
  const isRunning = state === 'running';
  const isCompleted = state === 'completed';

  return (
    <div
      onClick={onClick}
      className={`w-full max-w-md p-3.5 rounded-xl border transition-all cursor-pointer relative group ${
        isRunning
          ? 'bg-indigo-950/60 border-cyan-400 shadow-lg shadow-cyan-500/20 ring-2 ring-cyan-400/50 scale-[1.02]'
          : isCompleted
          ? 'bg-slate-900/90 border-emerald-500/50 hover:border-emerald-400 shadow-md shadow-emerald-500/10'
          : 'bg-slate-900/60 border-white/10 hover:border-white/20 hover:bg-slate-900/90'
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`w-9 h-9 rounded-lg bg-gradient-to-tr ${color} flex items-center justify-center text-white shadow-md relative`}>
            <Icon className="w-4 h-4" />
            {isRunning && (
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
              </span>
            )}
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h5 className="text-xs font-bold text-white group-hover:text-cyan-300 transition-colors">
                {title}
              </h5>
              {badgeText && (
                <span className="text-[9px] px-1.5 py-0.2 rounded bg-white/5 border border-white/10 text-slate-300 font-mono">
                  {badgeText}
                </span>
              )}
            </div>
            <p className="text-[11px] text-slate-400 mt-0.5">{subtitle}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {step ? (
            <div className="flex items-center gap-1 text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
              <CheckCircle2 className="w-3 h-3" />
              <span>{step.latency_ms}ms</span>
            </div>
          ) : isRunning ? (
            <div className="flex items-center gap-1 text-[11px] font-mono text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded-md border border-cyan-500/30">
              <RotateCw className="w-3 h-3 animate-spin" />
              <span>active</span>
            </div>
          ) : (
            <span className="text-[10px] text-slate-500 font-mono">idle</span>
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
  onClick
}: {
  nodeId: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  state: 'idle' | 'running' | 'completed' | 'skipped';
  step?: GraphNodeStep;
  onClick: () => void;
}) {
  const isRunning = state === 'running';
  const isCompleted = state === 'completed';

  return (
    <div
      onClick={onClick}
      className={`p-2.5 px-3 rounded-xl border text-xs flex items-center justify-between transition-all cursor-pointer ${
        isRunning
          ? 'bg-indigo-950/80 border-cyan-400 shadow-md shadow-cyan-500/20 ring-1 ring-cyan-400'
          : isCompleted
          ? 'bg-slate-900 border-emerald-500/50 text-white'
          : 'bg-slate-900/50 border-white/5 hover:border-white/10 text-slate-400 hover:text-white'
      }`}
    >
      <div className="flex items-center gap-2">
        <Icon className={`w-3.5 h-3.5 ${color}`} />
        <span className="font-medium text-[11px]">{name}</span>
      </div>

      <div>
        {step ? (
          <span className="text-[10px] font-mono text-emerald-400 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" />
            <span>{step.latency_ms}ms</span>
          </span>
        ) : isRunning ? (
          <span className="text-[10px] font-mono text-cyan-400 flex items-center gap-1">
            <RotateCw className="w-3 h-3 animate-spin" />
            <span>running</span>
          </span>
        ) : (
          <span className="text-[9px] font-mono text-slate-600">standby</span>
        )}
      </div>
    </div>
  );
}

function ConnectorLine({ active }: { active: boolean }) {
  return (
    <div className="h-3.5 w-0.5 relative my-0 flex items-center justify-center shrink-0">
      <div className={`w-0.5 h-full transition-colors ${active ? 'bg-gradient-to-b from-cyan-400 to-indigo-500' : 'bg-slate-800'}`} />
      {active && (
        <span className="absolute w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400 animate-pulse" />
      )}
    </div>
  );
}
