"use client";

import React, { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import {
  Lock,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  Loader2,
  Users,
  KeyRound,
  ExternalLink,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import GoogleAuthModal, { GoogleIcon } from "./GoogleAuthModal";

const DEMO_PERSONAS = [
  {
    email: "alex.rivera@neuronforce.ai",
    name: "Alex Rivera",
    role: "revops_lead",
    roleLabel: "RevOps Lead",
    tag: "Full Access & AI Mesh",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
  },
  {
    email: "sarah.jenkins@neuronforce.ai",
    name: "Sarah Jenkins",
    role: "admin",
    roleLabel: "Platform Admin",
    tag: "Security & Governance",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=SarahJ",
  },
  {
    email: "jordan.lee@neuronforce.ai",
    name: "Jordan Lee",
    role: "sales_rep",
    roleLabel: "Enterprise Sales Rep",
    tag: "Deals & Outreach",
    avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Jordan",
  },
];

interface AuthScreenGuardProps {
  children: React.ReactNode;
}

export default function AuthScreenGuard({ children }: AuthScreenGuardProps) {
  const pathname = usePathname();
  const {
    user,
    isAuthenticated,
    isLoading,
    loginWithDemoAccount,
    signInWithGoogleSSO,
    isFirebaseAvailable,
  } = useAuth();

  const [selectedEmail, setSelectedEmail] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showGoogleModal, setShowGoogleModal] = useState(false);
  const [justUnlocked, setJustUnlocked] = useState(false);
  const [unlockedUser, setUnlockedUser] = useState<string>("");
  const [isAnimatingUnlock, setIsAnimatingUnlock] = useState(false);

  const prevAuthRef = React.useRef(isAuthenticated);

  useEffect(() => {
    // If transitioning from unauthenticated -> authenticated, animate de-blur for 750ms
    if (!prevAuthRef.current && isAuthenticated) {
      setIsAnimatingUnlock(true);
      const timer = setTimeout(() => {
        setIsAnimatingUnlock(false);
      }, 750);
      return () => clearTimeout(timer);
    }
    prevAuthRef.current = isAuthenticated;
  }, [isAuthenticated]);

  // Handle successful sign-in toast
  useEffect(() => {
    if (isAuthenticated && user?.full_name && !justUnlocked) {
      setUnlockedUser(user.full_name);
    }
  }, [isAuthenticated, user]);

  // Don't apply blur guard on the dedicated /login page
  if (pathname === "/login") {
    return <>{children}</>;
  }

  const handlePersonaSelect = async (persona: (typeof DEMO_PERSONAS)[0]) => {
    setSelectedEmail(persona.email);
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const loggedUser = await loginWithDemoAccount({
        email: persona.email,
        full_name: persona.name,
        role: persona.role,
        avatar_url: persona.avatar,
      });

      setUnlockedUser(loggedUser.full_name);
      setJustUnlocked(true);
      setTimeout(() => setJustUnlocked(false), 3500);
    } catch (err: any) {
      setErrorMessage(
        err.message || "Authentication failed. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
      setSelectedEmail(null);
    }
  };

  const handleGoogleSSOClick = async () => {
    setIsSubmitting(true);
    setErrorMessage(null);

    if (isFirebaseAvailable) {
      try {
        const loggedUser = await signInWithGoogleSSO();
        setUnlockedUser(loggedUser.full_name);
        setJustUnlocked(true);
        setTimeout(() => setJustUnlocked(false), 3500);
        return;
      } catch (err: any) {
        console.warn(
          "Google SSO direct popup failed, falling back to modal:",
          err,
        );
      } finally {
        setIsSubmitting(false);
      }
    }

    setIsSubmitting(false);
    setShowGoogleModal(true);
  };

  const isLocked = !isAuthenticated;

  return (
    <div className="relative min-h-screen flex-1 flex flex-col">
      {/*
        Main Screen Page Content
        Applies smooth blur transition:
        - When unauthenticated: blur-md / blur-[14px], slightly dimmed, pointer-events-none
        - When transitioning to authenticated: blur-0 smoothly over 700ms
        - When authenticated: completely clean (no filter, no transform, no scale, no will-change)
          so fixed-position modals (like Create Deal) anchor to the true browser viewport!
      */}
      <div
        className={`flex-1 flex flex-col min-w-0 ${
          isLocked
            ? "filter blur-[12px] md:blur-[14px] brightness-90 md:brightness-75 pointer-events-none select-none transition-all duration-700 ease-out"
            : isAnimatingUnlock
              ? "filter blur-0 brightness-100 pointer-events-auto select-auto transition-all duration-700 ease-out"
              : ""
        }`}
        aria-hidden={isLocked}
      >
        {children}
      </div>

      {/* Floating Center Authentication Card when Locked */}
      {isLocked && (
        <div className="fixed inset-0 lg:left-64 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-in fade-in duration-500">
          {/* Subtle Dimmed Backdrop */}
          <div className="fixed inset-0 lg:left-64 bg-slate-950/40 backdrop-blur-xs transition-opacity duration-500" />

          {/* Frosted Glass Lock Card */}
          <div className="auth-guard-card relative w-full max-w-lg rounded-3xl border border-white/15 bg-[#0e1424]/90 p-6 sm:p-8 shadow-2xl shadow-black/60 backdrop-blur-2xl transition-all duration-500 z-10 space-y-6">
            {/* Lock Badge Header */}
            <div className="text-center space-y-3">
              <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-500/20 via-indigo-600/30 to-cyan-500/20 border border-indigo-500/40 shadow-lg shadow-indigo-500/20 text-indigo-400">
                <Lock className="w-6 h-6 animate-pulse" />
              </div>

              <div>
                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 mb-2">
                  <ShieldCheck className="w-3 h-3 text-cyan-400" />
                  <span>Enterprise Workspace Locked</span>
                </div>
                <h2 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
                  Sign in to Access NeuronForce
                </h2>
                <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-sm mx-auto leading-relaxed">
                  Real-time ARR telemetry, proprietary deal pipeline, and
                  autonomous AI agents require an authenticated session.
                </p>
              </div>
            </div>

            {/* Error Message if any */}
            {errorMessage && (
              <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs text-center font-medium">
                {errorMessage}
              </div>
            )}

            {/* Primary Action: Sign in with Google */}
            <div className="space-y-3">
              <button
                type="button"
                onClick={handleGoogleSSOClick}
                disabled={isSubmitting}
                className="w-full flex items-center justify-center gap-3 px-5 py-3.5 rounded-2xl bg-white hover:bg-slate-100 text-slate-900 text-sm font-bold shadow-xl shadow-white/10 hover:shadow-white/20 transition-all duration-200 active:scale-[0.98] cursor-pointer disabled:opacity-60"
              >
                {isSubmitting && !selectedEmail ? (
                  <Loader2 className="w-5 h-5 animate-spin text-slate-800" />
                ) : (
                  <GoogleIcon className="w-5 h-5" />
                )}
                <span>Continue with Google SSO</span>
                <ArrowRight className="w-4 h-4 ml-auto text-slate-500" />
              </button>

              <div className="relative flex items-center justify-center py-1">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-white/10" />
                </div>
                <span className="relative px-3 bg-[#0e1424] text-[10px] font-semibold tracking-wider uppercase text-slate-400">
                  Or test with 1-click enterprise role
                </span>
              </div>

              {/* 1-Click Demo Persona Fast-Track */}
              <div className="grid grid-cols-1 gap-2">
                {DEMO_PERSONAS.map((persona) => {
                  const isThisSelected =
                    selectedEmail === persona.email && isSubmitting;
                  return (
                    <button
                      key={persona.email}
                      type="button"
                      onClick={() => handlePersonaSelect(persona)}
                      disabled={isSubmitting}
                      className="auth-guard-persona-btn w-full flex items-center justify-between p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-indigo-600/15 hover:border-indigo-500/30 transition-all duration-200 text-left group cursor-pointer disabled:opacity-50"
                    >
                      <div className="flex items-center gap-3">
                        <img
                          src={persona.avatar}
                          alt={persona.name}
                          className="w-9 h-9 rounded-lg bg-indigo-950/50 border border-white/10 object-cover"
                        />
                        <div>
                          <div className="text-xs font-semibold text-white group-hover:text-indigo-200 flex items-center gap-1.5">
                            <span>{persona.name}</span>
                            <span className="text-[10px] px-1.5 py-0.2 rounded bg-indigo-500/20 text-indigo-300 font-normal">
                              {persona.roleLabel}
                            </span>
                          </div>
                          <div className="text-[11px] text-slate-400">
                            {persona.tag}
                          </div>
                        </div>
                      </div>

                      <div className="pr-2">
                        {isThisSelected ? (
                          <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
                        ) : (
                          <span className="text-[11px] font-medium text-indigo-400 group-hover:text-cyan-300 flex items-center gap-1">
                            <span>Enter</span>
                            <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                          </span>
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Custom Account / Advanced Options */}
            <div className="pt-2 border-t border-white/10 flex items-center justify-between text-[11px] text-slate-400">
              <button
                type="button"
                onClick={() => setShowGoogleModal(true)}
                className="hover:text-indigo-300 transition-colors cursor-pointer flex items-center gap-1"
              >
                <KeyRound className="w-3 h-3" />
                <span>Custom work email</span>
              </button>

              <span className="flex items-center gap-1 text-[10px] text-slate-500">
                <ShieldCheck className="w-3 h-3 text-emerald-400" />
                <span>256-bit JWT • Google OAuth 2.0 PKCE</span>
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Floating Welcome Toast when successfully unblurred */}
      {justUnlocked && (
        <div className="fixed top-5 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-5 py-3 rounded-2xl bg-emerald-950/95 border border-emerald-500/40 text-emerald-200 shadow-2xl shadow-emerald-950/80 backdrop-blur-xl animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="w-7 h-7 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
            <CheckCircle2 className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-white flex items-center gap-1.5">
              <span>Enterprise Workspace Unlocked</span>
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            </div>
            <div className="text-[11px] text-emerald-300">
              Authenticated as{" "}
              <span className="font-semibold text-white">{unlockedUser}</span>
            </div>
          </div>
        </div>
      )}

      {/* Google Sign-In & Sign-Up Modal */}
      <GoogleAuthModal
        isOpen={showGoogleModal}
        onClose={() => setShowGoogleModal(false)}
      />
    </div>
  );
}
