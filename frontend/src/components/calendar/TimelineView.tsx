'use client';

import React, { useMemo, useRef, useEffect } from 'react';
import { CalendarEvent } from '../../types/crm';
import { Video, Clock, MapPin, Plus } from 'lucide-react';

interface TimelineViewProps {
  events: CalendarEvent[];
  currentDate: Date;
  viewMode: 'week' | 'day';
  onSelectEvent: (event: CalendarEvent) => void;
  onSlotClick: (date: Date, hour: number) => void;
}

const START_HOUR = 7; // 7 AM
const END_HOUR = 22; // 10 PM
const TOTAL_HOURS = END_HOUR - START_HOUR; // 15 hours
const HOUR_HEIGHT = 64; // px per hour

export default function TimelineView({
  events,
  currentDate,
  viewMode,
  onSelectEvent,
  onSlotClick,
}: TimelineViewProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Compute days to display based on viewMode
  const days = useMemo(() => {
    if (viewMode === 'day') {
      const d = new Date(currentDate);
      d.setHours(0, 0, 0, 0);
      return [d];
    }

    // Week view: compute Monday through Sunday
    const d = new Date(currentDate);
    const dayOfWeek = d.getDay(); // 0 is Sunday, 1 is Monday...
    const diffToMonday = d.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
    const monday = new Date(d.setDate(diffToMonday));
    monday.setHours(0, 0, 0, 0);

    return Array.from({ length: 7 }, (_, i) => {
      const day = new Date(monday);
      day.setDate(monday.getDate() + i);
      return day;
    });
  }, [currentDate, viewMode]);

  // Current time marker (stable default for prerender, updated on client mount)
  const [mounted, setMounted] = React.useState(false);
  const [now, setNow] = React.useState<Date>(() => new Date('2026-10-22T12:00:00'));

  React.useEffect(() => {
    setMounted(true);
    setNow(new Date());
    const interval = setInterval(() => setNow(new Date()), 60000);
    return () => clearInterval(interval);
  }, []);

  const nowHour = now.getHours() + now.getMinutes() / 60;
  const isCurrentTimeInRange = nowHour >= START_HOUR && nowHour <= END_HOUR;
  const currentTimeTop = (nowHour - START_HOUR) * HOUR_HEIGHT;

  // Auto-scroll to near current time or first event on mount
  useEffect(() => {
    if (scrollContainerRef.current) {
      // Scroll to 8 AM or current time
      const targetScroll = Math.max(0, (Math.min(nowHour, 14) - START_HOUR - 1) * HOUR_HEIGHT);
      scrollContainerRef.current.scrollTop = targetScroll;
    }
  }, []);

  const isToday = (d: Date) => {
    if (!mounted) return false;
    return (
      d.getFullYear() === now.getFullYear() &&
      d.getMonth() === now.getMonth() &&
      d.getDate() === now.getDate()
    );
  };

  const hoursArray = Array.from({ length: TOTAL_HOURS }, (_, i) => START_HOUR + i);

  const formatHourLabel = (hour: number) => {
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const h = hour % 12 === 0 ? 12 : hour % 12;
    return `${h} ${ampm}`;
  };

  const DAY_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  return (
    <div className="glass-panel rounded-2xl border border-white/10 overflow-hidden flex flex-col shadow-2xl">
      {/* ── Days Header Bar ────────────────────────────────────────────── */}
      <div className="flex border-b border-white/10 bg-white/[0.02] backdrop-blur-md sticky top-0 z-20">
        {/* Timezone label header on left */}
        <div className="w-16 sm:w-20 shrink-0 p-3 flex flex-col justify-end border-r border-white/10 text-right pr-2">
          <span className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">
            GMT
          </span>
        </div>

        {/* Day Columns Header */}
        <div className={`flex-1 grid ${viewMode === 'day' ? 'grid-cols-1' : 'grid-cols-7'}`}>
          {days.map((day, idx) => {
            const today = isToday(day);
            const dayName = DAY_NAMES[day.getDay()];
            const dayNum = day.getDate();

            return (
              <div
                key={idx}
                className={`py-3 px-2 flex flex-col items-center justify-center border-r border-white/10 last:border-r-0 transition-colors ${
                  today ? 'bg-indigo-500/[0.07]' : ''
                }`}
              >
                <span
                  className={`text-[11px] font-bold uppercase tracking-wider mb-1 ${
                    today ? 'text-indigo-400' : 'text-slate-400'
                  }`}
                >
                  {dayName}
                </span>

                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all ${
                    today
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/40 ring-2 ring-indigo-400/50'
                      : 'text-slate-200 hover:bg-white/10'
                  }`}
                >
                  {dayNum}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Scrollable Hourly Timeline Grid ────────────────────────────── */}
      <div
        ref={scrollContainerRef}
        className="overflow-y-auto max-h-[660px] relative select-none"
        style={{ height: `${TOTAL_HOURS * HOUR_HEIGHT}px` }}
      >
        <div className="flex relative" style={{ height: `${TOTAL_HOURS * HOUR_HEIGHT}px` }}>
          {/* Time markers gutter (left) */}
          <div className="w-16 sm:w-20 shrink-0 border-r border-white/10 relative text-right pr-2">
            {hoursArray.map((hour, idx) => (
              <div
                key={hour}
                className="absolute right-2 text-[10px] font-semibold text-slate-400 -translate-y-1/2"
                style={{ top: `${idx * HOUR_HEIGHT}px` }}
              >
                {formatHourLabel(hour)}
              </div>
            ))}
          </div>

          {/* Timeline Grid Columns */}
          <div className={`flex-1 grid ${viewMode === 'day' ? 'grid-cols-1' : 'grid-cols-7'} relative`}>
            {/* Background Horizontal Hour Lines spanning all columns */}
            <div className="absolute inset-0 pointer-events-none z-0">
              {hoursArray.map((hour, idx) => (
                <div
                  key={hour}
                  className="absolute inset-x-0 border-t border-white/[0.06]"
                  style={{ top: `${idx * HOUR_HEIGHT}px` }}
                >
                  {/* Half-hour dashed divider */}
                  <div
                    className="absolute inset-x-0 border-t border-dashed border-white/[0.025]"
                    style={{ top: `${HOUR_HEIGHT / 2}px` }}
                  />
                </div>
              ))}
            </div>

            {/* Day Columns */}
            {days.map((day, dayIndex) => {
              const today = isToday(day);

              // Filter events for this day
              const dayEvents = events.filter((e) => {
                const eStart = new Date(e.start_time);
                return (
                  eStart.getFullYear() === day.getFullYear() &&
                  eStart.getMonth() === day.getMonth() &&
                  eStart.getDate() === day.getDate()
                );
              });

              return (
                <div
                  key={dayIndex}
                  className={`relative border-r border-white/10 last:border-r-0 ${
                    today ? 'bg-indigo-500/[0.03]' : ''
                  }`}
                  style={{ height: `${TOTAL_HOURS * HOUR_HEIGHT}px` }}
                >
                  {/* Clickable slot layers for scheduling */}
                  {hoursArray.map((hour, hourIdx) => (
                    <div
                      key={hour}
                      onClick={() => onSlotClick(day, hour)}
                      className="absolute inset-x-0 hover:bg-white/[0.03] transition-colors cursor-pointer group flex items-start justify-end pr-1 pt-1"
                      style={{
                        top: `${hourIdx * HOUR_HEIGHT}px`,
                        height: `${HOUR_HEIGHT}px`,
                      }}
                      title={`Click to schedule engagement at ${formatHourLabel(hour)}`}
                    >
                      <span className="opacity-0 group-hover:opacity-100 text-[10px] text-slate-500 font-medium px-1 rounded bg-black/40 pointer-events-none transition-opacity">
                        + Add
                      </span>
                    </div>
                  ))}

                  {/* Red/Indigo Today Current Time Horizontal Line */}
                  {today && isCurrentTimeInRange && (
                    <div
                      className="absolute inset-x-0 z-30 pointer-events-none flex items-center"
                      style={{ top: `${currentTimeTop}px` }}
                    >
                      <div className="w-2.5 h-2.5 rounded-full bg-rose-500 ring-2 ring-rose-400/50 -ml-1.5 shadow-sm" />
                      <div className="h-[2px] bg-rose-500/80 flex-1 shadow-sm" />
                    </div>
                  )}

                  {/* Rendered Event Blocks */}
                  {dayEvents.map((evt) => {
                    const start = new Date(evt.start_time);
                    const end = new Date(evt.end_time);
                    const startDecimal = start.getHours() + start.getMinutes() / 60;
                    const endDecimal = end.getHours() + end.getMinutes() / 60;

                    const clampedStart = Math.max(START_HOUR, Math.min(END_HOUR, startDecimal));
                    const clampedEnd = Math.max(clampedStart + 0.4, Math.min(END_HOUR, endDecimal));

                    const top = (clampedStart - START_HOUR) * HOUR_HEIGHT;
                    const height = Math.max(30, (clampedEnd - clampedStart) * HOUR_HEIGHT - 2);

                    const color = evt.color || '#6366f1';
                    const startTimeStr = start.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
                    const endTimeStr = end.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });

                    return (
                      <div
                        key={evt.id}
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectEvent(evt);
                        }}
                        className="absolute inset-x-1 rounded-xl p-2.5 transition-all cursor-pointer z-10 hover:z-20 hover:scale-[1.02] hover:shadow-xl group flex flex-col justify-between overflow-hidden"
                        style={{
                          top: `${top}px`,
                          height: `${height}px`,
                          backgroundColor: `${color}25`,
                          borderLeft: `4px solid ${color}`,
                          borderTop: `1px solid ${color}40`,
                          borderRight: `1px solid ${color}30`,
                          borderBottom: `1px solid ${color}30`,
                          backdropFilter: 'blur(8px)',
                        }}
                      >
                        <div>
                          <div className="flex items-center justify-between gap-1 mb-1">
                            <span className="text-[11px] font-bold text-white group-hover:text-indigo-200 transition-colors truncate">
                              {evt.title}
                            </span>
                            <span
                              className="text-[9px] uppercase px-1.5 py-0.2 rounded font-extrabold shrink-0"
                              style={{
                                color: color,
                                backgroundColor: `${color}30`,
                              }}
                            >
                              {evt.event_type}
                            </span>
                          </div>

                          <div className="flex items-center gap-1 text-[10px] text-slate-300 font-medium">
                            <Clock className="w-2.5 h-2.5 shrink-0" style={{ color }} />
                            <span>
                              {startTimeStr} – {endTimeStr}
                            </span>
                          </div>
                        </div>

                        {height > 55 && evt.location && (
                          <div className="flex items-center gap-1 text-[10px] text-slate-400 mt-1 truncate">
                            <Video className="w-2.5 h-2.5 shrink-0 text-cyan-400" />
                            <span className="truncate">{evt.location}</span>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
