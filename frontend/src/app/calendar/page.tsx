'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import { api } from '../../lib/api';
import { CalendarEvent } from '../../types/crm';
import {
  Calendar as CalendarIcon,
  Clock,
  Plus,
  Users,
  Video,
  MapPin,
  Trash2,
  ChevronLeft,
  ChevronRight,
  Sparkles
} from 'lucide-react';

export default function CalendarPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({
    title: '',
    start_time: '',
    end_time: '',
    location: 'Zoom Meeting',
    event_type: 'meeting',
    attendees: 'alex@neuronforce.ai, customer@acme.com',
    color: '#6366f1'
  });

  const openNewEventModal = () => {
    const start = new Date(Date.now() + 86400000).toISOString().slice(0, 16);
    const end = new Date(Date.now() + 90000000).toISOString().slice(0, 16);
    setForm(f => ({ ...f, start_time: start, end_time: end }));
    setShowModal(true);
  };

  const loadEvents = async () => {
    try {
      setLoading(true);
      const data = await api.getCalendarEvents();
      setEvents(data);
    } catch {
      // Fallback realistic calendar events
      setEvents([
        {
          id: 1,
          title: 'Enterprise Architecture QBR with HyperScale',
          description: 'Review migration from legacy Salesforce instance to NeuronForce with VP Eng.',
          start_time: '2026-10-22T14:00:00Z',
          end_time: '2026-10-22T15:00:00Z',
          location: 'Zoom Virtual Room',
          event_type: 'meeting',
          attendees: ['elena@hyperscale.ai', 'alex@neuronforce.ai'],
          color: '#6366f1',
          is_all_day: false,
          reminder_minutes: 15,
          created_at: '2026-10-20T10:00:00Z',
          updated_at: '2026-10-20T10:00:00Z'
        },
        {
          id: 2,
          title: 'POC Technical Deep Dive: Autonomous Agents',
          description: 'Hands-on review of lead scoring and email generative agents with RevOps team.',
          start_time: '2026-10-23T16:30:00Z',
          end_time: '2026-10-23T17:30:00Z',
          location: 'Google Meet',
          event_type: 'demo',
          attendees: ['marcus@innovatetech.io', 'jordan@neuronforce.ai'],
          color: '#f59e0b',
          is_all_day: false,
          reminder_minutes: 15,
          created_at: '2026-10-20T11:00:00Z',
          updated_at: '2026-10-20T11:00:00Z'
        },
        {
          id: 3,
          title: 'Contract Signing & Security Governance Review',
          description: 'Final security governance checklist approval with legal.',
          start_time: '2026-10-24T10:00:00Z',
          end_time: '2026-10-24T10:45:00Z',
          location: 'Teams Meeting',
          event_type: 'follow_up',
          attendees: ['sarah@cloudops.com', 'legal@neuronforce.ai'],
          color: '#10b981',
          is_all_day: false,
          reminder_minutes: 15,
          created_at: '2026-10-20T12:00:00Z',
          updated_at: '2026-10-20T12:00:00Z'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createCalendarEvent({
        title: form.title,
        start_time: new Date(form.start_time).toISOString(),
        end_time: new Date(form.end_time).toISOString(),
        location: form.location,
        event_type: form.event_type,
        color: form.color,
        attendees: form.attendees.split(',').map(a => a.trim()).filter(Boolean)
      });
      setShowModal(false);
      loadEvents();
    } catch (err) {
      alert('Could not schedule event: ' + String(err));
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.deleteCalendarEvent(id);
      setEvents(events.filter(e => e.id !== id));
    } catch {
      setEvents(events.filter(e => e.id !== id));
    }
  };

  return (
    <div className="flex-1 flex flex-col pb-12">
      <Header
        title="Executive Calendar &amp; Engagements"
        subtitle="Customer meeting schedules synchronized across deal timelines"
        onActionClick={openNewEventModal}
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto w-full">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">
              Upcoming Executive Engagements
            </h2>
            <p className="text-xs text-slate-400">
              High-priority customer meetings linked directly to pipeline opportunities
            </p>
          </div>

          <button
            onClick={openNewEventModal}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
          >
            <Plus className="w-4 h-4" />
            <span>Schedule Meeting</span>
          </button>
        </div>

        {/* Events Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {events.map((evt) => (
            <div
              key={evt.id}
              className="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col justify-between hover:border-indigo-500/30 transition-all group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span
                    className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border"
                    style={{
                      borderColor: evt.color,
                      color: evt.color,
                      backgroundColor: `${evt.color}15`
                    }}
                  >
                    {evt.event_type}
                  </span>
                  <button
                    onClick={() => handleDelete(evt.id)}
                    className="text-slate-500 hover:text-rose-400 p-1 rounded-md transition-colors cursor-pointer"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors mb-2">
                  {evt.title}
                </h4>

                {evt.description && (
                  <p className="text-xs text-slate-400 leading-relaxed mb-4">
                    {evt.description}
                  </p>
                )}
              </div>

              <div className="space-y-2 pt-3 border-t border-white/5 text-xs text-slate-300">
                <div className="flex items-center gap-2 text-[11px] text-slate-400">
                  <Clock className="w-3.5 h-3.5 text-indigo-400" />
                  <span>{new Date(evt.start_time).toLocaleString()}</span>
                </div>

                {evt.location && (
                  <div className="flex items-center gap-2 text-[11px] text-slate-400">
                    <Video className="w-3.5 h-3.5 text-cyan-400" />
                    <span>{evt.location}</span>
                  </div>
                )}

                {evt.attendees && evt.attendees.length > 0 && (
                  <div className="flex items-center gap-1.5 flex-wrap pt-1">
                    {evt.attendees.map((att, idx) => (
                      <span key={idx} className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-white/5">
                        {att}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* New Event Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-dropdown w-full max-w-md p-6 rounded-2xl border border-white/20 animate-in fade-in zoom-in-95 duration-200 text-xs">
            <h3 className="text-lg font-bold text-white mb-1">Schedule Engagement</h3>
            <p className="text-slate-400 mb-4">Add a customer meeting, demo, or contract review session.</p>

            <form onSubmit={handleCreate} className="space-y-3.5">
              <div>
                <label className="block font-medium text-slate-300 mb-1">Meeting Title</label>
                <input
                  required
                  type="text"
                  placeholder="e.g. Solution Demo & Architecture Walkthrough"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-medium text-slate-300 mb-1">Start Time</label>
                  <input
                    required
                    type="datetime-local"
                    value={form.start_time}
                    onChange={(e) => setForm({ ...form, start_time: e.target.value })}
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="block font-medium text-slate-300 mb-1">End Time</label>
                  <input
                    required
                    type="datetime-local"
                    value={form.end_time}
                    onChange={(e) => setForm({ ...form, end_time: e.target.value })}
                    className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Location / Video Link</label>
                <input
                  type="text"
                  value={form.location}
                  onChange={(e) => setForm({ ...form, location: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="block font-medium text-slate-300 mb-1">Attendees (comma separated)</label>
                <input
                  type="text"
                  value={form.attendees}
                  onChange={(e) => setForm({ ...form, attendees: e.target.value })}
                  className="w-full h-9 px-3 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 cursor-pointer"
                >
                  Save Meeting
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
