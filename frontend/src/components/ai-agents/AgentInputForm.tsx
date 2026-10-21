'use client';

import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Code2,
  Sliders,
  Check,
  HelpCircle,
  Zap,
  Building,
  User,
  DollarSign,
  TrendingUp,
  AlertTriangle,
  Clock,
  Layers,
  FileText,
  Mail,
  Shield,
  Send,
} from 'lucide-react';

export interface AgentPreset {
  name: string;
  badge?: string;
  payload: Record<string, any>;
}

export interface AgentInputFormProps {
  agentType: string;
  agentName: string;
  costEstimate: string;
  latencyEstimate: string;
  jsonValue: string;
  onChangeJson: (newJson: string) => void;
}

// Preset library tailored to every supported autonomous agent
const AGENT_PRESETS: Record<string, AgentPreset[]> = {
  lead_scoring: [
    {
      name: 'Hot Inbound Enterprise',
      badge: 'High Intent',
      payload: {
        contact_name: 'Dr. Elena Rostova',
        company: 'HyperScale Corp',
        email_opens: 14,
        page_views: 32,
        industry: 'Cloud Infrastructure',
      },
    },
    {
      name: 'Mid-Funnel Evaluation',
      badge: 'Nurture',
      payload: {
        contact_name: 'Marcus Johnson',
        company: 'Innovate AI Systems',
        email_opens: 6,
        page_views: 12,
        industry: 'FinTech & Banking',
      },
    },
    {
      name: 'Cold Outbound Prospect',
      badge: 'Cold',
      payload: {
        contact_name: 'Thomas Wright',
        company: 'Vanguard Retail',
        email_opens: 1,
        page_views: 2,
        industry: 'Enterprise Retail',
      },
    },
  ],
  email_draft: [
    {
      name: 'Architecture Scoping Follow-up',
      badge: 'Executive',
      payload: {
        recipient: 'Sarah Chen',
        context: 'Follow-up after product architecture review and POC scoping',
        tone: 'executive',
        focus_area: 'Implementation Timeline & Security',
      },
    },
    {
      name: 'Annual Renewal & Expansion',
      badge: 'Consultative',
      payload: {
        recipient: 'David Vance',
        context: 'Quarterly review discussion for contract renewal with seat expansion',
        tone: 'consultative',
        focus_area: 'Pricing & ROI Value',
      },
    },
    {
      name: 'Salesforce Migration Hook',
      badge: 'Direct',
      payload: {
        recipient: 'Lisa Thompson (VP RevOps)',
        context: 'Competitive displacement with 10x lower TCO and zero-data migration downtime',
        tone: 'direct',
        focus_area: 'Competitive Advantages',
      },
    },
  ],
  deal_analysis: [
    {
      name: 'Global Enterprise AI ($450K)',
      badge: 'Late Stage',
      payload: {
        deal_id: 401,
        title: 'Global Enterprise AI Automation',
        deal_value: 450000,
        stage: 'Proposal & Redlines',
        competitor_present: 'Salesforce Agentforce',
      },
    },
    {
      name: 'FinTech Cloud Acceleration ($85K)',
      badge: 'Mid Stage',
      payload: {
        deal_id: 402,
        title: 'FinTech Cloud Pipeline Acceleration',
        deal_value: 85000,
        stage: 'Architecture Validation',
        competitor_present: 'None / Incumbent',
      },
    },
    {
      name: 'Health System Expansion ($210K)',
      badge: 'Closing',
      payload: {
        deal_id: 403,
        title: 'Apex Health System Expansion',
        deal_value: 210000,
        stage: 'Executive Sign-off',
        competitor_present: 'HubSpot',
      },
    },
  ],
  churn_prediction: [
    {
      name: 'High ARR Accounts (> $100K)',
      badge: 'Priority',
      payload: {
        segment: 'enterprise_arr_100k_plus',
        time_horizon: '90_days',
        sensitivity: 'standard',
      },
    },
    {
      name: 'Upcoming Q4 Renewals',
      badge: 'Urgent',
      payload: {
        segment: 'annual_renewals_q4',
        time_horizon: '30_days',
        sensitivity: 'high',
      },
    },
    {
      name: 'Mid-Market Retention Check',
      badge: 'Tactical',
      payload: {
        segment: 'mid_market_50k_to_100k',
        time_horizon: '60_days',
        sensitivity: 'standard',
      },
    },
  ],
  forecast: [
    {
      name: 'Q4 Conservative (Risk-Adjusted)',
      badge: 'Safe',
      payload: {
        period: 'Q4_2026',
        scenario: 'conservative_risk_adjusted',
        include_weighted_deals: true,
      },
    },
    {
      name: 'Q4 Baseline Run-Rate',
      badge: 'Target',
      payload: {
        period: 'Q4_2026',
        scenario: 'baseline_runrate',
        include_weighted_deals: true,
      },
    },
    {
      name: 'FY 2027 Strategic Growth',
      badge: 'Expansion',
      payload: {
        period: 'Full_Year_2027',
        scenario: 'aggressive_pipeline',
        include_weighted_deals: false,
      },
    },
  ],
  meeting_summary: [
    {
      name: 'Security & Compliance Review',
      badge: '45m Tech',
      payload: {
        meeting_title: 'Stark Industries Security & SOC2 Review',
        duration_mins: 45,
        attendee_group: 'Architecture Team',
        discussion_highlights:
          'Reviewed SOC2 compliance report. Customer requested custom encryption key management and 99.99% SLA commitment.',
      },
    },
    {
      name: 'Procurement Redline Call',
      badge: '30m Commercial',
      payload: {
        meeting_title: 'DataWise Annual Master Services Agreement',
        duration_mins: 30,
        attendee_group: 'Procurement & Legal',
        discussion_highlights:
          'Agreed on payment terms Net-30 with 3-year upfront commitment for a 12% discount. Decision maker aligned.',
      },
    },
    {
      name: 'Quarterly Executive Review',
      badge: '60m C-Suite',
      payload: {
        meeting_title: 'Global Retail QBR with Executive Sponsors',
        duration_mins: 60,
        attendee_group: 'Executive Sponsors',
        discussion_highlights:
          'Reported 44% reduction in lead conversion cycle. Leadership requested expanding rollout across European division.',
      },
    },
  ],
  ticket_triage: [
    {
      name: 'Enterprise API Incident (P1)',
      badge: 'Critical',
      payload: {
        ticket_title: 'API Rate Limiting exceeded during bulk sync',
        customer_tier: 'enterprise',
        urgency: 'high',
        issue_text: 'HTTP 429 received when syncing batch contacts from production data warehouse.',
      },
    },
    {
      name: 'Billing Seat Count Discrepancy',
      badge: 'Billing',
      payload: {
        ticket_title: 'Seat count adjustment not reflected on monthly invoice',
        customer_tier: 'mid_market',
        urgency: 'medium',
        issue_text: 'Downgraded 4 inactive seats on the 1st of the month, invoice still shows previous seat count.',
      },
    },
    {
      name: 'Webhook Security Feature',
      badge: 'Product',
      payload: {
        ticket_title: 'Support for custom HMAC signatures in Zapier integration',
        customer_tier: 'standard',
        urgency: 'low',
        issue_text: 'Requesting custom SHA-256 webhook signing headers for enterprise compliance auditing.',
      },
    },
  ],
  campaign_optimize: [
    {
      name: 'Executive Webinar Invitation',
      badge: 'High Impact',
      payload: {
        subject: 'Exclusive Invite: Scaling Revenue Operations with Autonomous AI Agents',
        preview_text: 'Join 500+ RevOps executives for live pipeline automation benchmarks',
        target_segment: 'VP of Engineering / RevOps',
        campaign_type: 'Webinar Invite',
      },
    },
    {
      name: 'Salesforce Displacement Teaser',
      badge: 'Competitive',
      payload: {
        subject: 'Why 140+ RevOps teams moved from legacy CRM this quarter',
        preview_text: 'Discover 10x lower total cost of ownership and transparent sub-second AI agents',
        target_segment: 'Chief Revenue Officers (CRO)',
        campaign_type: 'Product Announcement',
      },
    },
    {
      name: '2026 AI Benchmark Report',
      badge: 'Content Nurture',
      payload: {
        subject: 'The 2026 State of Autonomous Sales Agents in Enterprise CRM',
        preview_text: 'Benchmark insights across 1.4M automated customer pipeline interactions',
        target_segment: 'Enterprise Sales Leaders',
        campaign_type: 'Nurture Sequence',
      },
    },
  ],
};

