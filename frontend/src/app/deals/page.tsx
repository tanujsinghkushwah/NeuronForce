'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import { api } from '../../lib/api';
import { Deal, DealStage, PipelineView, Priority } from '../../types/crm';
import {
  Kanban,
  Plus,
  Search,
  Filter,
  DollarSign,
  TrendingUp,
  Building,
  Sparkles,
  GripVertical,
  MoreHorizontal,
  ChevronRight,
  CheckCircle2,
  X,
  AlertCircle
} from 'lucide-react';

interface StageConfig {
  key: DealStage;
  label: string;
  color: string;
  dotColor: string;
}

const STAGES: StageConfig[] = [
  { key: 'prospecting', label: 'Prospecting', color: 'border-blue-500/30 bg-blue-500/5', dotColor: 'bg-blue-400' },
  { key: 'qualification', label: 'Qualification', color: 'border-indigo-500/30 bg-indigo-500/5', dotColor: 'bg-indigo-400' },
  { key: 'proposal', label: 'Proposal', color: 'border-purple-500/30 bg-purple-500/5', dotColor: 'bg-purple-400' },
  { key: 'negotiation', label: 'Negotiation', color: 'border-amber-500/30 bg-amber-500/5', dotColor: 'bg-amber-400' },
  { key: 'closed_won', label: 'Closed Won', color: 'border-emerald-500/30 bg-emerald-500/5', dotColor: 'bg-emerald-400' },
  { key: 'closed_lost', label: 'Closed Lost', color: 'border-rose-500/30 bg-rose-500/5', dotColor: 'bg-rose-400' },
];

