'use client';

import React from 'react';
import { CalendarEvent } from '../../types/crm';
import { Clock, Video, Trash2, MapPin, Users } from 'lucide-react';

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
      <div className="glass-panel p-12 rounded-2xl text-center border border-white/10">
        <p className="text-sm text-slate-400">No scheduled engagements found.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {events.map((evt) => {
        const startDate = new Date(evt.start_time);
        return (
          <div
            key={evt.id}
            onClick={() => onSelectEvent(evt)}
            className="glass-panel p-5 rounded-2xl border border-white/10 flex flex-col justify-between hover:border-indigo-500/40 hover:shadow-lg hover:shadow-indigo-500/10 transition-all group cursor-pointer"
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <span
                  className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border"
                  style={{
                    borderColor: evt.color || '#6366f1',
                    color: evt.color || '#6366f1',
                    backgroundColor: `${evt.color || '#6366f1'}15`,
                  }}
                >
                  {evt.event_type}
                </span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm(`Delete meeting "${evt.title}"?`)) {
                      onDeleteEvent(evt.id);
                    }
                  }}
                  className="text-slate-500 hover:text-rose-400 p-1 rounded-md transition-colors cursor-pointer"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>

              <h4 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors mb-2">
                {evt.title}
              </h4>

              {evt.description && (
                <p className="text-xs text-slate-400 leading-relaxed mb-4 line-clamp-2">
                  {evt.description}
                </p>
              )}
            </div>

            <div className="space-y-2 pt-3 border-t border-white/5 text-xs text-slate-300">
              <div className="flex items-center gap-2 text-[11px] text-slate-400">
                <Clock className="w-3.5 h-3.5 text-indigo-400" />
                <span>{startDate.toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}</span>
              </div>

              {evt.location && (
                <div className="flex items-center gap-2 text-[11px] text-slate-400">
                  <Video className="w-3.5 h-3.5 text-cyan-400" />
                  <span className="truncate">{evt.location}</span>
                </div>
              )}

              {evt.attendees && evt.attendees.length > 0 && (
                <div className="flex items-center gap-1.5 flex-wrap pt-1">
                  {evt.attendees.slice(0, 3).map((att, idx) => (
                    <span
                      key={idx}
                      className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-white/5 truncate max-w-[130px]"
                    >
                      {att}
                    </span>
                  ))}
                  {evt.attendees.length > 3 && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                      +{evt.attendees.length - 3}
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
