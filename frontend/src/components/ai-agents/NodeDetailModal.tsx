'use client';

import React from 'react';
import { X, CheckCircle2, Clock, Terminal, Copy, Check } from 'lucide-react';
import { GraphNodeStep } from '../../types/crm';

interface NodeDetailModalProps {
  step: GraphNodeStep | null;
  onClose: () => void;
}

export default function NodeDetailModal({ step, onClose }: NodeDetailModalProps) {
  const [copied, setCopied] = React.useState(false);

  if (!step) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(step.data || {}, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div 
        className="w-full max-w-2xl bg-[#0f172a] border border-indigo-500/30 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="p-4 px-6 border-b border-white/10 flex items-center justify-between bg-slate-900/80">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400">
              <Terminal className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <span>{step.label}</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-mono">
                  {step.status.toUpperCase()}
                </span>
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Workflow Step: <span className="text-indigo-300">{step.label}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-xs text-slate-300 font-medium">
              <Clock className="w-3.5 h-3.5 text-cyan-400" />
              <span>{step.latency_ms} ms</span>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Content */}
        <div className="p-6 overflow-y-auto space-y-4">
          <div>
            <span className="text-xs uppercase tracking-wider font-semibold text-slate-400 block mb-1">
              Summary
            </span>
            <div className="p-3 rounded-xl bg-slate-900/60 border border-white/5 text-xs text-slate-200">
              {step.summary}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-xs uppercase tracking-wider font-semibold text-slate-400">
                Step Details &amp; Output Data
              </span>
              <button
                onClick={handleCopy}
                className="flex items-center gap-1 text-[11px] text-indigo-400 hover:text-indigo-300 cursor-pointer"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy Data'}</span>
              </button>
            </div>
            <pre className="p-4 rounded-xl bg-[#090d16] border border-white/10 text-[11px] font-mono text-cyan-300/90 overflow-x-auto max-h-72 leading-relaxed selection:bg-indigo-500/30">
              {JSON.stringify(step.data || { note: 'No supplementary data emitted.' }, null, 2)}
            </pre>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-3 px-6 border-t border-white/10 bg-slate-900/50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
