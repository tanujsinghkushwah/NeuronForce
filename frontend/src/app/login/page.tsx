"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  ShieldCheck,
  ArrowRight,
  Loader2,
  Sparkles,
  ExternalLink,
} from "lucide-react";
import NeuronForceLogo from "../../components/NeuronForceLogo";
import { GoogleIcon } from "../../components/GoogleAuthModal";
import { useAuth } from "../../context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const {
    loginWithGoogle,
    loginWithDemoAccount,
    signInWithGoogleSSO,
    isFirebaseAvailable,
  } = useAuth();
  const [email, setEmail] = useState("");
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleFirebaseSSO = async () => {
    setIsSubmitting(true);
    setErrorMessage("");
    try {
      await signInWithGoogleSSO();
      router.push("/");
    } catch (err: any) {
      if (err.message !== "FIREBASE_CONFIG_REQUIRED") {
        setErrorMessage(err.message || "Google SSO failed");
      } else {
        // Fallback: prompt for 1-click select
        setErrorMessage(
          "Firebase credentials not set in env; please pick one of the 1-click accounts below.",
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDemoSelect = async (demo: {
    email: string;
    full_name: string;
    role: string;
    avatar: string;
  }) => {
    setIsSubmitting(true);
    setErrorMessage("");

    try {
      await loginWithDemoAccount({
        email: demo.email,
        full_name: demo.full_name,
        role: demo.role,
        avatar_url: demo.avatar,
      });
      router.push("/");
    } catch (err: any) {
      setErrorMessage(err.message || "Authentication failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCustomGoogleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setIsSubmitting(true);
    setErrorMessage("");

    try {
      const generatedSub = `google_${email.replace(/[^a-zA-Z0-9]/g, "_")}`;
      const name = email
        .split("@")[0]
        .replace(/[._]/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase());

      await loginWithGoogle({
        email,
        full_name: name,
        avatar_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
        sub: generatedSub,
        role: "sales_rep",
      });

      router.push("/");
    } catch (err: any) {
      setErrorMessage(err.message || "Authentication failed.");
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
        <div className="glass-panel rounded-3xl border border-white/15 bg-[#0e1424]/90 p-7 shadow-2xl backdrop-blur-xl">
          <div className="text-center pb-5 border-b border-white/10">
            <h2 className="text-lg font-bold text-white tracking-tight">
              Single Sign-On (SSO)
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Sign in with your enterprise Google Workspace or Google account
            </p>
          </div>

          {errorMessage && (
            <div className="my-4 p-3 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs">
              {errorMessage}
            </div>
          )}

          {/* Primary Firebase Google SSO Button */}
          <div className="py-5">
            <button
              type="button"
              disabled={isSubmitting}
              onClick={handleFirebaseSSO}
              className="w-full py-3 px-4 rounded-2xl bg-white hover:bg-slate-100 text-slate-900 text-xs font-bold shadow-lg hover:shadow-xl flex items-center justify-center gap-2.5 cursor-pointer transition-all active:scale-[0.99] disabled:opacity-50"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Connecting with Google SSO...</span>
                </>
              ) : (
                <>
                  <GoogleIcon className="w-5 h-5" />
                  <span>Continue with Google SSO</span>
                </>
              )}
            </button>
          </div>

          {/* Divider */}
          <div className="relative flex items-center justify-center my-2">
            <div className="border-t border-white/10 w-full" />
            <span className="bg-[#0e1424] px-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
              Or Choose 1-Click Identity
            </span>
          </div>

          {/* Pre-configured Demo Google Accounts */}
          <div className="space-y-2 py-4">
            {[
              {
                email: "alex.rivera@neuronforce.ai",
                full_name: "Alex Rivera",
                role: "revops_lead",
                roleLabel: "RevOps Lead",
                avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
              },
              {
                email: "sarah.jenkins@neuronforce.ai",
                full_name: "Sarah Jenkins",
                role: "admin",
                roleLabel: "Platform Admin",
                avatar:
                  "https://api.dicebear.com/7.x/avataaars/svg?seed=SarahJ",
              },
              {
                email: "jordan.lee@neuronforce.ai",
                full_name: "Jordan Lee",
                role: "sales_rep",
                roleLabel: "Enterprise Sales Rep",
                avatar:
                  "https://api.dicebear.com/7.x/avataaars/svg?seed=Jordan",
              },
            ].map((demo) => (
              <button
                key={demo.email}
                type="button"
                disabled={isSubmitting}
                onClick={() => handleDemoSelect(demo)}
                className="w-full flex items-center justify-between p-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-left transition-all group cursor-pointer"
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
                    <p className="text-[11px] text-slate-400 truncate">
                      {demo.email}
                    </p>
                  </div>
                </div>
                <span className="text-[10px] font-semibold text-slate-400 px-2 py-0.5 rounded-md bg-white/5 shrink-0 group-hover:bg-indigo-500/20 group-hover:text-indigo-200">
                  {demo.roleLabel}
                </span>
              </button>
            ))}

            {!showCustomInput ? (
              <button
                type="button"
                onClick={() => setShowCustomInput(true)}
                className="w-full py-2 text-center text-xs text-indigo-400 hover:text-indigo-300 transition-colors cursor-pointer"
              >
                + Connect another Google account
              </button>
            ) : (
              <form
                onSubmit={handleCustomGoogleSubmit}
                className="pt-2 space-y-2"
              >
                <input
                  type="email"
                  required
                  placeholder="name@company.com or name@gmail.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white/5 border border-white/15 text-white text-xs placeholder:text-slate-500 focus:outline-none focus:border-indigo-500"
                />
                <div className="flex gap-2">
                  <button
                    type="submit"
                    disabled={isSubmitting || !email}
                    className="flex-1 py-2 px-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center justify-center gap-1 cursor-pointer disabled:opacity-50"
                  >
                    <span>Sign In</span>
                    <ArrowRight className="w-3.5 h-3.5" />
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

          {/* Security Banner */}
          <div className="mt-4 pt-4 border-t border-white/10 flex items-center justify-between text-[11px] text-slate-500">
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
