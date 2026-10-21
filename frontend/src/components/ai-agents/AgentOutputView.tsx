'use client';

import React, { useState } from 'react';
import { AIAgentTask } from '../../types/crm';
import {
  CheckCircle2,
  Code2,
  Sparkles,
  Award,
  AlertTriangle,
  TrendingUp,
  Mail,
  FileText,
  ShieldAlert,
  ArrowRight,
  Copy,
  Check,
} from 'lucide-react';

interface AgentOutputViewProps {
  task: AIAgentTask;
}

export default function AgentOutputView({ task }: AgentOutputViewProps) {
  const [viewMode, setViewMode] = useState<'visual' | 'json'>('visual');
  const [copied, setCopied] = useState(false);

  const output = task.output_data || {};
  const isRealAI = output?._meta?.is_real_ai;
  const modelUsed = output?._meta?.model;

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(output, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-4 rounded-xl bg-slate-950/90 border border-indigo-500/40 text-xs space-y-3 animate-in fade-in duration-200 shadow-xl">
      {/* ── Telemetry Header ────────────────────────────────────────────── */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2.5 border-b border-white/10">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span className="font-bold text-white">Execution Complete</span>
          <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 font-semibold uppercase">
            {task.status}
          </span>
          {isRealAI && (
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-medium border border-indigo-500/30">
              Live OpenRouter
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-3 text-[11px] font-mono">
            <span className="text-slate-400">
              Latency: <strong className="text-white">{task.latency_ms}ms</strong>
            </span>
            <span className="text-slate-400">
              Cost: <strong className="text-emerald-400">${(task.actual_cost || 0.002).toFixed(4)}</strong>
            </span>
            <span className="text-slate-400">
              Confidence:{' '}
              <strong className="text-cyan-400">
                {Math.round((task.confidence_score || 0.92) * 100)}%
              </strong>
            </span>
          </div>

          {/* Toggle between Executive Summary and JSON */}
          <div className="flex items-center rounded-lg bg-slate-900 border border-white/10 p-0.5 text-[10px]">
            <button
              type="button"
              onClick={() => setViewMode('visual')}
              className={`px-2 py-0.5 rounded font-medium transition-colors cursor-pointer ${
                viewMode === 'visual'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Summary
            </button>
            <button
              type="button"
              onClick={() => setViewMode('json')}
              className={`px-2 py-0.5 rounded font-medium transition-colors cursor-pointer ${
                viewMode === 'json'
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              JSON
            </button>
          </div>
        </div>
      </div>

      {/* ── Content View ───────────────────────────────────────────────── */}
      {viewMode === 'visual' ? (
        <div className="space-y-3 pt-1">
          {/* Key Metric / Highlight Banner */}
          {(output.score !== undefined ||
            output.win_probability !== undefined ||
            output.churn_probability !== undefined ||
            output.predicted_revenue !== undefined) && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {output.score !== undefined && (
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-indigo-500/20">
                  <span className="text-[10px] text-slate-400 font-medium block">Lead Intent Score</span>
                  <span className="text-xl font-bold text-indigo-400 font-mono">
                    {output.score}
                    <span className="text-xs text-slate-500 font-normal">/100</span>
                  </span>
                </div>
              )}

              {output.win_probability !== undefined && (
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-emerald-500/20">
                  <span className="text-[10px] text-slate-400 font-medium block">Win Probability</span>
                  <span className="text-xl font-bold text-emerald-400 font-mono">
                    {Math.round(output.win_probability * 100)}%
                  </span>
                </div>
              )}

              {output.churn_probability !== undefined && (
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-rose-500/20">
                  <span className="text-[10px] text-slate-400 font-medium block">Churn Probability</span>
                  <span className="text-xl font-bold text-rose-400 font-mono">
                    {Math.round(output.churn_probability * 100)}%
                  </span>
                </div>
              )}

              {(output.total_revenue_at_risk !== undefined || output.revenue_at_risk !== undefined) && (
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-amber-500/20">
                  <span className="text-[10px] text-slate-400 font-medium block">ARR at Risk</span>
                  <span className="text-xl font-bold text-amber-400 font-mono">
                    ${((output.total_revenue_at_risk || output.revenue_at_risk || 0) / 1000).toFixed(0)}k
                  </span>
                </div>
              )}

              {output.predicted_revenue !== undefined && (
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-emerald-500/20">
                  <span className="text-[10px] text-slate-400 font-medium block">Forecasted Revenue</span>
                  <span className="text-xl font-bold text-emerald-400 font-mono">
                    ${(output.predicted_revenue / 1000).toFixed(0)}k
                  </span>
                </div>
              )}

              {output.priority && (
                <div className="p-2.5 rounded-lg bg-slate-900/80 border border-indigo-500/20">
                  <span className="text-[10px] text-slate-400 font-medium block">Priority Level</span>
                  <span className="text-sm font-bold text-white uppercase tracking-wider">
                    {output.priority}
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Recommendation / Key Takeaway Callout */}
          {(output.recommendation || output.recommended_next_action || output.summary || output.message) && (
            <div className="p-3 rounded-lg bg-indigo-500/[0.08] border border-indigo-500/30 flex items-start gap-2.5">
              <Sparkles className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
              <div>
                <span className="text-[11px] font-bold text-indigo-300 block mb-0.5">
                  AI Recommendation &amp; Strategic Insight
                </span>
                <p className="text-xs text-slate-200 leading-relaxed font-sans">
                  {output.recommendation ||
                    output.recommended_next_action ||
                    output.summary ||
                    output.message}
                </p>
              </div>
            </div>
          )}

          {/* Email Body Draft (if email agent) */}
          {output.subject && output.body && (
            <div className="space-y-2 p-3 rounded-lg bg-slate-900/90 border border-white/10">
              <div className="flex items-center justify-between pb-1.5 border-b border-white/10">
                <span className="font-semibold text-white">Subject: {output.subject}</span>
                <button
                  type="button"
                  onClick={() => {
                    navigator.clipboard.writeText(`${output.subject}\n\n${output.body}`);
                    setCopied(true);
                    setTimeout(() => setCopied(false), 2000);
                  }}
                  className="flex items-center gap-1 text-[11px] text-indigo-400 hover:text-indigo-300 cursor-pointer"
                >
                  {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                  {copied ? 'Copied' : 'Copy Email'}
                </button>
              </div>
              <p className="text-slate-300 text-xs whitespace-pre-line leading-relaxed font-sans">
                {output.body}
              </p>
            </div>
          )}

          {/* Bullet Factors / Drivers / Signals */}
          {(output.factors ||
            output.key_drivers ||
            output.churn_signals ||
            output.key_risks ||
            output.action_items) && (
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1.5">
                Key Contributing Signals &amp; Action Items
              </span>
              <div className="flex flex-wrap gap-1.5">
                {(
                  output.factors ||
                  output.key_drivers ||
                  output.churn_signals ||
                  output.key_risks ||
                  output.action_items ||
                  []
                ).map((item: any, i: number) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 rounded-md text-[11px] bg-slate-900 border border-white/10 text-slate-300 flex items-center gap-1.5"
                  >
                    <ArrowRight className="w-3 h-3 text-indigo-400 shrink-0" />
                    <span>{typeof item === 'string' ? item : JSON.stringify(item)}</span>
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Raw JSON Inspector Mode */
        <div className="relative">
          <button
            type="button"
            onClick={handleCopy}
            className="absolute top-2 right-2 px-2 py-1 rounded text-[10px] bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center gap-1 cursor-pointer transition-colors"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
            {copied ? 'Copied' : 'Copy JSON'}
          </button>
          <pre className="p-3 rounded-lg bg-black/60 border border-white/5 font-mono text-[11px] text-slate-200 overflow-x-auto max-h-56 leading-relaxed">
            {JSON.stringify(output, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
