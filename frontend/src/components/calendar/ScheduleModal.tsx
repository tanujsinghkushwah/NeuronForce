"use client";

import React from "react";
import { X, Calendar as CalendarIcon, Clock, Users, Video } from "lucide-react";

interface ScheduleModalProps {
  show: boolean;
  onClose: () => void;
  onSubmit: (e: React.FormEvent) => void;
  form: {
    title: string;
    start_time: string;
    end_time: string;
    location: string;
    event_type: string;
    attendees: string;
    color: string;
    description?: string;
  };
  setForm: React.Dispatch<
    React.SetStateAction<{
      title: string;
      start_time: string;
      end_time: string;
      location: string;
      event_type: string;
      attendees: string;
      color: string;
      description?: string;
    }>
  >;
}

export default function ScheduleModal({
  show,
  onClose,
  onSubmit,
  form,
  setForm,
}: ScheduleModalProps) {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="glass-dropdown w-full max-w-lg p-6 rounded-2xl border border-white/20 text-xs shadow-2xl relative">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="text-lg font-bold text-white tracking-tight">
              Schedule Executive Engagement
            </h3>
            <p className="text-slate-400 text-xs">
              Add a customer meeting, solution demo, or contract review.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={onSubmit} className="space-y-4">
          <div>
            <label className="block font-medium text-slate-300 mb-1">
              Meeting Title
            </label>
            <input
              required
              type="text"
              placeholder="e.g. Solution Demo & Architecture Walkthrough"
              value={form.title}
              onChange={(e) =>
                setForm((f) => ({ ...f, title: e.target.value }))
              }
              className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all text-xs"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Start Time
              </label>
              <input
                required
                type="datetime-local"
                value={form.start_time}
                onChange={(e) =>
                  setForm((f) => ({ ...f, start_time: e.target.value }))
                }
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-all text-xs"
              />
            </div>
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                End Time
              </label>
              <input
                required
                type="datetime-local"
                value={form.end_time}
                onChange={(e) =>
                  setForm((f) => ({ ...f, end_time: e.target.value }))
                }
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-all text-xs"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Type
              </label>
              <select
                value={form.event_type}
                onChange={(e) =>
                  setForm((f) => ({ ...f, event_type: e.target.value }))
                }
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white focus:outline-none focus:border-indigo-500 transition-all text-xs"
              >
                <option value="meeting">Executive Meeting</option>
                <option value="demo">Product Demo</option>
                <option value="follow_up">Deal Follow-up</option>
                <option value="presentation">QBR / Presentation</option>
                <option value="review">Contract Review</option>
              </select>
            </div>
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Badge Color
              </label>
              <div className="flex items-center gap-2 mt-1">
                {[
                  "#6366f1",
                  "#10b981",
                  "#f59e0b",
                  "#8b5cf6",
                  "#ef4444",
                  "#06b6d4",
                ].map((col) => (
                  <button
                    key={col}
                    type="button"
                    onClick={() => setForm((f) => ({ ...f, color: col }))}
                    className={`w-6 h-6 rounded-full border-2 transition-transform cursor-pointer ${
                      form.color === col
                        ? "border-white scale-110 shadow-md"
                        : "border-transparent hover:scale-105"
                    }`}
                    style={{ backgroundColor: col }}
                  />
                ))}
              </div>
            </div>
          </div>

          <div>
            <label className="block font-medium text-slate-300 mb-1">
              Location / Video Room
            </label>
            <input
              type="text"
              placeholder="e.g. Zoom Meeting / Google Meet"
              value={form.location}
              onChange={(e) =>
                setForm((f) => ({ ...f, location: e.target.value }))
              }
              className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all text-xs"
            />
          </div>

          <div>
            <label className="block font-medium text-slate-300 mb-1">
              Attendees (comma-separated emails)
            </label>
            <input
              type="text"
              placeholder="alex@neuronforce.ai, customer@megacorp.com"
              value={form.attendees}
              onChange={(e) =>
                setForm((f) => ({ ...f, attendees: e.target.value }))
              }
              className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-white/10 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-all text-xs"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-white/10">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs font-semibold transition-all cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
            >
              Confirm Engagement
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
