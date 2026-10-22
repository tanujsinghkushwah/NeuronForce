"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Users,
  Kanban,
  Sparkles,
  BarChart3,
  Calendar,
  Settings,
  Megaphone,
  LifeBuoy,
  Sun,
  Moon,
} from "lucide-react";
import NeuronForceLogo from "./NeuronForceLogo";
import { useTheme } from "../context/ThemeContext";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
  aiHighlight?: boolean;
}

const navItems: NavItem[] = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Contacts", href: "/contacts", icon: Users },
  { name: "Deals Pipeline", href: "/deals", icon: Kanban },
  {
    name: "AI Agents",
    href: "/ai-agents",
    icon: Sparkles,
    badge: "Active",
    aiHighlight: true,
  },
  {
    name: "Campaigns",
    href: "/campaigns",
    icon: Megaphone,
    badge: "Marketing",
  },
  { name: "Service Cases", href: "/tickets", icon: LifeBuoy, badge: "SLA" },
  { name: "Analytics & BI", href: "/analytics", icon: BarChart3 },
  { name: "Calendar", href: "/calendar", icon: Calendar },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();

  return (
    <aside className="w-64 border-r border-white/10 bg-[#0b101b]/95 backdrop-blur-xl flex flex-col h-screen sticky top-0 z-40 select-none">
      {/* Brand Header */}
      <div className="h-16 px-4 flex items-center justify-between border-b border-white/10">
        <Link href="/" className="flex items-center">
          <NeuronForceLogo size="md" />
        </Link>
      </div>

      {/* Navigation */}
      <div className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
          Core Platform
        </div>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all group ${
                isActive
                  ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/30"
                  : "text-slate-300 hover:text-white hover:bg-white/5"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon
                  className={`w-4 h-4 transition-colors ${
                    isActive
                      ? "text-white"
                      : item.aiHighlight
                        ? "text-cyan-400 group-hover:text-cyan-300"
                        : "text-slate-400 group-hover:text-slate-200"
                  }`}
                />
                <span>{item.name}</span>
              </div>

              {item.badge && (
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-semibold uppercase tracking-wide ${
                    isActive
                      ? "bg-white/20 text-white"
                      : "bg-cyan-500/15 text-cyan-400 border border-cyan-500/30"
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </div>

      {/* Dark / Light Mode Toggle in Bottom Left */}
      <div className="p-3 border-t border-white/10 mt-auto">
        <div className="flex items-center justify-between p-1.5 rounded-xl bg-white/5 border border-white/10 backdrop-blur-md">
          <div className="flex items-center gap-2 pl-1.5 text-xs font-medium text-slate-300">
            {theme === "dark" ? (
              <Moon className="w-3.5 h-3.5 text-indigo-400" />
            ) : (
              <Sun className="w-3.5 h-3.5 text-amber-500" />
            )}
            <span className="capitalize text-[11px]">{theme} Mode</span>
          </div>

          <div className="flex items-center bg-black/20 p-0.5 rounded-lg border border-white/5">
            <button
              id="theme-light-btn"
              onClick={() => setTheme("light")}
              title="Switch to Light Mode"
              className={`flex items-center gap-1 px-2 py-1 rounded-md text-[10px] font-semibold transition-all cursor-pointer ${
                theme === "light"
                  ? "bg-amber-400 text-slate-900 shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Sun className="w-3 h-3" />
              <span>Light</span>
            </button>
            <button
              id="theme-dark-btn"
              onClick={() => setTheme("dark")}
              title="Switch to Dark Mode"
              className={`flex items-center gap-1 px-2 py-1 rounded-md text-[10px] font-semibold transition-all cursor-pointer ${
                theme === "dark"
                  ? "bg-indigo-600 text-white shadow-sm shadow-indigo-600/40"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Moon className="w-3 h-3" />
              <span>Dark</span>
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}
