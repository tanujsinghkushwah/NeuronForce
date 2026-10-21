'use client';

import React from 'react';

interface NeuronForceLogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  showSubtitle?: boolean;
}

/**
 * NeuronForce Platform Vision Logo
 * Symbolism:
 * - Neural nodes & synaptic pathways: Cognitive AI decision engine & autonomous agents.
 * - Dynamic forward Force vector: Velocity, sales acceleration, and cloud CRM momentum.
 * - Glowing nexus core: Seamless fusion of deterministic CRM data with autonomous reasoning.
 */
export function NeuronForceIcon({ className = 'w-9 h-9' }: { className?: string }) {
  return (
    <div className={`relative flex items-center justify-center shrink-0 ${className}`}>
      {/* Ambient Glow */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-tr from-indigo-600 via-cyan-500 to-indigo-400 opacity-30 blur-md transform group-hover:scale-110 transition-transform duration-300 pointer-events-none" />

      {/* High-Definition Vector Logo */}
      <svg
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full relative z-10 drop-shadow-[0_2px_10px_rgba(99,102,241,0.5)] transform group-hover:scale-105 transition-transform duration-300"
      >
        <defs>
          {/* Main Neural Gradient */}
          <linearGradient id="nf-primary-grad" x1="4" y1="4" x2="44" y2="44" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#818CF8" /> {/* Indigo-400 */}
            <stop offset="50%" stopColor="#4F46E5" /> {/* Indigo-600 */}
            <stop offset="100%" stopColor="#06B6D4" /> {/* Cyan-500 */}
          </linearGradient>

          {/* Force Velocity Gradient */}
          <linearGradient id="nf-force-bolt" x1="16" y1="8" x2="32" y2="40" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#38BDF8" /> {/* Sky-400 */}
            <stop offset="60%" stopColor="#6366F1" /> {/* Indigo-500 */}
            <stop offset="100%" stopColor="#A855F7" /> {/* Purple-500 */}
          </linearGradient>

          {/* Node Glow Gradient */}
          <linearGradient id="nf-node-glow" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#67E8F9" />
            <stop offset="100%" stopColor="#3B82F6" />
          </linearGradient>

          {/* Ambient Inner Shadow / Glow */}
          <radialGradient id="nf-core-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#0F172A" stopOpacity="0.95" />
          </radialGradient>
        </defs>

        {/* Squircle Background Shield */}
        <rect
          x="3"
          y="3"
          width="42"
          height="42"
          rx="12"
          fill="url(#nf-core-glow)"
          stroke="url(#nf-primary-grad)"
          strokeWidth="1.5"
          className="transition-all"
        />

        {/* Synaptic Network Pathways (Neural Interconnects) */}
        {/* Node 1 (Top Left) to Center */}
        <line x1="13" y1="14" x2="24" y2="22" stroke="#818CF8" strokeWidth="1.5" strokeOpacity="0.6" strokeDasharray="2 2" />
        {/* Node 2 (Top Right) to Center */}
        <line x1="35" y1="14" x2="24" y2="22" stroke="#38BDF8" strokeWidth="1.5" strokeOpacity="0.6" strokeDasharray="2 2" />
        {/* Node 3 (Bottom Left) to Node 4 (Bottom Right) */}
        <line x1="14" y1="34" x2="34" y2="34" stroke="#6366F1" strokeWidth="1.2" strokeOpacity="0.5" />
        {/* Center to Bottom Left */}
        <line x1="24" y1="26" x2="14" y2="34" stroke="#818CF8" strokeWidth="1.2" strokeOpacity="0.4" />
        {/* Center to Bottom Right */}
        <line x1="24" y1="26" x2="34" y2="34" stroke="#06B6D4" strokeWidth="1.2" strokeOpacity="0.4" />

        {/* Central "FORCE" Kinetic Bolt & Neural Pulse */}
        <path
          d="M26 9L15 24H23L21 39L33 22H25L26 9Z"
          fill="url(#nf-force-bolt)"
          stroke="#E0E7FF"
          strokeWidth="1"
          strokeLinejoin="round"
          className="filter drop-shadow-[0_0_6px_rgba(56,189,248,0.7)]"
        />

        {/* Neural Synapse Nodes (Orbiting Intelligence) */}
        {/* Top-Left Synapse */}
        <circle cx="13" cy="14" r="2.5" fill="url(#nf-node-glow)" stroke="#FFFFFF" strokeWidth="0.8" />
        {/* Top-Right Synapse */}
        <circle cx="35" cy="14" r="2.5" fill="url(#nf-node-glow)" stroke="#FFFFFF" strokeWidth="0.8" />
        {/* Bottom-Left Synapse */}
        <circle cx="14" cy="34" r="2" fill="#818CF8" stroke="#FFFFFF" strokeWidth="0.6" />
        {/* Bottom-Right Synapse */}
        <circle cx="34" cy="34" r="2" fill="#06B6D4" stroke="#FFFFFF" strokeWidth="0.6" />

        {/* Pulsing Core Micro-Light */}
        <circle cx="24" cy="23" r="1.5" fill="#FFFFFF" />
      </svg>
    </div>
  );
}

export default function NeuronForceLogo({
  className = '',
  size = 'md',
  showText = true,
  showSubtitle = true,
}: NeuronForceLogoProps) {
  const iconSizeClasses = {
    sm: 'w-7 h-7',
    md: 'w-9 h-9',
    lg: 'w-11 h-11',
  };

  const textClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  };

  return (
    <div className={`flex items-center gap-2.5 group ${className}`}>
      <NeuronForceIcon className={iconSizeClasses[size]} />

      {showText && (
        <div className="flex flex-col">
          <div className="flex items-center gap-1.5">
            <span className={`font-black tracking-tight text-white group-hover:text-indigo-200 transition-colors ${textClasses[size]}`}>
              Neuron<span className="bg-gradient-to-r from-indigo-400 via-sky-300 to-cyan-400 bg-clip-text text-transparent">Force</span>
            </span>
          </div>

          {showSubtitle && (
            <div className="flex items-center gap-1">
              <span className="text-[9px] uppercase font-bold tracking-widest text-slate-400 group-hover:text-slate-300 transition-colors">
                Autonomous AI Sales Cloud
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
