'use client';

import React, { useState } from 'react';
import { X, ShieldCheck, CheckCircle2, ArrowRight, Loader2, UserPlus, ExternalLink } from 'lucide-react';
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

const GOOGLE_SSO_PROFILES = [
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
];

export default function GoogleAuthModal({
  isOpen,
  onClose,
}: GoogleAuthModalProps) {
  const { loginWithGoogle, loginWithDemoAccount } = useAuth();
  const [selectedEmail, setSelectedEmail] = useState<string | null>(null);
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [customEmail, setCustomEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  if (!isOpen) return null;

  const handleSelectGoogleProfile = async (profile: (typeof GOOGLE_SSO_PROFILES)[0]) => {
    setSelectedEmail(profile.email);
    setIsSubmitting(true);
    setErrorMessage('');

    try {
      await loginWithDemoAccount({
        email: profile.email,
        full_name: profile.full_name,
        role: profile.role,
        avatar_url: profile.avatar,
      });
      onClose();
    } catch (err: any) {
      setErrorMessage(err.message || 'Google SSO sign-in failed');
    } finally {
      setIsSubmitting(false);
      setSelectedEmail(null);
    }
  };

  const handleCustomGoogleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customEmail) return;

    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const generatedSub = `google_${customEmail.replace(/[^a-zA-Z0-9]/g, '_')}`;
      const name = customEmail.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());

      await loginWithGoogle({
        email: customEmail,
        full_name: name,
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${customEmail}`,
        sub: generatedSub,
        role: 'sales_rep',
      });
      onClose();
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to authenticate Google account');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLiveGoogleSSORedirect = () => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    window.location.href = `${backendUrl}/api/auth/google/login`;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      {/* Dialog Surface */}
      <div
        className="glass-panel w-full max-w-[420px] rounded-3xl border border-white/15 bg-[#0d1322]/95 p-6 shadow-2xl relative overflow-hidden text-slate-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Ambient Top Glow */}
        <div className="absolute -top-24 -left-20 w-52 h-52 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-20 w-52 h-52 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />

        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-1.5 rounded-full text-slate-400 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Google SSO Header */}
        <div className="flex flex-col items-center text-center pt-2 pb-5 border-b border-white/10">
          <div className="w-12 h-12 rounded-2xl bg-white shadow-lg flex items-center justify-center mb-3">
            <GoogleIcon className="w-7 h-7" />
          </div>
          <h3 className="text-base font-bold text-white tracking-tight">
            Sign in with Google SSO
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Choose an account to continue to <span className="text-white font-medium">NeuronForce</span>
          </p>
        </div>

        {errorMessage && (
          <div className="my-3 p-2.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs">
            {errorMessage}
          </div>
        )}

        {/* 1-Click Google Accounts Chooser */}
        <div className="py-4 space-y-2">
          {GOOGLE_SSO_PROFILES.map((profile) => {
            const isThisLoading = isSubmitting && selectedEmail === profile.email;
            return (
              <button
                key={profile.email}
                type="button"
                disabled={isSubmitting}
                onClick={() => handleSelectGoogleProfile(profile)}
                className="w-full flex items-center justify-between p-3 rounded-2xl border border-white/10 bg-white/[0.03] hover:bg-white/[0.08] hover:border-indigo-400/40 text-left transition-all group cursor-pointer active:scale-[0.99] disabled:opacity-50"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className="relative">
                    <img
                      src={profile.avatar}
                      alt={profile.full_name}
                      className="w-9 h-9 rounded-full bg-slate-800 border border-white/20 shrink-0 object-cover"
                    />
                    <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-white rounded-full flex items-center justify-center shadow-xs">
                      <GoogleIcon className="w-2.5 h-2.5" />
                    </div>
                  </div>
                  <div className="min-w-0">
                    <p className="text-xs font-semibold text-white group-hover:text-indigo-200 truncate">
                      {profile.full_name}
                    </p>
                    <p className="text-[11px] text-slate-400 truncate">{profile.email}</p>
                  </div>
                </div>

                <div className="flex items-center gap-1.5 shrink-0 pl-2">
                  {isThisLoading ? (
                    <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />
                  ) : (
                    <span className="text-[10px] font-semibold text-slate-400 px-2 py-0.5 rounded-md bg-white/5 border border-white/5 group-hover:bg-indigo-500/20 group-hover:text-indigo-200 group-hover:border-indigo-500/30 transition-colors">
                      {profile.roleLabel}
                    </span>
                  )}
                </div>
              </button>
            );
          })}

          {/* Use Another Google Account Toggle */}
          {!showCustomInput ? (
            <button
              type="button"
              disabled={isSubmitting}
              onClick={() => setShowCustomInput(true)}
              className="w-full flex items-center gap-3 p-3 rounded-2xl border border-dashed border-white/15 hover:border-indigo-400/50 hover:bg-white/[0.04] text-left transition-all text-slate-300 hover:text-white cursor-pointer"
            >
              <div className="w-9 h-9 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-slate-400">
                <UserPlus className="w-4 h-4" />
              </div>
              <span className="text-xs font-medium">Use another Google account</span>
            </button>
          ) : (
            <form onSubmit={handleCustomGoogleSubmit} className="pt-2 space-y-2">
              <div className="relative">
                <input
                  type="email"
                  required
                  autoFocus
                  placeholder="Enter your Google email (e.g. user@gmail.com)"
                  value={customEmail}
                  onChange={(e) => setCustomEmail(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white/5 border border-white/15 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                />
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={isSubmitting || !customEmail}
                  className="flex-1 py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
                >
                  {isSubmitting ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <>
                      <span>Continue with Google SSO</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => setShowCustomInput(false)}
                  className="px-3 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs cursor-pointer"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>

        {/* Live OAuth Redirect (Optional direct Google consent redirect) */}
        <div className="pt-2 pb-1">
          <button
            type="button"
            onClick={handleLiveGoogleSSORedirect}
            className="w-full py-2 px-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-[11px] text-slate-400 hover:text-white flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Launch Google OAuth Authorization Flow</span>
          </button>
        </div>

        {/* Google SSO Consent & Privacy Notice */}
        <div className="mt-4 pt-3 border-t border-white/10 text-[10px] text-slate-500 leading-relaxed text-center">
          To continue, Google will share your verified name, email address, language preference, and profile picture with NeuronForce.
        </div>
      </div>
    </div>
  );
}
