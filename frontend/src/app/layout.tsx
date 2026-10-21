import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Sidebar from '../components/Sidebar';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

export const metadata: Metadata = {
  title: 'NeuronForce | Autonomous AI-Powered CRM Platform',
  description:
    'A modern, high-performance alternative to Salesforce with transparent AI agents, sub-100ms latency, and clear cost/confidence observability.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full">
      <body className={`${inter.variable} bg-[#090d16] text-slate-100 min-h-screen flex antialiased selection:bg-indigo-500/30 selection:text-indigo-200`}>
        <Sidebar />
        <main className="flex-1 min-w-0 flex flex-col relative overflow-y-auto">
          {/* Ambient Glow */}
          <div className="absolute top-0 left-1/4 right-1/4 h-64 bg-indigo-600/10 blur-[120px] pointer-events-none -z-10 rounded-full" />
          <div className="absolute top-1/2 right-10 w-96 h-96 bg-cyan-500/5 blur-[140px] pointer-events-none -z-10 rounded-full" />
          {children}
        </main>
      </body>
    </html>
  );
}
