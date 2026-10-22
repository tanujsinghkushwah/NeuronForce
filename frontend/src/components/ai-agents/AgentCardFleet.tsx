'use client';

import React from 'react';
import {
  Zap,
  Mail,
  Award,
  ShieldAlert,
  FileText,
  TrendingUp,
  LifeBuoy,
  Megaphone,
  ChevronRight,
  Clock,
  Sparkles,
  Lock
} from 'lucide-react';

export interface AgentCardItem {
  id: string;
  name: string;
  category: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  costEstimate: string;
  latencyEstimate: string;
  color: string;
  isActive: boolean;
  samplePrompt: string;
}

export const FLEET_AGENTS: AgentCardItem[] = [
  // ─── 5 Active Implemented Agent Workflows ─────────────────────────────────
  {
    id: 'lead_scoring',
    name: 'Lead Scoring Agent',
    category: 'Sales Automation',
    description: 'Predicts buyer intent using multi-factor signals (engagement, ICP alignment, tech stack).',
    icon: Zap,
    costEstimate: '~$0.002',
    latencyEstimate: '~250ms',
    color: 'from-indigo-600 to-blue-500',
    isActive: true,
    samplePrompt: 'Score lead Elena Rostova from HyperScale for enterprise buyer intent'
  },
  {
    id: 'email_draft',
    name: 'Personalized Email Drafter',
    category: 'Content Generation',
    description: 'Generates context-aware, hyper-personalized sales follow-ups addressing known buyer objections.',
    icon: Mail,
    costEstimate: '~$0.008',
    latencyEstimate: '~1200ms',
    color: 'from-purple-600 to-indigo-500',
    isActive: true,
    samplePrompt: 'Draft a follow-up email to Sarah Chen regarding architecture review'
  },
  {
    id: 'deal_risk',
    name: 'Deal Risk & Win Probability',
    category: 'Revenue Intelligence',
    description: 'Detects competitor undercutting, budget freezes, and missing champions across deal records.',
    icon: Award,
    costEstimate: '~$0.015',
    latencyEstimate: '~1800ms',
    color: 'from-cyan-600 to-blue-600',
    isActive: true,
    samplePrompt: 'Analyze deal risk and win probability for TechCorp Enterprise Platform License'
  },
  {
    id: 'churn_prediction',
    name: 'Customer Churn Sentinel',
    category: 'Retention Intelligence',
    description: 'Identifies enterprise accounts exhibiting usage drop-offs and recommends retention interventions.',
    icon: ShieldAlert,
    costEstimate: '~$0.025',
    latencyEstimate: '~1500ms',
    color: 'from-rose-600 to-amber-500',
    isActive: true,
    samplePrompt: 'Identify enterprise accounts with elevated churn risk'
  },
  {
    id: 'meeting_summary',
    name: 'Executive Meeting Summarizer',
    category: 'Meeting Intelligence',
    description: 'Extracts action items, timeline commitments, sentiment, and CRM deal updates from meeting notes.',
    icon: FileText,
    costEstimate: '~$0.012',
    latencyEstimate: '~1100ms',
    color: 'from-amber-600 to-orange-500',
    isActive: true,
    samplePrompt: 'Summarize meeting notes and action items for Stark Industries review'
  },

  // ─── Coming Soon Workflows (Reduced Opacity) ──────────────────────────────
  {
    id: 'forecast',
    name: 'Pipeline Revenue Forecaster',
    category: 'Executive Forecasting',
    description: 'Runs ensemble Bayesian forecast calculations with risk-adjusted confidence intervals.',
    icon: TrendingUp,
    costEstimate: '~$0.045',
    latencyEstimate: '~2400ms',
    color: 'from-emerald-600 to-teal-500',
    isActive: false,
    samplePrompt: 'Forecast Q4 revenue trajectory'
  },
  {
    id: 'ticket_triage',
    name: 'Service Cloud Triage Agent',
    category: 'Service Automation',
    description: 'Autonomous case classification, SLA urgency prediction, customer sentiment, and rapid response drafting.',
    icon: LifeBuoy,
    costEstimate: '~$0.005',
    latencyEstimate: '~400ms',
    color: 'from-blue-600 to-cyan-500',
    isActive: false,
    samplePrompt: 'Triage customer support cases'
  },
  {
    id: 'campaign_optimize',
    name: 'Marketing Campaign Optimizer',
    category: 'Marketing Intelligence',
    description: 'Predicts email open & click-through rates, scores subject line hooks, and suggests high-converting A/B variants.',
    icon: Megaphone,
    costEstimate: '~$0.006',
    latencyEstimate: '~500ms',
    color: 'from-pink-600 to-rose-500',
    isActive: false,
    samplePrompt: 'Optimize campaign open rates'
  }
];

interface AgentCardFleetProps {
  onSelectAgentPrompt: (prompt: string) => void;
}

export default function AgentCardFleet({ onSelectAgentPrompt }: AgentCardFleetProps) {
  const activeCount = FLEET_AGENTS.filter(a => a.isActive).length;
  const comingSoonCount = FLEET_AGENTS.filter(a => !a.isActive).length;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
            <span>Autonomous Agent Fleet</span>
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 font-semibold font-mono">
              {activeCount} Active · {comingSoonCount} Coming Soon
            </span>
          </h3>
          <p className="text-xs text-slate-400">
            Specialized micro-agents handling non-deterministic CRM workflows through the LangGraph studio
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {FLEET_AGENTS.map((agent) => {
          const Icon = agent.icon;

          if (!agent.isActive) {
            // Dimmed "Coming Soon" card
            return (
              <div
                key={agent.id}
                className="p-5 rounded-2xl border border-white/5 bg-slate-950/40 opacity-40 filter grayscale-[40%] cursor-not-allowed select-none flex flex-col justify-between relative overflow-hidden"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-slate-400">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-slate-400 font-medium flex items-center gap-1 font-mono">
                      <Lock className="w-2.5 h-2.5" />
                      Coming Soon
                    </span>
                  </div>

                  <h4 className="text-sm font-bold text-slate-300 mb-1.5">
                    {agent.name}
                  </h4>
                  <p className="text-xs text-slate-400 leading-relaxed mb-4 line-clamp-3">
                    {agent.description}
                  </p>
                </div>

                <div className="pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 font-mono">
                  <span>Est: {agent.costEstimate}</span>
                  <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">
                    In Development
                  </span>
                </div>
              </div>
            );
          }

          // Active 5 Agents
          return (
            <div
              key={agent.id}
              onClick={() => onSelectAgentPrompt(agent.samplePrompt)}
              className="glass-panel-interactive p-5 rounded-2xl border border-white/10 flex flex-col justify-between group cursor-pointer hover:border-indigo-500/50 hover:shadow-lg hover:shadow-indigo-500/10 transition-all duration-200"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${agent.color} flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-semibold font-mono">
                    Active
                  </span>
                </div>

                <div className="text-[10px] uppercase font-bold text-indigo-400 tracking-wider mb-1">
                  {agent.category}
                </div>
                <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors mb-1.5">
                  {agent.name}
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed mb-4">
                  {agent.description}
                </p>
              </div>

              <div className="pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400 font-mono">
                <span>{agent.latencyEstimate}</span>
                <span className="text-cyan-400 group-hover:translate-x-1 transition-transform font-sans font-medium flex items-center gap-1">
                  <span>Launch in Chat</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
