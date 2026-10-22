"use client";

import React from "react";
import { CalendarEvent } from "../../types/crm";
import {
  X,
  Clock,
  Video,
  MapPin,
  Users,
  Trash2,
  Calendar,
  ExternalLink,
  ShieldCheck,
} from "lucide-react";

interface EventDetailModalProps {
  event: CalendarEvent | null;
  onClose: () => void;
  onDelete: (id: number) => void;
}

export default function EventDetailModal({
  event,
  onClose,
  onDelete,
}: EventDetailModalProps) {
  if (!event) return null;

  const startDate = new Date(event.start_time);
  const endDate = new Date(event.end_time);

  const formatTime = (d: Date) =>
    d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  const formatDate = (d: Date) =>
    d.toLocaleDateString(undefined, {
      weekday: "long",
      month: "short",
      day: "numeric",
      year: "numeric",
    });

  const isVideoCall =
    event.location?.toLowerCase().includes("zoom") ||
    event.location?.toLowerCase().includes("meet") ||
    event.location?.toLowerCase().includes("teams");

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="glass-dropdown w-full max-w-lg p-6 rounded-2xl border border-white/20 shadow-2xl relative">
        {/* Top Header bar with color accent */}
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex items-center gap-2.5">
            <span
              className="w-3.5 h-3.5 rounded-full ring-4"
              style={{
                backgroundColor: event.color || "#6366f1",
                boxShadow: `0 0 12px ${event.color || "#6366f1"}80`,
              }}
            />
            <span
              className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border"
              style={{
                borderColor: event.color || "#6366f1",
                color: event.color || "#6366f1",
                backgroundColor: `${event.color || "#6366f1"}15`,
              }}
            >
              {event.event_type}
            </span>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => {
                if (confirm(`Cancel and delete meeting "${event.title}"?`)) {
                  onDelete(event.id);
                  onClose();
                }
              }}
              title="Delete engagement"
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
            >
              <Trash2 className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-white mb-2 leading-snug">
          {event.title}
        </h3>

        {/* Description / Agenda */}
        {event.description && (
          <p className="text-xs text-slate-300 leading-relaxed mb-5 p-3 rounded-xl bg-white/[0.03] border border-white/5">
            {event.description}
          </p>
        )}

        {/* Meeting Specs */}
        <div className="space-y-3.5 text-xs text-slate-200 mb-6">
          {/* Date & Time */}
          <div className="flex items-start gap-3">
            <Calendar className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <div>
              <div className="font-semibold text-white">
                {formatDate(startDate)}
              </div>
              <div className="text-slate-400 text-[11px] flex items-center gap-1.5 mt-0.5">
                <Clock className="w-3 h-3 text-slate-400" />
                <span>
                  {formatTime(startDate)} – {formatTime(endDate)}
                </span>
                <span className="text-slate-500">•</span>
                <span>
                  {Math.round(
                    (endDate.getTime() - startDate.getTime()) / 60000,
                  )}{" "}
                  mins
                </span>
              </div>
            </div>
          </div>

          {/* Location / Meeting Room */}
          {event.location && (
            <div className="flex items-start gap-3">
              {isVideoCall ? (
                <Video className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
              ) : (
                <MapPin className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              )}
              <div className="flex-1 flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white">
                    {event.location}
                  </div>
                  <div className="text-slate-400 text-[11px]">
                    {isVideoCall
                      ? "Virtual Video Conference Room"
                      : "In-person / Phone"}
                  </div>
                </div>

                {isVideoCall && (
                  <button
                    onClick={() =>
                      alert(`Launching ${event.location} video room...`)
                    }
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 font-medium text-[11px] transition-all cursor-pointer"
                  >
                    <span>Join</span>
                    <ExternalLink className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Attendees */}
          {event.attendees && event.attendees.length > 0 && (
            <div className="flex items-start gap-3">
              <Users className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <div className="flex-1">
                <div className="font-semibold text-white mb-1.5">
                  Confirmed Attendees ({event.attendees.length})
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {event.attendees.map((attendee, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-[11px] text-slate-300"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                      <span>{attendee}</span>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* CRM Deal / Opportunity status */}
          <div className="flex items-center gap-2 p-2.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-[11px]">
            <ShieldCheck className="w-4 h-4 text-indigo-400 shrink-0" />
            <span>
              Synced with Salesforce-compatible pipeline opportunity timeline
            </span>
          </div>
        </div>

        {/* Action footer */}
        <div className="flex items-center justify-end gap-2.5 pt-4 border-t border-white/10">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-semibold transition-all cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