export default function DealsPage() {
  const [pipeline, setPipeline] = useState<PipelineView | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [search, setSearch] = useState('');
  const [newDeal, setNewDeal] = useState({
    title: '',
    value: 100000,
    stage: 'prospecting' as DealStage,
    probability: 25,
    company: '',
    owner: 'Alex Rivera',
    priority: 'medium' as Priority
  });

  const loadPipeline = async () => {
    try {
      setLoading(true);
      const data = await api.getPipeline();
      setPipeline(data);
    } catch {
      // Fallback realistic pipeline
      setPipeline({
        total_value: 3850000,
        weighted_value: 2140000,
        stages: {
          prospecting: [
            { id: 101, title: 'Inbound Pilot Evaluation', value: 45000, company: 'Apex Media', probability: 10, owner: 'Sam Taylor', priority: 'medium', ai_win_probability: 0.35, tags: ['pilot'], contacts: [] },
            { id: 102, title: 'RevOps Platform Audit', value: 75000, company: 'Starlight Retail', probability: 15, owner: 'Alex Rivera', priority: 'high', ai_win_probability: 0.42, tags: ['audit'], contacts: [] },
          ],
          qualification: [
            { id: 201, title: 'Enterprise Data Migration', value: 240000, company: 'Fintech Vanguard', probability: 30, owner: 'Jordan Lee', priority: 'high', ai_win_probability: 0.62, tags: ['migration'], contacts: [] },
            { id: 202, title: 'Cloud Infrastructure Upgrade', value: 180000, company: 'NextWave Logistics', probability: 35, owner: 'Sarah Chen', priority: 'medium', ai_win_probability: 0.58, tags: ['cloud'], contacts: [] },
          ],
          proposal: [
            { id: 301, title: 'Multi-Tenant CRM Modernization', value: 320000, company: 'OmniGlobal Inc', probability: 50, owner: 'Alex Rivera', priority: 'high', ai_win_probability: 0.74, tags: ['enterprise'], contacts: [] },
            { id: 302, title: 'Support Automation License', value: 160000, company: 'HealthTech Direct', probability: 55, owner: 'Jordan Lee', priority: 'medium', ai_win_probability: 0.69, tags: ['automation'], contacts: [] },
          ],
          negotiation: [
            { id: 401, title: 'Global Enterprise AI Automation', value: 450000, company: 'HyperScale Corp', probability: 80, owner: 'Alex Rivera', priority: 'critical', ai_win_probability: 0.88, tags: ['ai-core', 'q4-commit'], contacts: [] },
            { id: 402, title: 'Autonomous Agent Mesh Expansion', value: 680000, company: 'CyberGuard Systems', probability: 85, owner: 'Sarah Chen', priority: 'critical', ai_win_probability: 0.91, tags: ['expansion'], contacts: [] },
          ],
          closed_won: [
            { id: 501, title: 'Core CRM Platform Tier 1', value: 550000, company: 'Titan Industries', probability: 100, owner: 'Alex Rivera', priority: 'high', ai_win_probability: 1.0, tags: ['closed'], contacts: [] },
            { id: 502, title: 'AI Agent Production Rollout', value: 420000, company: 'Nexus Capital', probability: 100, owner: 'Sam Taylor', priority: 'high', ai_win_probability: 1.0, tags: ['closed'], contacts: [] },
          ],
          closed_lost: [
            { id: 601, title: 'Legacy Replacement RFP', value: 350000, company: 'Tradition Bank', probability: 0, owner: 'Jordan Lee', priority: 'medium', ai_win_probability: 0.12, tags: ['budget-freeze'], contacts: [] },
          ]
        }
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPipeline();
  }, []);

  const [draggedDeal, setDraggedDeal] = useState<{ id: number; fromStage: DealStage } | null>(null);
  const [dragOverStage, setDragOverStage] = useState<DealStage | null>(null);

  const handleDropOnStage = async (targetStage: DealStage) => {
    if (!draggedDeal) return;
    const { id: dealId, fromStage } = draggedDeal;
    setDragOverStage(null);
    setDraggedDeal(null);

    if (fromStage === targetStage) return;

    const probMap: Record<DealStage, number> = {
      prospecting: 10,
      qualification: 25,
      proposal: 50,
      negotiation: 75,
      closed_won: 100,
      closed_lost: 0
    };
    const newProb = probMap[targetStage] ?? 25;

    // Optimistic local update
    if (pipeline) {
      const nextStages = { ...pipeline.stages };
      let movedItem: any = null;
      for (const k in nextStages) {
        const idx = nextStages[k].findIndex(d => d.id === dealId);
        if (idx !== -1) {
          movedItem = { ...nextStages[k][idx], stage: targetStage, probability: newProb };
          nextStages[k] = nextStages[k].filter(d => d.id !== dealId);
          break;
        }
      }
      if (movedItem) {
        if (!nextStages[targetStage]) nextStages[targetStage] = [];
        nextStages[targetStage] = [movedItem, ...nextStages[targetStage]];

        let totalVal = 0;
        let weightedVal = 0;
        for (const k in nextStages) {
          for (const d of nextStages[k]) {
            if (k !== 'closed_won' && k !== 'closed_lost') {
              totalVal += d.value || 0;
              weightedVal += ((d.value || 0) * (d.probability || 0)) / 100;
            }
          }
        }
        setPipeline({
          stages: nextStages,
          total_value: totalVal,
          weighted_value: Math.round(weightedVal)
        });
      }
    }

    try {
      await api.updateDeal(dealId, { stage: targetStage, probability: newProb });
      loadPipeline();
    } catch (err) {
      console.error('Failed to update deal stage:', err);
      loadPipeline();
    }
  };

  const handleCreateDeal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createDeal(newDeal);
      setShowCreateModal(false);
      loadPipeline();
    } catch (err) {
      alert('Could not create deal: ' + String(err));
    }
  };

  return (
    <div className="flex-1 flex flex-col pb-12">
      <Header
        title="Interactive Pipeline &amp; Kanban"
        subtitle="Manage deal velocity, stage progression, and AI win probabilities"
        onActionClick={() => setShowCreateModal(true)}
      />

      <div className="p-6 md:p-8 space-y-6 max-w-[1600px] mx-auto w-full">
        {/* Pipeline Summary Metrics Banner */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="glass-panel p-4 rounded-xl flex items-center justify-between border-indigo-500/20">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Total Pipeline Value</span>
              <div className="text-2xl font-extrabold text-white mt-0.5">
                ${((pipeline?.total_value || 0) / 1000).toLocaleString()}k
              </div>
            </div>
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold">
              <DollarSign className="w-5 h-5" />
            </div>
          </div>

          <div className="glass-panel p-4 rounded-xl flex items-center justify-between border-cyan-500/20">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-cyan-400">Weighted Forecast Value</span>
              <div className="text-2xl font-extrabold text-white mt-0.5">
                ${((pipeline?.weighted_value || 0) / 1000).toLocaleString()}k
              </div>
            </div>
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold">
              <TrendingUp className="w-5 h-5" />
            </div>
          </div>

          <div className="glass-panel p-4 rounded-xl flex items-center justify-between border-emerald-500/20">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Active Opportunities</span>
              <div className="text-2xl font-extrabold text-white mt-0.5">
                {Object.values(pipeline?.stages || {}).reduce((acc, list) => acc + list.length, 0)} Deals
              </div>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md flex items-center gap-1.5 cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>New Deal</span>
            </button>
          </div>
        </div>

        {/* Kanban Board Columns Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 items-start">
          {STAGES.map((st) => {
            const stageDeals = (pipeline?.stages?.[st.key] || []).filter(d =>
              search ? d.title.toLowerCase().includes(search.toLowerCase()) || (d.company && d.company.toLowerCase().includes(search.toLowerCase())) : true
            );
            const stageTotal = stageDeals.reduce((sum, d) => sum + (d.value || 0), 0);

            return (
              <div
                key={st.key}
                onDragOver={(e) => {
                  e.preventDefault();
                  e.dataTransfer.dropEffect = 'move';
                  if (dragOverStage !== st.key) setDragOverStage(st.key);
                }}
                onDragLeave={(e) => {
                  if (!e.currentTarget.contains(e.relatedTarget as Node)) {
                    setDragOverStage(null);
                  }
                }}
                onDrop={(e) => {
                  e.preventDefault();
                  handleDropOnStage(st.key);
                }}
                className={`rounded-2xl border transition-all flex flex-col max-h-[800px] ${
                  dragOverStage === st.key && draggedDeal?.fromStage !== st.key
                    ? 'border-indigo-400/80 bg-indigo-950/40 shadow-xl shadow-indigo-500/10 ring-2 ring-indigo-500/40'
                    : 'border-white/10 bg-slate-900/60 backdrop-blur-md'
                }`}
              >
                {/* Column Header */}
                <div className={`p-3.5 border-b border-white/10 rounded-t-2xl flex items-center justify-between ${st.color}`}>
                  <div className="flex items-center gap-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${st.dotColor}`}></span>
                    <span className="text-xs font-bold text-white tracking-tight">{st.label}</span>
                  </div>
                  <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-semibold border border-white/10">
                    {stageDeals.length}
                  </span>
                </div>

                {/* Subheader: Stage Value */}
                <div className="px-3.5 py-2 bg-slate-950/40 text-[11px] text-slate-400 border-b border-white/5 flex items-center justify-between">
                  <span>Stage Total:</span>
                  <span className="text-white font-semibold">${(stageTotal / 1000).toFixed(0)}k</span>
                </div>

                {/* Deal Cards Container */}
                <div className="p-3 space-y-3 overflow-y-auto flex-1 min-h-[300px]">
                  {dragOverStage === st.key && draggedDeal?.fromStage !== st.key && (
                    <div className="p-3.5 rounded-xl border-2 border-dashed border-indigo-400/60 bg-indigo-500/15 text-center text-xs text-indigo-300 font-semibold animate-pulse">
                      Drop here to move to {st.label}
                    </div>
                  )}

                  {stageDeals.length === 0 ? (
                    <div className="py-12 text-center text-xs text-slate-400 border border-dashed border-white/10 rounded-xl">
                      No deals in {st.label.toLowerCase()}
                    </div>
                  ) : (
                    stageDeals.map((deal) => {
                      const isDraggingThis = draggedDeal?.id === deal.id;
                      return (
                        <div
                          key={deal.id}
                          draggable={true}
                          onDragStart={(e) => {
                            e.dataTransfer.setData('text/plain', String(deal.id));
                            e.dataTransfer.effectAllowed = 'move';
                            setDraggedDeal({ id: deal.id, fromStage: st.key });
                          }}
                          onDragEnd={() => {
                            setDraggedDeal(null);
                            setDragOverStage(null);
                          }}
                          className={`glass-panel-interactive p-3.5 rounded-xl border border-white/10 space-y-2.5 group cursor-grab active:cursor-grabbing transition-all ${
                            isDraggingThis ? 'opacity-40 scale-[0.98] border-indigo-500 ring-2 ring-indigo-500/30' : ''
                          }`}
                        >
                          <div className="flex items-start justify-between gap-2">
                            <h4 className="text-xs font-bold text-white group-hover:text-indigo-300 transition-colors line-clamp-2">
                              {deal.title}
                            </h4>
                            <div className="flex items-center gap-1 shrink-0">
                              {deal.priority === 'critical' && (
                                <span className="text-[9px] px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold uppercase">
                                  HOT
                                </span>
                              )}
                              <GripVertical className="w-3.5 h-3.5 text-slate-500 group-hover:text-slate-300" />
                            </div>
                          </div>

                          {deal.company && (
                            <div className="text-[11px] text-slate-400 flex items-center gap-1.5">
                              <Building className="w-3 h-3 text-slate-400" />
                              <span>{deal.company}</span>
                            </div>
                          )}

                          <div className="flex items-center justify-between pt-1">
                            <span className="text-sm font-extrabold text-white">
                              ${Number(deal.value).toLocaleString()}
                            </span>

                            <div className="flex items-center gap-1 text-[11px] font-bold text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded-md border border-cyan-500/20">
                              <Sparkles className="w-2.5 h-2.5 text-cyan-400" />
                              <span>{deal.ai_win_probability ? `${Math.round(deal.ai_win_probability * 100)}%` : `${deal.probability}%`}</span>
                            </div>
                          </div>

                          {/* Owner & Drag Info */}
                          <div className="flex items-center justify-between pt-2 border-t border-white/5 text-[10px] text-slate-400">
                            <span>{deal.owner || 'Unassigned'}</span>
                            <span className="text-[9px] text-slate-500 group-hover:text-indigo-400 transition-colors">
                              Drag to move
                            </span>
                          </div>
                        </div>
                      );
                    })
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* New Deal Modal */}
      {showCreateModal && (
        <div
          onClick={(e) => {
            if (e.target === e.currentTarget) setShowCreateModal(false);
          }}
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto"
        >
          <div className="glass-dropdown w-full max-w-md p-6 rounded-2xl border border-white/20 animate-in fade-in zoom-in-95 duration-200 my-auto">
            <h3 className="text-lg font-bold text-white mb-1">Add Opportunity</h3>
            <p className="text-xs text-slate-400 mb-4">New deals automatically integrate with the AI Win Probability engine.</p>

            <form onSubmit={handleCreateDeal} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-medium text-slate-300 mb-1">Deal Title</label>
                <input
                  required
                  type="text"
                  placeholder="e.g. Enterprise Cloud Security Package"
                  value={newDeal.title}
                  onChange={(e) => setNewDeal({ ...newDeal, title: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Value (USD)</label>
                  <input
                    required
                    type="number"
                    min="1"
                    value={newDeal.value}
                    onChange={(e) => setNewDeal({ ...newDeal, value: Number(e.target.value) })}
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Company</label>
                  <input
                    required
                    type="text"
                    placeholder="e.g. Acme Inc"
                    value={newDeal.company}
                    onChange={(e) => setNewDeal({ ...newDeal, company: e.target.value })}
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Stage</label>
                  <select
                    value={newDeal.stage}
                    onChange={(e) => setNewDeal({ ...newDeal, stage: e.target.value as any })}
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  >
                    <option value="prospecting">Prospecting</option>
                    <option value="qualification">Qualification</option>
                    <option value="proposal">Proposal</option>
                    <option value="negotiation">Negotiation</option>
                    <option value="closed_won">Closed Won</option>
                  </select>
                </div>
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Owner</label>
                  <input
                    type="text"
                    value={newDeal.owner}
                    onChange={(e) => setNewDeal({ ...newDeal, owner: e.target.value })}
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
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
                  Save Opportunity
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
