'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ShieldCheck, ArrowRight, Loader2, Sparkles } from 'lucide-react';
import NeuronForceLogo from '../../components/NeuronForceLogo';
import { GoogleIcon } from '../../components/GoogleAuthModal';
import { useAuth } from '../../context/AuthContext';

export default function LoginPage() {
  const router = useRouter();
  const { loginWithGoogle, loginWithDemoAccount, isAuthenticated } = useAuth();
  const [mode, setMode] = useState<'signin' | 'signup'>('signin');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState<'sales_rep' | 'revops_lead' | 'admin'>('sales_rep');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleCustomGoogleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setErrorMessage('Please enter your Google email.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const generatedSub = `google_${email.replace(/[^a-zA-Z0-9]/g, '_')}`;
      const name = fullName.trim() || email.split('@')[0].replace(/[._]/g, ' ');

      await loginWithGoogle({
        email,
        full_name: name,
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
        sub: generatedSub,
        role: role,
      });

      router.push('/');
    } catch (err: any) {
      setErrorMessage(err.message || 'Google authentication failed.');
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
      router.push('/');
    } catch (err: any) {
      setErrorMessage(err.message || 'Authentication failed.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-6 relative overflow-hidden bg-[#070b14]">
      {/* Background Gradients */}
      <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] bg-indigo-600/15 blur-[160px] rounded-full pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/3 w-[500px] h-[500px] bg-cyan-500/10 blur-[160px] rounded-full pointer-events-none" />

      <div className="w-full max-w-md relative z-10 space-y-6">
        {/* Brand Logo Header */}
        <div className="flex flex-col items-center text-center space-y-2">
          <NeuronForceLogo size="lg" />
          <p className="text-xs text-slate-400">
            Next-Gen Autonomous AI CRM & Enterprise Sales Cloud
          </p>
        </div>

        {/* Main Auth Card */}
        <div className="glass-panel rounded-2xl border border-white/15 bg-[#0e1424]/90 p-7 shadow-2xl backdrop-blur-xl">
          {/* Mode Switcher */}
          <div className="grid grid-cols-2 gap-1 p-1 bg-white/5 rounded-xl border border-white/10 mb-6">
            <button
              type="button"
              onClick={() => setMode('signin')}
              className={`py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
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
              className={`py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer ${
                mode === 'signup'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Sign Up
            </button>
          </div>

          {errorMessage && (
            <div className="mb-4 p-3 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs">
              {errorMessage}
            </div>
          )}

          {/* Pre-configured Demo Google Accounts */}
          <div className="space-y-2 mb-6">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1.5">
              One-Click Enterprise Google Sign-In:
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
                      className="w-8 h-8 rounded-full bg-slate-800 border border-white/10 shrink-0"
                    />
                    <div className="min-w-0">
                      <p className="text-xs font-semibold text-white group-hover:text-indigo-300 truncate">
                        {demo.full_name}
                      </p>
                      <p className="text-[11px] text-slate-400 truncate">{demo.email}</p>
                    </div>
                  </div>
                  <span className="text-[10px] font-semibold text-slate-400 px-2.5 py-1 rounded-md bg-white/5 shrink-0 group-hover:bg-indigo-500/25 group-hover:text-indigo-200">
                    {demo.roleLabel}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Form Divider */}
          <div className="relative flex items-center justify-center my-5">
            <div className="border-t border-white/10 w-full" />
            <span className="bg-[#0e1424] px-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
              Or Connect Custom Google Account
            </span>
          </div>

          {/* Custom Google Email Form */}
          <form onSubmit={handleCustomGoogleAuth} className="space-y-3.5">
            <div>
              <label className="block text-[11px] font-medium text-slate-300 mb-1">
                Google Email
              </label>
              <input
                type="email"
                required
                placeholder="name@company.com or name@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              />
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
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-[11px] font-medium text-slate-300 mb-1">
                    Workspace Role
                  </label>
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value as any)}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-[#131b2e] border border-white/10 text-white text-xs focus:outline-none focus:border-indigo-500"
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
              className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white text-xs font-bold shadow-xl shadow-indigo-500/25 flex items-center justify-center gap-2 cursor-pointer transition-all disabled:opacity-50"
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
                    {mode === 'signin' ? 'Sign In with Google' : 'Create Account with Google'}
                  </span>
                  <ArrowRight className="w-4 h-4 ml-1" />
                </>
              )}
            </button>
          </form>

          {/* Security Banner */}
          <div className="mt-6 pt-4 border-t border-white/10 flex items-center justify-between text-[11px] text-slate-500">
            <div className="flex items-center gap-1.5 text-slate-400">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Google OIDC • 256-Bit Session Isolation</span>
            </div>
            <span>v1.0.0</span>
          </div>
        </div>
      </div>
    </div>
  );
}
