'use client';

import React, { useState } from 'react';
import { X, ShieldCheck, CheckCircle2, UserCheck, Sparkles, ArrowRight, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface GoogleAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  defaultMode?: 'signin' | 'signup';
}

export function GoogleIcon({ className = 'w-5 h-5' }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24">
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
      />
    </svg>
  );
}

export default function GoogleAuthModal({
  isOpen,
  onClose,
  defaultMode = 'signin',
}: GoogleAuthModalProps) {
  const { loginWithGoogle, loginWithDemoAccount } = useAuth();
  const [mode, setMode] = useState<'signin' | 'signup'>(defaultMode);
  const [customEmail, setCustomEmail] = useState('');
  const [customName, setCustomName] = useState('');
  const [selectedRole, setSelectedRole] = useState<'sales_rep' | 'revops_lead' | 'admin'>('sales_rep');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  if (!isOpen) return null;

  const handleCustomGoogleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customEmail) {
      setErrorMessage('Please enter an email address');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const generatedSub = `google_${customEmail.replace(/[^a-zA-Z0-9]/g, '_')}`;
      const name = customName.trim() || customEmail.split('@')[0].replace(/[._]/g, ' ');

      await loginWithGoogle({
        email: customEmail,
        full_name: name,
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${customEmail}`,
        sub: generatedSub,
        role: selectedRole,
      });

      onClose();
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to authenticate with Google');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDemoSelect = async (demo: { email: string; full_name: string; role: string; avatar: string }) => {
    setIsSubmitting(true);
    setErrorMessage('');

    try {
      await loginWithDemoAccount({
        email: demo.email,
        full_name: demo.full_name,
        role: demo.role,
        avatar_url: demo.avatar,
      });
      onClose();
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to authenticate');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-md animate-fadeIn">
      <div
        className="glass-panel w-full max-w-md rounded-2xl border border-white/15 bg-[#0e1424]/95 p-6 shadow-2xl relative overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Glow Effects */}
        <div className="absolute -top-20 -left-20 w-44 h-44 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-20 -right-20 w-44 h-44 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none" />

        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-5">
          <div className="w-11 h-11 rounded-xl bg-white flex items-center justify-center shadow-md">
            <GoogleIcon className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white tracking-tight">
              {mode === 'signin' ? 'Sign In with Google' : 'Create Account with Google'}
            </h3>
            <p className="text-xs text-slate-400">
              NeuronForce Autonomous Sales Cloud
            </p>
          </div>
        </div>

        {/* Mode Switch Tabs */}
        <div className="grid grid-cols-2 gap-1 p-1 bg-white/5 rounded-xl border border-white/10 mb-5">
          <button
            type="button"
            onClick={() => setMode('signin')}
            className={`py-1.5 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
              mode === 'signin'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => setMode('signup')}
            className={`py-1.5 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
              mode === 'signup'
                ? 'bg-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Sign Up
          </button>
        </div>

        {errorMessage && (
          <div className="mb-4 p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
            <span>{errorMessage}</span>
          </div>
        )}

        {/* One-Click Google Enterprise Logins */}
        <div className="space-y-2 mb-5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">
            {mode === 'signin' ? 'Quick Sign-In with Demo Account:' : 'Pre-configured Profiles:'}
          </span>

          <div className="grid grid-cols-1 gap-2">
            {[
              {
                email: 'alex.rivera@neuronforce.ai',
                full_name: 'Alex Rivera',
                role: 'revops_lead',
                roleLabel: 'RevOps Lead',
                avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex',
              },
              {
                email: 'sarah.jenkins@neuronforce.ai',
                full_name: 'Sarah Jenkins',
                role: 'admin',
                roleLabel: 'Platform Admin',
                avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=SarahJ',
              },
              {
                email: 'jordan.lee@neuronforce.ai',
                full_name: 'Jordan Lee',
                role: 'sales_rep',
                roleLabel: 'Enterprise Sales Rep',
                avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jordan',
              },
            ].map((demo) => (
              <button
                key={demo.email}
                type="button"
                disabled={isSubmitting}
                onClick={() => handleDemoSelect(demo)}
                className="w-full flex items-center justify-between p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-indigo-600/20 hover:border-indigo-500/40 text-left transition-all group cursor-pointer"
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <img
                    src={demo.avatar}
                    alt={demo.full_name}
                    className="w-7 h-7 rounded-full bg-slate-800 border border-white/10 shrink-0"
                  />
                  <div className="min-w-0">
                    <p className="text-xs font-semibold text-white group-hover:text-indigo-300 truncate">
                      {demo.full_name}
                    </p>
                    <p className="text-[10px] text-slate-400 truncate">{demo.email}</p>
                  </div>
                </div>
                <span className="text-[10px] font-medium text-slate-400 px-2 py-0.5 rounded-md bg-white/5 shrink-0 group-hover:bg-indigo-500/20 group-hover:text-indigo-200">
                  {demo.roleLabel}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div className="relative flex items-center justify-center my-4">
          <div className="border-t border-white/10 w-full" />
          <span className="bg-[#0e1424] px-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            Or Use Custom Google Account
          </span>
        </div>

        {/* Custom Email Form */}
        <form onSubmit={handleCustomGoogleSubmit} className="space-y-3">
          <div>
            <label className="block text-[11px] font-medium text-slate-300 mb-1">
              Google Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                required
                placeholder="name@company.com or name@gmail.com"
                value={customEmail}
                onChange={(e) => setCustomEmail(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          </div>

          {mode === 'signup' && (
            <>
              <div>
                <label className="block text-[11px] font-medium text-slate-300 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  placeholder="e.g. Elena Rostova"
                  value={customName}
                  onChange={(e) => setCustomName(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-[11px] font-medium text-slate-300 mb-1">
                  Assigned Workspace Role
                </label>
                <select
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value as any)}
                  className="w-full px-3 py-2 rounded-xl bg-[#131b2e] border border-white/10 text-white text-xs focus:outline-none focus:border-indigo-500"
                >
                  <option value="sales_rep">Enterprise Sales Rep</option>
                  <option value="revops_lead">RevOps Lead</option>
                  <option value="admin">Platform Administrator</option>
                </select>
              </div>
            </>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white text-xs font-bold shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 cursor-pointer transition-all disabled:opacity-50"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Authenticating with Google...</span>
              </>
            ) : (
              <>
                <GoogleIcon className="w-4 h-4" />
                <span>
                  {mode === 'signin' ? 'Sign In with Google' : 'Create Google Account'}
                </span>
                <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </>
            )}
          </button>
        </form>

        {/* Security Footer */}
        <div className="mt-5 pt-3 border-t border-white/10 flex items-center justify-between text-[10px] text-slate-500">
          <div className="flex items-center gap-1.5 text-slate-400">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Google OIDC 256-Bit JWT</span>
          </div>
          <span className="text-slate-500">NeuronForce Security</span>
        </div>
      </div>
    </div>
  );
}
