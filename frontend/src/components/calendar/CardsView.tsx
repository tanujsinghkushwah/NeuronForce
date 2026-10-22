"use client";

import React from "react";
import { CalendarEvent } from "../../types/crm";
import {
  Clock,
  Video,
  Trash2,
  MapPin,
  Users,
  Calendar,
  ArrowUpRight,
} from "lucide-react";

interface CardsViewProps {
  events: CalendarEvent[];
  onSelectEvent: (event: CalendarEvent) => void;
  onDeleteEvent: (id: number) => void;
}

export default function CardsView({
  events,
  onSelectEvent,
  onDeleteEvent,
}: CardsViewProps) {
  if (events.length === 0) {
    return (
      <div className="glass-panel p-16 rounded-3xl text-center border border-white/10 space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto">
          <Calendar className="w-6 h-6" />
        </div>
        <h3 className="text-base font-bold text-white">
          No Scheduled Engagements
        </h3>
        <p className="text-xs text-slate-400 max-w-sm mx-auto">
          Click "+ Schedule" in the top toolbar to organize a client meeting,
          demo, or follow-up.
        </p>
      </div>
    );
  }

  // Helper to calculate readable duration (e.g., '45 mins' or '1 hr 15 mins')
  const getDurationString = (startIso: string, endIso: string) => {
    const start = new Date(startIso).getTime();
    const end = new Date(endIso).getTime();
    const diffMins = Math.max(0, Math.round((end - start) / (1000 * 60)));

    if (diffMins < 60) return `${diffMins} mins`;
    const hrs = Math.floor(diffMins / 60);
    const mins = diffMins % 60;
    return mins > 0 ? `${hrs}h ${mins}m` : `${hrs} hr${hrs > 1 ? "s" : ""}`;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      {events.map((evt) => {
        const startDate = new Date(evt.start_time);
        const endDate = new Date(evt.end_time);

        const dateStr = startDate.toLocaleDateString(undefined, {
          weekday: "short",
          month: "short",
          day: "numeric",
          year: "numeric",
        });

        const startTimeStr = startDate.toLocaleTimeString([], {
          hour: "numeric",
          minute: "2-digit",
        });

        const endTimeStr = endDate.toLocaleTimeString([], {
          hour: "numeric",
          minute: "2-digit",
        });

        const durationStr = getDurationString(evt.start_time, evt.end_time);
        const color = evt.color || "#6366f1";

        const isVideoMeeting =
          evt.location?.toLowerCase().includes("zoom") ||
          evt.location?.toLowerCase().includes("meet") ||
          evt.location?.toLowerCase().includes("teams") ||
          evt.location?.toLowerCase().includes("virtual");

        return (
          <div
            key={evt.id}
            onClick={() => onSelectEvent(evt)}
            className="glass-panel p-6 rounded-2xl border border-white/10 flex flex-col justify-between hover:border-indigo-500/50 hover:shadow-xl hover:shadow-indigo-500/10 transition-all duration-200 group cursor-pointer relative overflow-hidden"
            style={{
              borderLeft: `4px solid ${color}`,
            }}
          >
            {/* Top Row: Event Type Badge + Duration + Delete Action */}
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <div className="flex items-center gap-2 flex-wrap">
                  <span
                    className="text-[10px] uppercase font-extrabold px-2.5 py-0.5 rounded-full border tracking-wider"
                    style={{
                      borderColor: `${color}60`,
                      color: color,
                      backgroundColor: `${color}15`,
                    }}
                  >
                    {evt.event_type.replace("_", " ")}
                  </span>

                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-slate-300">
                    {durationStr}
                  </span>
                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm(`Delete meeting "${evt.title}"?`)) {
                        onDeleteEvent(evt.id);
                      }
                    }}
                    title="Delete meeting"
                    className="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-500/10 transition-colors cursor-pointer"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>

              {/* Title: Full sizing, no awkward trimming */}
              <h4 className="text-base font-bold text-white group-hover:text-indigo-300 transition-colors mb-2 break-words leading-snug">
                {evt.title}
              </h4>

              {/* Description: Generous multi-line preview */}
              {evt.description && (
                <p className="text-xs text-slate-300 leading-relaxed mb-4 line-clamp-3">
                  {evt.description}
                </p>
              )}
            </div>

            {/* Bottom Section: Date, Time, Location & Full Attendees */}
            <div className="space-y-3 pt-4 border-t border-white/10 text-xs">
              {/* Date & Time Range */}
              <div className="flex items-center gap-2.5 text-xs text-slate-200">
                <div className="w-6 h-6 rounded-lg bg-indigo-500/15 border border-indigo-500/30 flex items-center justify-center shrink-0 text-indigo-400">
                  <Clock className="w-3.5 h-3.5" />
                </div>
                <div className="flex flex-col">
                  <span className="font-semibold text-white">{dateStr}</span>
                  <span className="text-[11px] text-slate-400">
                    {startTimeStr} – {endTimeStr}
                  </span>
                </div>
              </div>

              {/* Location */}
              {evt.location && (
                <div className="flex items-center gap-2.5 text-xs text-slate-300">
                  <div className="w-6 h-6 rounded-lg bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center shrink-0 text-cyan-400">
                    {isVideoMeeting ? (
                      <Video className="w-3.5 h-3.5" />
                    ) : (
                      <MapPin className="w-3.5 h-3.5" />
                    )}
                  </div>
                  <span className="break-words font-medium text-slate-300">
                    {evt.location}
                  </span>
                </div>
              )}

              {/* Attendees: Full width chips, no 130px truncation */}
              {evt.attendees && evt.attendees.length > 0 && (
                <div className="pt-1">
                  <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 mb-1.5">
                    <Users className="w-3 h-3 text-indigo-400" />
                    <span>Participants ({evt.attendees.length}):</span>
                  </div>

                  <div className="flex items-center gap-1.5 flex-wrap">
                    {evt.attendees.map((att, idx) => (
                      <span
                        key={idx}
                        className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-800/90 hover:bg-slate-700/90 text-slate-200 border border-white/10 font-medium transition-colors"
                      >
                        {att}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* View Details Click affordance */}
              <div className="pt-2 flex items-center justify-end text-[11px] font-medium text-indigo-400 group-hover:text-cyan-300 transition-colors">
                <span>View engagement details</span>
                <ArrowUpRight className="w-3.5 h-3.5 ml-0.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
