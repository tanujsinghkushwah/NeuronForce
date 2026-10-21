'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Users,
  Kanban,
  Sparkles,
  BarChart3,
  Calendar,
  Settings,
  Zap,
  CheckCircle2,
  ChevronRight,
  Megaphone,
  LifeBuoy
} from 'lucide-react';
import NeuronForceLogo from './NeuronForceLogo';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
  aiHighlight?: boolean;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Contacts', href: '/contacts', icon: Users },
  { name: 'Deals Pipeline', href: '/deals', icon: Kanban },
  { name: 'AI Agents', href: '/ai-agents', icon: Sparkles, badge: 'Active', aiHighlight: true },
  { name: 'Campaigns', href: '/campaigns', icon: Megaphone, badge: 'Marketing' },
  { name: 'Service Cases', href: '/tickets', icon: LifeBuoy, badge: 'SLA' },
  { name: 'Analytics & BI', href: '/analytics', icon: BarChart3 },
  { name: 'Calendar', href: '/calendar', icon: Calendar },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

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
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                  : 'text-slate-300 hover:text-white hover:bg-white/5'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon
                  className={`w-4 h-4 transition-colors ${
                    isActive
                      ? 'text-white'
                      : item.aiHighlight
                      ? 'text-cyan-400 group-hover:text-cyan-300'
                      : 'text-slate-400 group-hover:text-slate-200'
                  }`}
                />
                <span>{item.name}</span>
              </div>

              {item.badge && (
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-semibold uppercase tracking-wide ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}
      </div>

      {/* AI Engine Status Card */}
      <div className="p-3 border-t border-white/10">
        <div className="p-3 rounded-xl bg-gradient-to-br from-indigo-950/60 to-slate-900/60 border border-indigo-500/20 backdrop-blur-md">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-semibold text-white">AI Agent Mesh</span>
            </div>
            <span className="text-[10px] text-emerald-400 font-medium">99.9% Uptime</span>
          </div>

          <p className="text-[11px] text-slate-300 leading-relaxed mb-2.5">
            Transparent reasoning &amp; cost tracking on every automated sales decision.
          </p>

          <Link
            href="/ai-agents"
            className="flex items-center justify-between text-[11px] text-indigo-300 hover:text-indigo-200 font-medium group"
          >
            <span>Open Agent Monitor</span>
            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </div>
      </div>
    </aside>
  );
}
