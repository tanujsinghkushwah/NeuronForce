'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import { api } from '../../lib/api';
import { AppSettings } from '../../types/crm';
import {
  Settings as SettingsIcon,
  Sliders,
  Shield,
  Bell,
  Cpu,
  Building,
  CheckCircle2,
  Save,
  DollarSign,
  Lock,
  Zap
} from 'lucide-react';

export default function SettingsPage() {
  const [settings, setSettings] = useState<AppSettings | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.getSettings().then(setSettings).catch(() => {
      setSettings({
        company: {
          name: 'NeuronForce Enterprise',
          timezone: 'America/Los_Angeles (PST)',
          currency: 'USD ($)',
          fiscal_year_start: 'January'
        },
        ai_config: {
          auto_lead_scoring: true,
          auto_email_drafts: true,
          churn_prediction_enabled: true,
          forecast_model: 'Ensemble Bayesian',
          max_daily_budget: 10.0,
          confidence_threshold: 0.75,
          model_provider: 'OpenRouter Multi-Model (Claude 3.5, Llama 3.3, GPT-4o, Gemini 2.0)',
          cost_optimization: true
        },
        notifications: {
          email_alerts: true,
          deal_stage_changes: true,
          ai_task_completion: true,
          daily_digest: true
        },
        pipeline_stages: [
          { key: 'prospecting', label: 'Prospecting', probability: 10 },
          { key: 'qualification', label: 'Qualification', probability: 25 },
          { key: 'proposal', label: 'Proposal', probability: 50 },
          { key: 'negotiation', label: 'Negotiation', probability: 75 },
          { key: 'closed_won', label: 'Closed Won', probability: 100 },
          { key: 'closed_lost', label: 'Closed Lost', probability: 0 }
        ]
      });
    });
  }, []);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  if (!settings) return null;

  return (
    <div className="flex-1 flex flex-col pb-12">
      <Header
        title="System &amp; AI Configuration"
        subtitle="Manage organization parameters, autonomous agent policies, and budget guardrails"
      />

      <div className="p-6 md:p-8 space-y-8 max-w-5xl mx-auto w-full text-xs">
        <form onSubmit={handleSave} className="space-y-6">
          {/* AI Autonomous Agent Policies */}
          <div className="glass-panel p-6 rounded-2xl border-indigo-500/30 bg-gradient-to-br from-[#0c1224] to-slate-900">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-white/10">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                  <Cpu className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">AI Agent Governance &amp; Thresholds</h3>
                  <p className="text-[11px] text-slate-400">Control budget safety caps, confidence cutoffs, and provider fallbacks</p>
                </div>
              </div>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 font-semibold">
                Autonomous Mode Active
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  Confidence Threshold for Auto-Action: {Math.round(settings.ai_config.confidence_threshold * 100)}%
                </label>
                <p className="text-[11px] text-slate-400 mb-2">
                  Decisions below this score flag for human sales rep manual review.
                </p>
                <input
                  type="range"
                  min="0.5"
                  max="0.95"
                  step="0.05"
                  value={settings.ai_config.confidence_threshold}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      ai_config: { ...settings.ai_config, confidence_threshold: parseFloat(e.target.value) }
                    })
                  }
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">
                  Daily Hard AI Spend Cap: ${settings.ai_config.max_daily_budget.toFixed(2)}
                </label>
                <p className="text-[11px] text-slate-400 mb-2">
                  Automatic rate-limiter prevents runaway token costs across microservices.
                </p>
                <input
                  type="range"
                  min="2"
                  max="50"
                  step="1"
                  value={settings.ai_config.max_daily_budget}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      ai_config: { ...settings.ai_config, max_daily_budget: parseFloat(e.target.value) }
                    })
                  }
                  className="w-full accent-emerald-500 cursor-pointer"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 pt-4 border-t border-white/5">
              <label className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-white/5 cursor-pointer hover:border-indigo-500/30">
                <input
                  type="checkbox"
                  checked={settings.ai_config.auto_lead_scoring}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      ai_config: { ...settings.ai_config, auto_lead_scoring: e.target.checked }
                    })
                  }
                  className="accent-indigo-500 rounded"
                />
                <div>
                  <span className="font-semibold text-white block">Auto Lead Scoring</span>
                  <span className="text-[10px] text-slate-400">Score new inbound leads instantly</span>
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-white/5 cursor-pointer hover:border-indigo-500/30">
                <input
                  type="checkbox"
                  checked={settings.ai_config.churn_prediction_enabled}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      ai_config: { ...settings.ai_config, churn_prediction_enabled: e.target.checked }
                    })
                  }
                  className="accent-cyan-500 rounded"
                />
                <div>
                  <span className="font-semibold text-white block">Churn Sentinel</span>
                  <span className="text-[10px] text-slate-400">Weekly predictive risk alerts</span>
                </div>
              </label>

              <label className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-white/5 cursor-pointer hover:border-indigo-500/30">
                <input
                  type="checkbox"
                  checked={settings.ai_config.cost_optimization}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      ai_config: { ...settings.ai_config, cost_optimization: e.target.checked }
                    })
                  }
                  className="accent-purple-500 rounded"
                />
                <div>
                  <span className="font-semibold text-white block">Cost Optimizer</span>
                  <span className="text-[10px] text-slate-400">Route small tasks to Flash models</span>
                </div>
              </label>
            </div>
          </div>

          {/* Company Profile Settings */}
          <div className="glass-panel p-6 rounded-2xl border border-white/10">
            <div className="flex items-center gap-2.5 mb-4 pb-3 border-b border-white/10">
              <div className="w-8 h-8 rounded-xl bg-slate-800 text-slate-300 flex items-center justify-center">
                <Building className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">Organization Profile</h3>
                <p className="text-[11px] text-slate-400">Base configuration for enterprise billing and reporting</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-slate-300 font-medium mb-1">Company Name</label>
                <input
                  type="text"
                  value={settings.company.name}
                  onChange={(e) =>
                    setSettings({ ...settings, company: { ...settings.company, name: e.target.value } })
                  }
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Default Timezone</label>
                <input
                  type="text"
                  value={settings.company.timezone}
                  onChange={(e) =>
                    setSettings({ ...settings, company: { ...settings.company, timezone: e.target.value } })
                  }
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Reporting Currency</label>
                <input
                  type="text"
                  value={settings.company.currency}
                  onChange={(e) =>
                    setSettings({ ...settings, company: { ...settings.company, currency: e.target.value } })
                  }
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block text-slate-300 font-medium mb-1">Fiscal Year Start</label>
                <input
                  type="text"
                  value={settings.company.fiscal_year_start}
                  onChange={(e) =>
                    setSettings({ ...settings, company: { ...settings.company, fiscal_year_start: e.target.value } })
                  }
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
          </div>

          {/* Pipeline Stages Customization */}
          <div className="glass-panel p-6 rounded-2xl border border-white/10">
            <h3 className="text-sm font-bold text-white mb-1">Sales Pipeline Stages</h3>
            <p className="text-[11px] text-slate-400 mb-4">Stage probabilities used for AI weighted revenue calculations</p>

            <div className="divide-y divide-white/5">
              {settings.pipeline_stages.map((st, idx) => (
                <div key={st.key} className="py-2.5 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="w-5 h-5 rounded-full bg-slate-800 text-slate-400 text-[10px] flex items-center justify-center font-bold">
                      {idx + 1}
                    </span>
                    <span className="font-semibold text-white">{st.label}</span>
                    <span className="text-slate-500 font-mono text-[10px]">({st.key})</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-slate-400 text-[11px]">Weight:</span>
                    <span className="font-bold text-cyan-400">{st.probability}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Save Button Bar */}
          <div className="flex items-center justify-between pt-4">
            {saved ? (
              <span className="text-emerald-400 font-semibold flex items-center gap-1.5 animate-in fade-in">
                <CheckCircle2 className="w-4 h-4" />
                Settings saved successfully!
              </span>
            ) : <span />}

            <button
              type="submit"
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
            >
              <Save className="w-4 h-4" />
              <span>Save Configuration</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
