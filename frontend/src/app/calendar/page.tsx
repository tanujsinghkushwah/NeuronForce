"use client";

import React, { useEffect, useState, useMemo } from "react";
import Header from "../../components/Header";
import { api } from "../../lib/api";
import { CalendarEvent } from "../../types/crm";
import TimelineView from "../../components/calendar/TimelineView";
import CardsView from "../../components/calendar/CardsView";
import EventDetailModal from "../../components/calendar/EventDetailModal";
import ScheduleModal from "../../components/calendar/ScheduleModal";
import {
  Calendar as CalendarIcon,
  LayoutGrid,
  Rows3,
  Plus,
  ChevronLeft,
  ChevronRight,
  Sparkles,
} from "lucide-react";

export default function CalendarPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);

  // View mode: 'timeline' (Google Calendar style) or 'cards' (card grid)
  const [activeView, setActiveView] = useState<"timeline" | "cards">(
    "timeline",
  );

  // Timeline sub-mode: 'week' (7-day timeline) or 'day' (1-day timeline)
  const [timelineSubMode, setTimelineSubMode] = useState<"week" | "day">(
    "week",
  );

  // Active anchor date for calendar navigation (stable initial value for prerender, updated on mount)
  const [currentDate, setCurrentDate] = useState<Date>(
    () => new Date("2026-10-22T00:00:00"),
  );

  useEffect(() => {
    setCurrentDate(new Date());
  }, []);

  // Modals state
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(
    null,
  );
  const [showScheduleModal, setShowScheduleModal] = useState(false);

  const [form, setForm] = useState({
    title: "",
    start_time: "",
    end_time: "",
    location: "Zoom Meeting",
    event_type: "meeting",
    attendees: "alex@neuronforce.ai, customer@acme.com",
    color: "#6366f1",
  });

  const openNewEventModal = () => {
    const now = new Date();
    // Default to next hour
    const start = new Date(now);
    start.setMinutes(0, 0, 0);
    start.setHours(start.getHours() + 1);

    const end = new Date(start);
    end.setHours(end.getHours() + 1);

    // Format local datetime string: YYYY-MM-DDTHH:mm
    const toLocalISO = (d: Date) => {
      const pad = (n: number) => String(n).padStart(2, "0");
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
    };

    setForm((f) => ({
      ...f,
      start_time: toLocalISO(start),
      end_time: toLocalISO(end),
    }));
    setShowScheduleModal(true);
  };

  const handleSlotClick = (date: Date, hour: number) => {
    const start = new Date(date);
    start.setHours(hour, 0, 0, 0);

    const end = new Date(date);
    end.setHours(hour + 1, 0, 0, 0);

    const pad = (n: number) => String(n).padStart(2, "0");
    const toLocalISO = (d: Date) =>
      `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;

    setForm((f) => ({
      ...f,
      start_time: toLocalISO(start),
      end_time: toLocalISO(end),
      title: "",
    }));
    setShowScheduleModal(true);
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
          title: "Enterprise Architecture QBR with HyperScale",
          description:
            "Review migration from legacy Salesforce instance to NeuronForce with VP Eng.",
          start_time: "2026-10-22T14:00:00Z",
          end_time: "2026-10-22T15:00:00Z",
          location: "Zoom Virtual Room",
          event_type: "meeting",
          attendees: ["elena@hyperscale.ai", "alex@neuronforce.ai"],
          color: "#6366f1",
          is_all_day: false,
          reminder_minutes: 15,
          created_at: "2026-10-20T10:00:00Z",
          updated_at: "2026-10-20T10:00:00Z",
        },
        {
          id: 2,
          title: "POC Technical Deep Dive: Autonomous Agents",
          description:
            "Hands-on review of lead scoring and email generative agents with RevOps team.",
          start_time: "2026-10-23T16:30:00Z",
          end_time: "2026-10-23T17:30:00Z",
          location: "Google Meet",
          event_type: "demo",
          attendees: ["marcus@innovatetech.io", "jordan@neuronforce.ai"],
          color: "#f59e0b",
          is_all_day: false,
          reminder_minutes: 15,
          created_at: "2026-10-20T11:00:00Z",
          updated_at: "2026-10-20T11:00:00Z",
        },
        {
          id: 3,
          title: "Contract Signing & Security Governance Review",
          description:
            "Final security governance checklist approval with legal.",
          start_time: "2026-10-24T10:00:00Z",
          end_time: "2026-10-24T10:45:00Z",
          location: "Teams Meeting",
          event_type: "follow_up",
          attendees: ["sarah@cloudops.com", "legal@neuronforce.ai"],
          color: "#10b981",
          is_all_day: false,
          reminder_minutes: 15,
          created_at: "2026-10-20T12:00:00Z",
          updated_at: "2026-10-20T12:00:00Z",
        },
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
        attendees: form.attendees
          .split(",")
          .map((a) => a.trim())
          .filter(Boolean),
      });
      setShowScheduleModal(false);
      loadEvents();
    } catch (err) {
      alert("Could not schedule event: " + String(err));
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.deleteCalendarEvent(id);
      setEvents((prev) => prev.filter((e) => e.id !== id));
    } catch {
      setEvents((prev) => prev.filter((e) => e.id !== id));
    }
  };

  // Navigation handlers
  const handlePrev = () => {
    setCurrentDate((prev) => {
      const d = new Date(prev);
      if (timelineSubMode === "week") {
        d.setDate(d.getDate() - 7);
      } else {
        d.setDate(d.getDate() - 1);
      }
      return d;
    });
  };

  const handleNext = () => {
    setCurrentDate((prev) => {
      const d = new Date(prev);
      if (timelineSubMode === "week") {
        d.setDate(d.getDate() + 7);
      } else {
        d.setDate(d.getDate() + 1);
      }
      return d;
    });
  };

  // Format header range string with deterministic naming
  const formattedDateRange = useMemo(() => {
    const MONTH_NAMES = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    const WEEKDAY_NAMES = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ];

    if (timelineSubMode === "day") {
      const weekday = WEEKDAY_NAMES[currentDate.getDay()];
      const month = MONTH_NAMES[currentDate.getMonth()];
      return `${weekday}, ${month} ${currentDate.getDate()}, ${currentDate.getFullYear()}`;
    }

    // Week range: find Monday and Sunday
    const d = new Date(currentDate);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1);
    const monday = new Date(d.setDate(diff));
    const sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);

    const mMonth = MONTH_NAMES[monday.getMonth()];
    const sMonth = MONTH_NAMES[sunday.getMonth()];
    const year = sunday.getFullYear();

    if (mMonth === sMonth) {
      return `${mMonth} ${monday.getDate()} – ${sunday.getDate()}, ${year}`;
    }
    return `${mMonth} ${monday.getDate()} – ${sMonth} ${sunday.getDate()}, ${year}`;
  }, [currentDate, timelineSubMode]);

  return (
    <div className="flex-1 flex flex-col pb-12">
      <Header
        title="Executive Calendar &amp; Engagements"
        subtitle="Customer meeting schedules synchronized across deal timelines"
        onActionClick={openNewEventModal}
      />

      <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto w-full">
        {/* ── Top Controls & Switcher Toolbar ─────────────────────────── */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-4 rounded-2xl border border-white/10">
          {/* Left: Date navigation controls */}
          <div className="flex items-center gap-3">
            <div className="flex items-center bg-white/5 rounded-xl border border-white/10 p-0.5">
              <button
                onClick={handlePrev}
                title="Previous"
                className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={handleNext}
                title="Next"
                className="p-1.5 text-slate-300 hover:text-white rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            <div className="flex items-center gap-2 pl-2">
              <CalendarIcon className="w-4 h-4 text-indigo-400" />
              <span className="text-sm font-bold text-white tracking-tight">
                {formattedDateRange}
              </span>
            </div>
          </div>

          {/* Right: View mode toggles & Action */}
          <div className="flex items-center gap-2.5 flex-wrap">
            {/* Timeline Sub-mode: Week vs Day (only visible when in Timeline View) */}
            {activeView === "timeline" && (
              <div className="flex items-center bg-black/25 p-1 rounded-xl border border-white/10">
                <button
                  onClick={() => setTimelineSubMode("week")}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    timelineSubMode === "week"
                      ? "bg-indigo-600 text-white shadow-sm"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Week
                </button>
                <button
                  onClick={() => setTimelineSubMode("day")}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    timelineSubMode === "day"
                      ? "bg-indigo-600 text-white shadow-sm"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  Day
                </button>
              </div>
            )}

            {/* Primary View Switcher: Timeline vs Cards */}
            <div className="flex items-center bg-black/25 p-1 rounded-xl border border-white/10">
              <button
                onClick={() => setActiveView("timeline")}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  activeView === "timeline"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-white"
                }`}
                title="Google Calendar Timeline View"
              >
                <Rows3 className="w-3.5 h-3.5" />
                <span>Timeline</span>
              </button>

              <button
                onClick={() => setActiveView("cards")}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  activeView === "cards"
                    ? "bg-indigo-600 text-white shadow-sm"
                    : "text-slate-400 hover:text-white"
                }`}
                title="Cards Grid View"
              >
                <LayoutGrid className="w-3.5 h-3.5" />
                <span>Cards</span>
              </button>
            </div>

            {/* Schedule Meeting Button */}
            <button
              onClick={openNewEventModal}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/30 transition-all cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Schedule</span>
            </button>
          </div>
        </div>

        {/* ── Main View Area ─────────────────────────────────────────── */}
        {activeView === "timeline" ? (
          <TimelineView
            events={events}
            currentDate={currentDate}
            viewMode={timelineSubMode}
            onSelectEvent={(evt) => setSelectedEvent(evt)}
            onSlotClick={handleSlotClick}
          />
        ) : (
          <CardsView
            events={events}
            onSelectEvent={(evt) => setSelectedEvent(evt)}
            onDeleteEvent={handleDelete}
          />
        )}
      </div>

      {/* ── Event Details Modal ──────────────────────────────────────── */}
      <EventDetailModal
        event={selectedEvent}
        onClose={() => setSelectedEvent(null)}
        onDelete={handleDelete}
      />

      {/* ── Schedule Meeting Modal ───────────────────────────────────── */}
      <ScheduleModal
        show={showScheduleModal}
        onClose={() => setShowScheduleModal(false)}
        onSubmit={handleCreate}
        form={form}
        setForm={setForm}
      />
    </div>
  );
}
