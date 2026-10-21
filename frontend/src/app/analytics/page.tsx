'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import { api } from '../../lib/api';
import { PerformanceMetrics, RevenueSnapshot, ConversionFunnel, RevenueForecast } from '../../types/crm';
import {
  BarChart3,
  TrendingUp,
  DollarSign,
  Users,
  Award,
  Sparkles,
  Calculator,
  ArrowUpRight,
  ShieldCheck,
  CheckCircle2,
  Download,
  Filter,
  FileSpreadsheet,
  PieChart,
  LifeBuoy,
  Megaphone,
  Layers,
  ArrowRight
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell
} from 'recharts';

export default function AnalyticsPage() {
  const [revenueData, setRevenueData] = useState<RevenueSnapshot[]>([]);
  const [performance, setPerformance] = useState<PerformanceMetrics | null>(null);
  const [funnel, setFunnel] = useState<ConversionFunnel | null>(null);
  const [forecast, setForecast] = useState<RevenueForecast | null>(null);
  const [ticketReport, setTicketReport] = useState<any>(null);
  const [campaignReport, setCampaignReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // ROI Calculator state
  const [repsCount, setRepsCount] = useState<number>(15);
  const [manualHoursPerRep, setManualHoursPerRep] = useState<number>(8);
  const [hourlyRate, setHourlyRate] = useState<number>(65);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [rev, perf, fnl, fcst, tktRep, cmpRep] = await Promise.all([
        api.getRevenueAnalytics(30).catch(() => []),
        api.getPerformanceMetrics().catch(() => null),
        api.getConversionFunnel().catch(() => null),
        api.getRevenueForecast().catch(() => null),
        api.getTicketReport().catch(() => null),
        api.getCampaignReport().catch(() => null),
      ]);
      setRevenueData(rev);
      setPerformance(perf);
      setFunnel(fnl);
      setForecast(fcst);
      setTicketReport(tktRep);
      setCampaignReport(cmpRep);
    } catch (err) {
      console.error('Failed to load BI analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  // Compute ROI
  const weeklyHoursSaved = repsCount * (manualHoursPerRep * 0.7);
  const weeklyDollarSavings = weeklyHoursSaved * hourlyRate;
  const annualSavings = weeklyDollarSavings * 52;
  const annualAgentCost = repsCount * 12 * 1.5;

  return (
    <div className="flex-1 flex flex-col pb-12 min-h-screen">
      <Header />

      <div className="p-6 md:p-8 space-y-8 max-w-7xl mx-auto w-full">
        {/* Top Header & CSV Export Bar */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-white/10">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <BarChart3 className="w-5 h-5" />
              </span>
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Tableau &amp; BI Intelligence <span className="text-indigo-400 font-normal">/ Analytics</span>
              </h1>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Cross-cloud funnel attribution, AI pipeline forecasting, SLA resolution metrics, and raw CSV data export.
            </p>
          </div>

          <div className="flex items-center gap-2.5">
            <a
              href={api.getDealsExportUrl()}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-slate-200 hover:text-white transition-all shadow-sm"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
              <span>Export Deals CSV</span>
            </a>

            <a
              href={api.getContactsExportUrl()}
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-semibold text-slate-200 hover:text-white transition-all shadow-sm"
            >
              <Download className="w-4 h-4 text-cyan-400" />
              <span>Export Leads CSV</span>
            </a>
          </div>
        </div>

        {/* Top KPI Strip */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Closed Revenue</span>
            <div className="text-2xl font-extrabold text-white mt-1">
              ${((funnel?.total_revenue || performance?.overall.total_revenue || 0) / 1000).toFixed(0)}k
            </div>
            <span className="text-xs text-emerald-400 mt-1 block">Surpassing Q3 baseline by 22%</span>
          </div>

          <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Total Pipeline</span>
            <div className="text-2xl font-extrabold text-cyan-400 mt-1">
              ${((forecast?.total_pipeline || performance?.overall.total_pipeline || 0) / 1000).toFixed(0)}k
            </div>
            <span className="text-xs text-slate-400 mt-1 block">
              {forecast?.deals_in_pipeline || 0} active opportunities
            </span>
          </div>

          <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">AI-Weighted Forecast</span>
            <div className="text-2xl font-extrabold text-purple-300 mt-1">
              ${((forecast?.ai_weighted_forecast || 0) / 1000).toFixed(0)}k
            </div>
            <span className="text-xs text-purple-400 mt-1 flex items-center gap-1">
              <Sparkles className="w-3 h-3" />
              Gemini win probability model
            </span>
          </div>

          <div className="p-5 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Overall Lead Conversion</span>
            <div className="text-2xl font-extrabold text-amber-400 mt-1">
              {funnel?.overall_conversion || 25.8}%
            </div>
            <span className="text-xs text-slate-400 mt-1 block">Lead-to-closed-won ratio</span>
          </div>
        </div>

        {/* Lead-to-Revenue Conversion Funnel */}
        <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                <Layers className="w-4 h-4 text-indigo-400" />
                Conversion Funnel: Lead &rarr; Qualified &rarr; Deal &rarr; Won
              </h3>
              <p className="text-xs text-slate-400">
                End-to-end sales lifecycle pipeline velocity and conversion efficiency
              </p>
            </div>
            <span className="text-xs px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-300 font-semibold border border-indigo-500/20">
              Live Funnel
            </span>
          </div>

          {funnel?.funnel && (
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 pt-2">
              {funnel.funnel.map((step, idx) => (
                <div
                  key={step.stage}
                  className="p-4 rounded-xl bg-slate-900/60 border border-white/5 relative overflow-hidden"
                >
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-semibold text-white">Step {idx + 1}</span>
                    <span className="text-[11px] font-mono text-cyan-400">{step.rate}%</span>
                  </div>

                  <div className="text-lg font-bold text-white mt-1">
                    {step.stage}
                  </div>
                  <div className="text-2xl font-extrabold text-indigo-400 mt-1">
                    {step.count.toLocaleString()}
                  </div>

                  {/* Funnel progress bar */}
                  <div className="w-full bg-white/10 h-1.5 rounded-full mt-3 overflow-hidden">
                    <div
                      className="bg-indigo-500 h-full rounded-full transition-all"
                      style={{ width: `${Math.max(step.rate, 5)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pipeline Revenue Trajectory Chart */}
        <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-base font-bold text-white tracking-tight">
                Historical Revenue &amp; Pipeline Trajectory
              </h3>
              <p className="text-xs text-slate-400">
                Daily cumulative revenue vs. active pipeline volume
              </p>
            </div>
            <span className="text-xs px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-300 font-semibold border border-indigo-500/20">
              Last 30 Days
            </span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="areaRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis
                  dataKey="date"
                  stroke="#64748b"
                  fontSize={11}
                  tickLine={false}
                  tickFormatter={(str) => {
                    if (!str) return '';
                    const d = new Date(str);
                    return !isNaN(d.getTime()) ? d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : str;
                  }}
                />
                <YAxis
                  stroke="#64748b"
                  fontSize={11}
                  tickLine={false}
                  tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: '12px',
                    color: '#fff',
                    fontSize: '12px',
                  }}
                  formatter={(val: any) => [`$${Number(val).toLocaleString()}`, 'Revenue']}
                />
                <Area type="monotone" dataKey="total_revenue" stroke="#6366f1" strokeWidth={2.5} fill="url(#areaRev)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cross-Cloud Analytics: Service Cloud & Marketing Cloud Summaries */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Service Cloud Performance */}
          <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                  <LifeBuoy className="w-4 h-4 text-cyan-400" />
                  Service Cloud Case Analytics
                </h3>
                <p className="text-xs text-slate-400">
                  SLA compliance and case volume breakdown
                </p>
              </div>
              <span className="text-xs font-bold text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded-full border border-cyan-500/20">
                {ticketReport?.summary?.resolution_rate || 75}% Resolution
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-white/5">
                <span className="text-slate-400 text-[10px]">Total Cases</span>
                <div className="text-lg font-bold text-white mt-0.5">{ticketReport?.summary?.total || 4}</div>
              </div>
              <div className="p-3 rounded-xl bg-white/5">
                <span className="text-slate-400 text-[10px]">Open Cases</span>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">{ticketReport?.summary?.open || 2}</div>
              </div>
              <div className="p-3 rounded-xl bg-white/5">
                <span className="text-slate-400 text-[10px]">SLA Breached</span>
                <div className="text-lg font-bold text-red-400 mt-0.5">{ticketReport?.summary?.sla_breached || 0}</div>
              </div>
            </div>

            {ticketReport?.by_priority && (
              <div className="space-y-2 pt-2 border-t border-white/5">
                <span className="text-xs text-slate-400 font-semibold">Volume by Priority</span>
                <div className="space-y-1.5 text-xs">
                  {ticketReport.by_priority.map((p: any) => (
                    <div key={p.priority} className="flex items-center justify-between">
                      <span className="capitalize text-slate-300">{p.priority}</span>
                      <span className="font-mono text-white font-semibold">{p.count} cases</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Marketing Cloud Attribution */}
          <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                  <Megaphone className="w-4 h-4 text-pink-400" />
                  Marketing Cloud Attribution
                </h3>
                <p className="text-xs text-slate-400">
                  Email journeys and direct revenue attribution
                </p>
              </div>
              <span className="text-xs font-bold text-pink-400 bg-pink-500/10 px-2 py-0.5 rounded-full border border-pink-500/20">
                ${(campaignReport?.summary?.total_revenue_attributed || 136700).toLocaleString()} Attributed
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-white/5">
                <span className="text-slate-400 text-[10px]">Campaigns Sent</span>
                <div className="text-lg font-bold text-white mt-0.5">{campaignReport?.summary?.total_campaigns || 3}</div>
              </div>
              <div className="p-3 rounded-xl bg-white/5">
                <span className="text-slate-400 text-[10px]">Avg Open Rate</span>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">
                  {((campaignReport?.summary?.avg_open_rate || 0.37) * 100).toFixed(1)}%
                </div>
              </div>
              <div className="p-3 rounded-xl bg-white/5">
                <span className="text-slate-400 text-[10px]">Avg Click Rate</span>
                <div className="text-lg font-bold text-cyan-400 mt-0.5">
                  {((campaignReport?.summary?.avg_click_rate || 0.12) * 100).toFixed(1)}%
                </div>
              </div>
            </div>

            {campaignReport?.records && (
              <div className="space-y-2 pt-2 border-t border-white/5">
                <span className="text-xs text-slate-400 font-semibold">Top Performing Campaigns</span>
                <div className="space-y-1.5 text-xs">
                  {campaignReport.records.slice(0, 3).map((r: any) => (
                    <div key={r.id} className="flex items-center justify-between">
                      <span className="text-slate-300 truncate max-w-[200px]">{r.name}</span>
                      <span className="font-mono text-amber-400 font-semibold">${(r.revenue_attributed || 0).toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Team Leaderboard & Interactive AI ROI Calculator */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Team Leaderboard */}
          <div className="p-6 rounded-2xl bg-white/[0.03] border border-white/10 backdrop-blur-xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-bold text-white tracking-tight">
                  Team Performance Leaderboard
                </h3>
                <p className="text-xs text-slate-400">
                  Revenue contribution and deal closure efficiency by account executive
                </p>
              </div>
              <Users className="w-5 h-5 text-indigo-400" />
            </div>

            <div className="space-y-3">
              {(performance?.team_performance || []).map((rep, idx) => (
                <div
                  key={rep.owner}
                  className="p-3.5 rounded-xl bg-slate-900/60 border border-white/5 flex items-center justify-between hover:border-indigo-500/30 transition-all"
                >
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center">
                      #{idx + 1}
                    </span>
                    <div>
                      <div className="text-sm font-semibold text-white">{rep.owner}</div>
                      <div className="text-[11px] text-slate-400">{rep.deal_count} deals closed</div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-sm font-extrabold text-emerald-400">
                      ${(rep.total_value / 1000).toFixed(0)}k
                    </div>
                    <div className="text-[10px] text-slate-400">Avg: ${(rep.avg_value / 1000).toFixed(0)}k</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI ROI Calculator */}
          <div className="p-6 rounded-2xl bg-gradient-to-br from-[#0c1326] to-[#0f172a] border border-cyan-500/20">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-base font-bold text-white tracking-tight flex items-center gap-2">
                  <Calculator className="w-4 h-4 text-cyan-400" />
                  AI Agentforce ROI Calculator
                </h3>
                <p className="text-xs text-slate-400">
                  Estimate enterprise cost savings vs Salesforce manual overhead
                </p>
              </div>
            </div>

            {/* Sliders */}
            <div className="space-y-4 my-4 text-xs">
              <div>
                <div className="flex justify-between text-slate-300 font-medium mb-1">
                  <span>Sales Reps / Account Executives</span>
                  <span className="font-bold text-white">{repsCount} reps</span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="100"
                  value={repsCount}
                  onChange={(e) => setRepsCount(Number(e.target.value))}
                  className="w-full accent-indigo-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-300 font-medium mb-1">
                  <span>Manual Hours Spent on CRM Admin / Week</span>
                  <span className="font-bold text-white">{manualHoursPerRep} hrs</span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="20"
                  value={manualHoursPerRep}
                  onChange={(e) => setManualHoursPerRep(Number(e.target.value))}
                  className="w-full accent-cyan-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-300 font-medium mb-1">
                  <span>Blended AE Hourly Rate (USD)</span>
                  <span className="font-bold text-white">${hourlyRate}/hr</span>
                </div>
                <input
                  type="range"
                  min="30"
                  max="150"
                  value={hourlyRate}
                  onChange={(e) => setHourlyRate(Number(e.target.value))}
                  className="w-full accent-purple-500 cursor-pointer"
                />
              </div>
            </div>

            {/* Calculated Results Box */}
            <div className="p-4 rounded-xl bg-slate-950/80 border border-white/10 grid grid-cols-2 gap-4">
              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400">Annual AE Time Saved</span>
                <div className="text-xl font-extrabold text-cyan-300 mt-0.5">
                  {(weeklyHoursSaved * 52).toLocaleString()} hrs
                </div>
              </div>

              <div>
                <span className="text-[10px] uppercase font-bold text-slate-400">Annual Net Savings</span>
                <div className="text-xl font-extrabold text-emerald-400 mt-0.5">
                  ${Math.round(annualSavings).toLocaleString()}
                </div>
              </div>
            </div>

            <div className="mt-4 flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-white/5">
              <span>Estimated Agent Token Cost / yr:</span>
              <span className="text-white font-mono font-bold">${Math.round(annualAgentCost)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