export default function AgentInputForm({
  agentType,
  agentName,
  costEstimate,
  latencyEstimate,
  jsonValue,
  onChangeJson,
}: AgentInputFormProps) {
  // Mode: 'friendly' (Visual Form) or 'json' (Developer Mode)
  const [mode, setMode] = useState<'friendly' | 'json'>('friendly');
  const [jsonError, setJsonError] = useState<string | null>(null);

  // Form field state extracted from parsed JSON
  const [formData, setFormData] = useState<Record<string, any>>({});

  // Parse external jsonValue on mount and whenever it changes externally
  useEffect(() => {
    try {
      const parsed = JSON.parse(jsonValue);
      setFormData(parsed);
      setJsonError(null);
    } catch {
      setJsonError('Invalid JSON format');
    }
  }, [jsonValue]);

  // Update a single form field and broadcast to jsonValue
  const handleFieldChange = (key: string, value: any) => {
    const updated = { ...formData, [key]: value };
    setFormData(updated);
    setJsonError(null);
    onChangeJson(JSON.stringify(updated, null, 2));
  };

  // Apply a preset payload
  const handleApplyPreset = (preset: AgentPreset) => {
    setFormData(preset.payload);
    setJsonError(null);
    onChangeJson(JSON.stringify(preset.payload, null, 2));
  };

  const presets = AGENT_PRESETS[agentType] || [];

  return (
    <div className="flex flex-col space-y-3">
      {/* ── Header with Mode Switcher & Telemetry ──────────────────────── */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-1">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-200 flex items-center gap-1.5">
            <Sliders className="w-3.5 h-3.5 text-indigo-400" />
            Agent Parameters
          </span>
          <span className="text-[11px] px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 font-medium border border-indigo-500/20">
            {mode === 'friendly' ? 'Customer Friendly UI' : 'Raw JSON Mode'}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[10px] text-slate-400 font-mono hidden sm:inline">
            Est: {costEstimate} • {latencyEstimate}
          </span>

          {/* Toggle between Friendly Form and Developer JSON */}
          <div className="flex items-center rounded-lg bg-slate-900 border border-white/10 p-0.5 text-[11px]">
            <button
              type="button"
              id="agent-mode-friendly-btn"
              onClick={() => setMode('friendly')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md transition-all cursor-pointer font-medium ${
                mode === 'friendly'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Sparkles className="w-3 h-3" />
              <span>Friendly Form</span>
            </button>
            <button
              type="button"
              id="agent-mode-json-btn"
              onClick={() => setMode('json')}
              className={`flex items-center gap-1 px-2.5 py-1 rounded-md transition-all cursor-pointer font-medium ${
                mode === 'json'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Code2 className="w-3 h-3" />
              <span>JSON</span>
            </button>
          </div>
        </div>
      </div>

      {/* ── Quick Presets / Business Scenarios ─────────────────────────── */}
      {presets.length > 0 && (
        <div className="flex flex-wrap items-center gap-1.5 p-2 rounded-xl bg-indigo-500/[0.04] border border-indigo-500/15">
          <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 flex items-center gap-1 mr-1">
            <Zap className="w-3 h-3 text-amber-400" />
            Quick Scenarios:
          </span>
          {presets.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleApplyPreset(preset)}
              className="px-2.5 py-1 rounded-lg text-xs bg-slate-900/90 hover:bg-indigo-600/20 border border-white/10 hover:border-indigo-500/40 text-slate-200 transition-all flex items-center gap-1.5 cursor-pointer shadow-sm group"
            >
              <span className="text-slate-300 group-hover:text-white font-medium">
                {preset.name}
              </span>
              {preset.badge && (
                <span className="text-[9px] px-1.5 py-0.2 rounded bg-indigo-500/20 text-indigo-300 font-semibold uppercase">
                  {preset.badge}
                </span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* ── View Body: Customer-Friendly Form vs Developer JSON ──────────── */}
      {mode === 'friendly' ? (
        <div className="p-4 rounded-xl bg-slate-950/70 border border-white/10 space-y-4 shadow-inner">
          {/* Agent Spec Specific Form Renderers */}
          {agentType === 'lead_scoring' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <User className="w-3.5 h-3.5 text-indigo-400" />
                  Prospect Full Name
                </label>
                <input
                  type="text"
                  value={formData.contact_name || ''}
                  onChange={(e) => handleFieldChange('contact_name', e.target.value)}
                  placeholder="e.g. Dr. Elena Rostova"
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <Building className="w-3.5 h-3.5 text-indigo-400" />
                  Company / Organization
                </label>
                <input
                  type="text"
                  value={formData.company || ''}
                  onChange={(e) => handleFieldChange('company', e.target.value)}
                  placeholder="e.g. HyperScale Corp"
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5">
                    <Mail className="w-3.5 h-3.5 text-cyan-400" />
                    Email Opens &amp; Clicks
                  </label>
                  <span className="text-xs font-mono font-bold text-cyan-400">
                    {formData.email_opens || 0} opens
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="50"
                  value={formData.email_opens || 0}
                  onChange={(e) => handleFieldChange('email_opens', parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5">
                    <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                    Website &amp; Pricing Visits
                  </label>
                  <span className="text-xs font-mono font-bold text-emerald-400">
                    {formData.page_views || 0} views
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="60"
                  value={formData.page_views || 0}
                  onChange={(e) => handleFieldChange('page_views', parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>
            </div>
          )}

          {agentType === 'email_draft' && (
            <div className="space-y-3.5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                    <User className="w-3.5 h-3.5 text-indigo-400" />
                    Recipient Name / Title
                  </label>
                  <input
                    type="text"
                    value={formData.recipient || ''}
                    onChange={(e) => handleFieldChange('recipient', e.target.value)}
                    placeholder="e.g. Sarah Chen (Chief Information Officer)"
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                    Communication Tone
                  </label>
                  <div className="grid grid-cols-3 gap-1.5">
                    {['executive', 'consultative', 'direct'].map((tone) => (
                      <button
                        key={tone}
                        type="button"
                        onClick={() => handleFieldChange('tone', tone)}
                        className={`py-1.5 px-2 text-center rounded-lg text-xs capitalize font-medium transition-all cursor-pointer ${
                          formData.tone === tone
                            ? 'bg-indigo-600 text-white shadow-sm'
                            : 'bg-slate-900 border border-white/10 text-slate-400 hover:text-white'
                        }`}
                      >
                        {tone}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  Meeting Discussion &amp; Context Focus
                </label>
                <textarea
                  rows={2}
                  value={formData.context || ''}
                  onChange={(e) => handleFieldChange('context', e.target.value)}
                  placeholder="e.g. Follow-up after product architecture review and POC scoping"
                  className="w-full p-2.5 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>
            </div>
          )}

          {agentType === 'deal_analysis' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  Deal Opportunity Name
                </label>
                <input
                  type="text"
                  value={formData.title || ''}
                  onChange={(e) => handleFieldChange('title', e.target.value)}
                  placeholder="e.g. Global Enterprise AI Automation"
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
                  Deal Value (USD)
                </label>
                <input
                  type="number"
                  value={formData.deal_value || 0}
                  onChange={(e) => handleFieldChange('deal_value', parseFloat(e.target.value) || 0)}
                  placeholder="450000"
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                  Current Pipeline Stage
                </label>
                <select
                  value={formData.stage || 'Proposal & Redlines'}
                  onChange={(e) => handleFieldChange('stage', e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                >
                  <option value="Discovery & Scoping">Discovery &amp; Scoping</option>
                  <option value="Architecture Validation">Architecture Validation</option>
                  <option value="Proposal & Redlines">Proposal &amp; Contract Redlines</option>
                  <option value="Executive Sign-off">Executive Sign-off &amp; Procurement</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                  Competitor In Play
                </label>
                <select
                  value={formData.competitor_present || 'Salesforce Agentforce'}
                  onChange={(e) => handleFieldChange('competitor_present', e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                >
                  <option value="None / Incumbent">None / Incumbent Legacy Stack</option>
                  <option value="Salesforce Agentforce">Salesforce Agentforce</option>
                  <option value="HubSpot">HubSpot Enterprise</option>
                  <option value="Microsoft Copilot">Microsoft Dynamics / Copilot</option>
                </select>
              </div>
            </div>
          )}

          {agentType === 'churn_prediction' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <Building className="w-3.5 h-3.5 text-indigo-400" />
                  Customer Segment
                </label>
                <select
                  value={formData.segment || 'enterprise_arr_100k_plus'}
                  onChange={(e) => handleFieldChange('segment', e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                >
                  <option value="enterprise_arr_100k_plus">Enterprise Accounts (ARR &gt; $100K)</option>
                  <option value="mid_market_50k_to_100k">Mid-Market ($50K – $100K ARR)</option>
                  <option value="annual_renewals_q4">Upcoming Q4 Annual Renewals</option>
                  <option value="smb_rapid_growth">Fast-Growing SMB Accounts</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <Clock className="w-3.5 h-3.5 text-indigo-400" />
                  Time Horizon
                </label>
                <div className="grid grid-cols-3 gap-1.5">
                  {[
                    { id: '30_days', label: '30 Days' },
                    { id: '60_days', label: '60 Days' },
                    { id: '90_days', label: '90 Days' },
                  ].map((item) => (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => handleFieldChange('time_horizon', item.id)}
                      className={`py-1.5 px-2 text-center rounded-lg text-xs font-medium transition-all cursor-pointer ${
                        formData.time_horizon === item.id
                          ? 'bg-indigo-600 text-white shadow-sm'
                          : 'bg-slate-900 border border-white/10 text-slate-400 hover:text-white'
                      }`}
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {agentType === 'forecast' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <Clock className="w-3.5 h-3.5 text-indigo-400" />
                  Forecasting Period
                </label>
                <select
                  value={formData.period || 'Q4_2026'}
                  onChange={(e) => handleFieldChange('period', e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                >
                  <option value="Q4_2026">Q4 2026 (Current Quarter)</option>
                  <option value="Q1_2027">Q1 2027 (Next Quarter)</option>
                  <option value="Full_Year_2027">Full Year 2027 Annual</option>
                </select>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                  <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
                  Forecast Model Scenario
                </label>
                <select
                  value={formData.scenario || 'conservative_risk_adjusted'}
                  onChange={(e) => handleFieldChange('scenario', e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                >
                  <option value="conservative_risk_adjusted">Conservative (Risk-Adjusted)</option>
                  <option value="baseline_runrate">Baseline (Historical Run-Rate)</option>
                  <option value="aggressive_pipeline">Aggressive (High Growth Target)</option>
                </select>
              </div>
            </div>
          )}

          {agentType === 'meeting_summary' && (
            <div className="space-y-3.5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                    <FileText className="w-3.5 h-3.5 text-indigo-400" />
                    Meeting Title
                  </label>
                  <input
                    type="text"
                    value={formData.meeting_title || ''}
                    onChange={(e) => handleFieldChange('meeting_title', e.target.value)}
                    placeholder="e.g. Stark Industries Security Review"
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5 mb-1">
                    <Clock className="w-3.5 h-3.5 text-indigo-400" />
                    Duration
                  </label>
                  <div className="grid grid-cols-4 gap-1.5">
                    {[15, 30, 45, 60].map((mins) => (
                      <button
                        key={mins}
                        type="button"
                        onClick={() => handleFieldChange('duration_mins', mins)}
                        className={`py-1.5 px-2 text-center rounded-lg text-xs font-medium transition-all cursor-pointer ${
                          formData.duration_mins === mins
                            ? 'bg-indigo-600 text-white shadow-sm'
                            : 'bg-slate-900 border border-white/10 text-slate-400 hover:text-white'
                        }`}
                      >
                        {mins}m
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                  Discussion Points / Raw Meeting Notes
                </label>
                <textarea
                  rows={2}
                  value={formData.discussion_highlights || ''}
                  onChange={(e) => handleFieldChange('discussion_highlights', e.target.value)}
                  placeholder="Paste raw notes or audio transcript highlights here..."
                  className="w-full p-2.5 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>
            </div>
          )}

          {agentType === 'ticket_triage' && (
            <div className="space-y-3.5">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div className="md:col-span-2">
                  <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                    Support Ticket Subject
                  </label>
                  <input
                    type="text"
                    value={formData.ticket_title || ''}
                    onChange={(e) => handleFieldChange('ticket_title', e.target.value)}
                    placeholder="e.g. API Rate Limiting exceeded during bulk sync"
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                    Urgency / SLA
                  </label>
                  <select
                    value={formData.urgency || 'high'}
                    onChange={(e) => handleFieldChange('urgency', e.target.value)}
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  >
                    <option value="critical">Critical (P1 Outage)</option>
                    <option value="high">High (P2 Blocking)</option>
                    <option value="medium">Medium (P3 Standard)</option>
                    <option value="low">Low (P4 Query)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                  Customer Issue Description
                </label>
                <textarea
                  rows={2}
                  value={formData.issue_text || ''}
                  onChange={(e) => handleFieldChange('issue_text', e.target.value)}
                  placeholder="Describe the issue reported by the customer..."
                  className="w-full p-2.5 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>
            </div>
          )}

          {agentType === 'campaign_optimize' && (
            <div className="space-y-3.5">
              <div>
                <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                  Email Subject Line Hook
                </label>
                <input
                  type="text"
                  value={formData.subject || ''}
                  onChange={(e) => handleFieldChange('subject', e.target.value)}
                  placeholder="e.g. Exclusive Invite: Scaling Revenue Operations with Autonomous AI Agents"
                  className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                    Pre-header / Preview Snippet
                  </label>
                  <input
                    type="text"
                    value={formData.preview_text || ''}
                    onChange={(e) => handleFieldChange('preview_text', e.target.value)}
                    placeholder="e.g. Join 500+ RevOps executives for live pipeline automation benchmarks"
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>

                <div>
                  <label className="text-[11px] font-semibold text-slate-300 mb-1 block">
                    Target Buyer Persona
                  </label>
                  <select
                    value={formData.target_segment || 'VP of Engineering / RevOps'}
                    onChange={(e) => handleFieldChange('target_segment', e.target.value)}
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  >
                    <option value="VP of Engineering / RevOps">VP of Engineering / RevOps</option>
                    <option value="Chief Revenue Officers (CRO)">Chief Revenue Officers (CRO)</option>
                    <option value="Enterprise Sales Leaders">Enterprise Sales Leaders</option>
                    <option value="Growth Marketing Directors">Growth Marketing Directors</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Fallback for generic or dynamic fields */}
          {!['lead_scoring', 'email_draft', 'deal_analysis', 'churn_prediction', 'forecast', 'meeting_summary', 'ticket_triage', 'campaign_optimize'].includes(agentType) && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.entries(formData).map(([k, v]) => (
                <div key={k}>
                  <label className="text-[11px] font-semibold text-slate-300 capitalize mb-1 block">
                    {k.replace(/_/g, ' ')}
                  </label>
                  <input
                    type="text"
                    value={typeof v === 'object' ? JSON.stringify(v) : String(v)}
                    onChange={(e) => handleFieldChange(k, e.target.value)}
                    className="w-full px-3 py-2 text-xs rounded-lg bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-colors"
                  />
                </div>
              ))}
            </div>
          )}

          {/* Sync indicator */}
          <div className="flex items-center justify-between pt-1 border-t border-white/5 text-[10px] text-slate-500">
            <span className="flex items-center gap-1 text-emerald-400">
              <Check className="w-3 h-3" />
              Inputs auto-synchronized with AI execution payload
            </span>
            <button
              type="button"
              onClick={() => setMode('json')}
              className="hover:text-indigo-400 underline transition-colors cursor-pointer"
            >
              Inspect underlying JSON
            </button>
          </div>
        </div>
      ) : (
        /* Developer Mode: Direct JSON Editor */
        <div className="space-y-1.5">
          <textarea
            rows={5}
            value={jsonValue}
            onChange={(e) => {
              onChangeJson(e.target.value);
              try {
                const parsed = JSON.parse(e.target.value);
                setFormData(parsed);
                setJsonError(null);
              } catch (err: any) {
                setJsonError('Syntax error: invalid JSON');
              }
            }}
            className="w-full p-3 rounded-xl bg-slate-950 border border-white/10 font-mono text-xs text-cyan-300 focus:outline-none focus:border-indigo-500 transition-colors shadow-inner"
          />
          {jsonError ? (
            <div className="text-[11px] text-rose-400 flex items-center gap-1 font-mono">
              <AlertTriangle className="w-3 h-3" />
              {jsonError}
            </div>
          ) : (
            <div className="text-[10px] text-slate-500 flex items-center justify-between">
              <span>Valid JSON payload ready for OpenRouter AI inference</span>
              <button
                type="button"
                onClick={() => setMode('friendly')}
                className="text-indigo-400 hover:text-indigo-300 underline cursor-pointer"
              >
                Return to Friendly Form
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
