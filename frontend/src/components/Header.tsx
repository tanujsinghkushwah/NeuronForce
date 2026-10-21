'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Search, Bell, Plus, LogOut, ChevronDown, User as UserIcon, Shield, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import GoogleAuthModal, { GoogleIcon } from './GoogleAuthModal';

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
  const { user, isAuthenticated, logout, signInWithGoogleSSO, isFirebaseAvailable } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const formatRole = (role?: string) => {
    switch (role) {
      case 'revops_lead':
        return 'RevOps Lead';
      case 'admin':
        return 'Platform Admin';
      case 'sales_rep':
        return 'Sales Rep';
      default:
        return 'Workspace Member';
    }
  };

  return (
    <>
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

          {/* Dynamic Authenticated User or Google Sign-In */}
          {isAuthenticated && user ? (
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="flex items-center gap-2.5 pl-2 py-1 border-l border-white/10 hover:opacity-90 transition-opacity cursor-pointer group"
              >
                {user.avatar_url ? (
                  <img
                    src={user.avatar_url}
                    alt={user.full_name}
                    className="w-8 h-8 rounded-full bg-slate-800 ring-1 ring-white/20 shadow-sm object-cover"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-xs text-white ring-1 ring-white/20 shadow-sm">
                    {getInitials(user.full_name || 'User')}
                  </div>
                )}
                <div className="hidden sm:flex flex-col text-left">
                  <div className="flex items-center gap-1">
                    <span className="text-xs font-semibold text-white leading-tight group-hover:text-indigo-300 transition-colors">
                      {user.full_name}
                    </span>
                    <ChevronDown className="w-3 h-3 text-slate-400" />
                  </div>
                  <span className="text-[10px] text-slate-400 leading-tight">
                    {formatRole(user.role)}
                  </span>
                </div>
              </button>

              {/* User Account Menu Dropdown */}
              {showDropdown && (
                <div className="absolute right-0 mt-2 w-64 rounded-2xl bg-[#0e1424]/95 border border-white/15 p-2 shadow-2xl backdrop-blur-xl z-50 animate-fadeIn">
                  <div className="p-3 border-b border-white/10">
                    <p className="text-xs font-bold text-white truncate">{user.full_name}</p>
                    <p className="text-[11px] text-slate-400 truncate">{user.email}</p>
                    <div className="mt-2 flex items-center gap-1.5">
                      <span className="text-[9px] font-semibold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                        {formatRole(user.role)}
                      </span>
                      <span className="text-[9px] font-medium px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                        <GoogleIcon className="w-2.5 h-2.5" />
                        Verified
                      </span>
                    </div>
                  </div>

                  <div className="p-1 space-y-0.5">
                    <button
                      onClick={() => {
                        setShowDropdown(false);
                        setShowAuthModal(true);
                      }}
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-slate-300 hover:text-white hover:bg-white/5 rounded-xl transition-colors cursor-pointer text-left"
                    >
                      <GoogleIcon className="w-3.5 h-3.5" />
                      <span>Switch Google Account</span>
                    </button>

                    <button
                      onClick={() => {
                        setShowDropdown(false);
                        logout();
                      }}
                      className="w-full flex items-center gap-2 px-3 py-2 text-xs text-rose-300 hover:text-rose-200 hover:bg-rose-500/10 rounded-xl transition-colors cursor-pointer text-left"
                    >
                      <LogOut className="w-3.5 h-3.5" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="pl-2 border-l border-white/10">
              <button
                onClick={async () => {
                  if (isFirebaseAvailable) {
                    try {
                      await signInWithGoogleSSO();
                      return;
                    } catch (e) {
                      console.log('Firebase SSO popup cancelled or fallback needed', e);
                    }
                  }
                  setShowAuthModal(true);
                }}
                className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-white hover:bg-slate-100 text-slate-900 text-xs font-bold shadow-md hover:shadow-lg transition-all active:scale-95 cursor-pointer"
              >
                <GoogleIcon className="w-4 h-4" />
                <span>Sign in with Google</span>
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Google Sign-In & Sign-Up Modal */}
      <GoogleAuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
      />
    </>
  );
}
