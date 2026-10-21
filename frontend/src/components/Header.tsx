'use client';

import React, { useState } from 'react';
import { Search, Bell, Sparkles, Plus, CheckCircle, Zap } from 'lucide-react';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  onActionClick?: (action: 'deal' | 'contact' | 'agent') => void;
}

export default function Header({
  title = 'Enterprise Overview',
  subtitle = 'Real-time sales telemetry, AI agents, and pipeline velocity',
  onActionClick
}: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <header className="h-16 border-b border-white/10 bg-[#0b101b]/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Title & Context */}
      <div>
        <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
          {title}
        </h1>
        <p className="text-xs text-slate-300 hidden md:block">
          {subtitle}
        </p>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <div className="relative hidden lg:block w-64">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search deals, contacts, agents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-9 pl-9 pr-4 rounded-xl bg-slate-900/80 border border-white/10 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-indigo-500 transition-colors"
          />
        </div>

        {/* Action Button */}
        {onActionClick && (
          <div className="flex items-center gap-2">
            <button
              onClick={() => onActionClick('deal')}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-lg shadow-indigo-600/25 transition-all active:scale-95 cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>New Deal</span>
            </button>
          </div>
        )}

        {/* Notifications */}
        <button
          aria-label="View notifications"
          className="w-9 h-9 rounded-xl bg-slate-900/80 border border-white/10 flex items-center justify-center text-slate-300 hover:text-white hover:bg-white/5 transition-colors relative cursor-pointer"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-cyan-400 ring-2 ring-slate-900"></span>
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-2.5 pl-2 border-l border-white/10">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white ring-1 ring-white/20 shadow-sm">
            AR
          </div>
          <div className="hidden sm:flex flex-col text-left">
            <span className="text-xs font-semibold text-white leading-tight">Alex Rivera</span>
            <span className="text-[10px] text-slate-400 leading-tight">RevOps Lead</span>
          </div>
        </div>
      </div>
    </header>
  );
}
