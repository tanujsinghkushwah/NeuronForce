"use client";

import React, { useState, useEffect, useRef, useMemo, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  Search,
  X,
  Loader2,
  Users,
  Kanban,
  Sparkles,
  LifeBuoy,
  Megaphone,
  Compass,
  ArrowRight,
  ExternalLink,
  CornerDownLeft,
  ChevronRight,
  User as UserIcon,
} from "lucide-react";
import { api } from "../lib/api";
import { GlobalSearchResultItem, GlobalSearchResponse } from "../types/crm";

interface GlobalSearchProps {
  placeholder?: string;
  className?: string;
}

type CategoryTab = "all" | "contacts" | "deals" | "agents" | "tickets" | "campaigns" | "navigation";

export default function GlobalSearch({
  placeholder = "Search deals, contacts, agents... (⌘K)",
  className = "",
}: GlobalSearchProps) {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<CategoryTab>("all");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [results, setResults] = useState<GlobalSearchResponse | null>(null);

  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const resultsListRef = useRef<HTMLDivElement>(null);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Platform detection for keyboard shortcut label
  const isMac = typeof window !== "undefined" && navigator.platform.toUpperCase().indexOf("MAC") >= 0;

  // Perform search against backend API
  const performSearch = useCallback(async (searchQuery: string) => {
    try {
      setLoading(true);
      const data = await api.globalSearch(searchQuery.trim());
      setResults(data);
      setSelectedIndex(0);
    } catch (err) {
      console.warn("Global search backend fetch failed, using fallback:", err);
      // Fallback data if offline or tunnel interrupted
      setResults({
        query: searchQuery,
        total: 2,
        items: [
          {
            id: "fallback-contacts",
            type: "navigation",
            title: "Contacts Directory",
            subtitle: "Browse contacts and leads",
            badge: "CRM",
            badge_color: "indigo",
            href: `/contacts?search=${encodeURIComponent(searchQuery)}`,
          },
          {
            id: "fallback-deals",
            type: "navigation",
            title: "Deals Pipeline",
            subtitle: "Browse deals and revenue stages",
            badge: "Pipeline",
            badge_color: "purple",
            href: `/deals?search=${encodeURIComponent(searchQuery)}`,
          },
        ],
        categories: {
          navigation: [
            {
              id: "fallback-contacts",
              type: "navigation",
              title: "Contacts Directory",
              subtitle: "Browse contacts and leads",
              badge: "CRM",
              badge_color: "indigo",
              href: `/contacts?search=${encodeURIComponent(searchQuery)}`,
            },
            {
              id: "fallback-deals",
              type: "navigation",
              title: "Deals Pipeline",
              subtitle: "Browse deals and revenue stages",
              badge: "Pipeline",
              badge_color: "purple",
              href: `/deals?search=${encodeURIComponent(searchQuery)}`,
            },
          ],
        },
      });
    } finally {
      setLoading(false);
    }
  }, []);

  // Handle typing with 150ms debounce
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setQuery(val);
    if (!isOpen) setIsOpen(true);

    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(() => {
      performSearch(val);
    }, 150);
  };

  // Focus and open search
  const handleFocus = () => {
    setIsOpen(true);
    if (!results) {
      performSearch(query);
    }
  };

  // Close dropdown and clear
  const handleClear = () => {
    setQuery("");
    setSelectedIndex(0);
    performSearch("");
    inputRef.current?.focus();
  };

  const handleClose = () => {
    setIsOpen(false);
    setSelectedIndex(0);
  };

  // Global keyboard shortcuts: ⌘K or Ctrl+K to open, Escape to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setIsOpen(true);
        inputRef.current?.focus();
        inputRef.current?.select();
      } else if (e.key === "Escape" && isOpen) {
        e.preventDefault();
        handleClose();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen]);

  // Click outside to close
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Filter items by active category tab
  const displayedItems = useMemo<GlobalSearchResultItem[]>(() => {
    if (!results) return [];
    if (activeTab === "all") {
      return results.items || [];
    }
    const catItems = results.categories[activeTab];
    return catItems || [];
  }, [results, activeTab]);

  // Keyboard navigation up / down / enter
  const handleListKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen || displayedItems.length === 0) {
      if (e.key === "Enter" && query.trim()) {
        router.push(`/contacts?search=${encodeURIComponent(query.trim())}`);
        handleClose();
      }
      return;
    }

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % displayedItems.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + displayedItems.length) % displayedItems.length);
    } else if (e.key === "Enter") {
      e.preventDefault();
      const currentItem = displayedItems[selectedIndex];
      if (currentItem) {
        navigateToItem(currentItem);
      }
    }
  };

  // Scroll selected item into view in list
  useEffect(() => {
    if (resultsListRef.current && isOpen) {
      const activeEl = resultsListRef.current.querySelector(`[data-index="${selectedIndex}"]`);
      if (activeEl) {
        activeEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }
    }
  }, [selectedIndex, isOpen]);

  // Navigate to target item
  const navigateToItem = (item: GlobalSearchResultItem) => {
    handleClose();
    router.push(item.href);
  };

  // Helper to highlight matched query tokens
  const highlightMatches = (text: string, highlightQuery: string) => {
    if (!highlightQuery.trim()) return text;
    const tokens = highlightQuery
      .trim()
      .split(/\s+/)
      .filter((t) => t.length > 1 && !["and", "or", "the", "in", "with", "&"].includes(t.toLowerCase()));

    if (tokens.length === 0) return text;

    try {
      const regex = new RegExp(`(${tokens.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`, "gi");
      const parts = text.split(regex);
      return parts.map((part, i) =>
        regex.test(part) ? (
          <span key={i} className="text-indigo-400 font-bold bg-indigo-500/20 px-0.5 rounded">
            {part}
          </span>
        ) : (
          part
        ),
      );
    } catch {
      return text;
    }
  };

  // Category Icon Resolver
  const getItemIcon = (type: GlobalSearchResultItem["type"]) => {
    switch (type) {
      case "contact":
        return <Users className="w-4 h-4 text-emerald-400" />;
      case "deal":
        return <Kanban className="w-4 h-4 text-purple-400" />;
      case "agent":
        return <Sparkles className="w-4 h-4 text-cyan-400" />;
      case "ticket":
        return <LifeBuoy className="w-4 h-4 text-rose-400" />;
      case "campaign":
        return <Megaphone className="w-4 h-4 text-amber-400" />;
      case "navigation":
      default:
        return <Compass className="w-4 h-4 text-blue-400" />;
    }
  };

  // Badge Color Resolver
  const getBadgeClass = (color?: string) => {
    switch (color) {
      case "emerald":
        return "bg-emerald-500/15 text-emerald-300 border-emerald-500/30";
      case "purple":
        return "bg-purple-500/15 text-purple-300 border-purple-500/30";
      case "cyan":
        return "bg-cyan-500/15 text-cyan-300 border-cyan-500/30";
      case "rose":
        return "bg-rose-500/15 text-rose-300 border-rose-500/30";
      case "amber":
        return "bg-amber-500/15 text-amber-300 border-amber-500/30";
      case "blue":
        return "bg-blue-500/15 text-blue-300 border-blue-500/30";
      case "slate":
      default:
        return "bg-slate-800 text-slate-300 border-white/10";
    }
  };

  // Category counts
  const counts = {
    contacts: results?.categories.contacts?.length || 0,
    deals: results?.categories.deals?.length || 0,
    agents: results?.categories.agents?.length || 0,
    tickets: results?.categories.tickets?.length || 0,
    campaigns: results?.categories.campaigns?.length || 0,
    navigation: results?.categories.navigation?.length || 0,
  };

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      {/* ─── Search Bar Input ─── */}
      <div className="relative flex items-center">
        {loading ? (
          <Loader2 className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-indigo-400 animate-spin" />
        ) : (
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
        )}

        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleInputChange}
          onFocus={handleFocus}
          onKeyDown={handleListKeyDown}
          placeholder={placeholder}
          aria-label="Global search across deals, contacts, agents, and tickets"
          className="w-full h-9 pl-9 pr-14 rounded-xl bg-slate-900/90 border border-white/10 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all shadow-inner"
        />

        {/* Clear or Keyboard Shortcut Indicator */}
        <div className="absolute right-2.5 top-1/2 -translate-y-1/2 flex items-center gap-1.5">
          {query ? (
            <button
              onClick={handleClear}
              className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
              title="Clear search"
            >
              <X className="w-3 h-3" />
            </button>
          ) : (
            <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] font-mono font-medium text-slate-400 bg-white/5 border border-white/10 rounded-md">
              {isMac ? "⌘" : "Ctrl+"}K
            </kbd>
          )}
        </div>
      </div>

      {/* ─── Dropdown Results Modal / Flyout ─── */}
      {isOpen && (
        <div className="absolute left-0 sm:left-auto sm:right-0 mt-2 w-[92vw] sm:w-[560px] md:w-[620px] max-w-[95vw] rounded-2xl bg-[#0c1220]/95 border border-white/15 p-3 shadow-2xl backdrop-blur-2xl z-50 animate-fadeIn text-left text-slate-200">
          {/* Category Filter Pills */}
          <div className="flex items-center gap-1.5 pb-2.5 mb-2 border-b border-white/10 overflow-x-auto no-scrollbar">
            <button
              onClick={() => {
                setActiveTab("all");
                setSelectedIndex(0);
              }}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                activeTab === "all"
                  ? "bg-indigo-600 text-white font-semibold shadow-sm"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <span>All</span>
              {results && (
                <span className="text-[10px] opacity-75">({results.total})</span>
              )}
            </button>

            {counts.contacts > 0 && (
              <button
                onClick={() => {
                  setActiveTab("contacts");
                  setSelectedIndex(0);
                }}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                  activeTab === "contacts"
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Users className="w-3 h-3 text-emerald-400" />
                <span>Contacts</span>
                <span className="text-[10px] opacity-75">({counts.contacts})</span>
              </button>
            )}

            {counts.deals > 0 && (
              <button
                onClick={() => {
                  setActiveTab("deals");
                  setSelectedIndex(0);
                }}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                  activeTab === "deals"
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Kanban className="w-3 h-3 text-purple-400" />
                <span>Deals</span>
                <span className="text-[10px] opacity-75">({counts.deals})</span>
              </button>
            )}

            {counts.agents > 0 && (
              <button
                onClick={() => {
                  setActiveTab("agents");
                  setSelectedIndex(0);
                }}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                  activeTab === "agents"
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Sparkles className="w-3 h-3 text-cyan-400" />
                <span>AI Agents</span>
                <span className="text-[10px] opacity-75">({counts.agents})</span>
              </button>
            )}

            {counts.tickets > 0 && (
              <button
                onClick={() => {
                  setActiveTab("tickets");
                  setSelectedIndex(0);
                }}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                  activeTab === "tickets"
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <LifeBuoy className="w-3 h-3 text-rose-400" />
                <span>Tickets</span>
                <span className="text-[10px] opacity-75">({counts.tickets})</span>
              </button>
            )}

            {counts.campaigns > 0 && (
              <button
                onClick={() => {
                  setActiveTab("campaigns");
                  setSelectedIndex(0);
                }}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                  activeTab === "campaigns"
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Megaphone className="w-3 h-3 text-amber-400" />
                <span>Campaigns</span>
                <span className="text-[10px] opacity-75">({counts.campaigns})</span>
              </button>
            )}

            {counts.navigation > 0 && (
              <button
                onClick={() => {
                  setActiveTab("navigation");
                  setSelectedIndex(0);
                }}
                className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors cursor-pointer flex items-center gap-1 shrink-0 ${
                  activeTab === "navigation"
                    ? "bg-indigo-600 text-white font-semibold"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Compass className="w-3 h-3 text-blue-400" />
                <span>Navigation</span>
                <span className="text-[10px] opacity-75">({counts.navigation})</span>
              </button>
            )}
          </div>

          {/* ─── Search Results List ─── */}
          <div
            ref={resultsListRef}
            className="max-h-[380px] overflow-y-auto space-y-1 pr-1 custom-scrollbar"
          >
            {displayedItems.length > 0 ? (
              displayedItems.map((item, idx) => {
                const isSelected = idx === selectedIndex;

                return (
                  <div
                    key={item.id}
                    data-index={idx}
                    onClick={() => navigateToItem(item)}
                    onMouseEnter={() => setSelectedIndex(idx)}
                    className={`group flex items-center justify-between p-2.5 rounded-xl cursor-pointer transition-all ${
                      isSelected
                        ? "bg-indigo-600/20 border border-indigo-500/40 text-white shadow-sm"
                        : "hover:bg-white/5 border border-transparent text-slate-300"
                    }`}
                  >
                    <div className="flex items-center gap-3 min-w-0 pr-2">
                      {/* Avatar or Category Icon */}
                      {item.type === "contact" && item.meta?.avatar_url ? (
                        <img
                          src={item.meta.avatar_url}
                          alt={item.title}
                          className="w-8 h-8 rounded-full bg-slate-800 ring-1 ring-white/10 shrink-0 object-cover"
                        />
                      ) : (
                        <div
                          className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 border border-white/10 ${
                            item.type === "contact"
                              ? "bg-emerald-500/10"
                              : item.type === "deal"
                              ? "bg-purple-500/10"
                              : item.type === "agent"
                              ? "bg-cyan-500/10"
                              : item.type === "ticket"
                              ? "bg-rose-500/10"
                              : item.type === "campaign"
                              ? "bg-amber-500/10"
                              : "bg-blue-500/10"
                          }`}
                        >
                          {getItemIcon(item.type)}
                        </div>
                      )}

                      {/* Title & Subtitle */}
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-semibold text-white truncate leading-tight group-hover:text-indigo-200">
                            {highlightMatches(item.title, query)}
                          </span>
                          {item.badge && (
                            <span
                              className={`text-[9px] font-semibold px-1.5 py-0.5 rounded-full border shrink-0 ${getBadgeClass(
                                item.badge_color,
                              )}`}
                            >
                              {item.badge}
                            </span>
                          )}
                        </div>
                        {item.subtitle && (
                          <p className="text-[11px] text-slate-400 truncate mt-0.5 leading-tight">
                            {highlightMatches(item.subtitle, query)}
                          </p>
                        )}
                      </div>
                    </div>

                    {/* Right Action Hint */}
                    <div className="flex items-center gap-1.5 shrink-0 text-slate-400">
                      {isSelected && (
                        <span className="hidden sm:inline-flex items-center gap-1 text-[10px] font-mono text-indigo-300 bg-indigo-500/20 px-1.5 py-0.5 rounded border border-indigo-500/30">
                          <span>Open</span>
                          <CornerDownLeft className="w-2.5 h-2.5" />
                        </span>
                      )}
                      <ChevronRight
                        className={`w-3.5 h-3.5 transition-transform ${
                          isSelected ? "text-white translate-x-0.5" : "text-slate-600"
                        }`}
                      />
                    </div>
                  </div>
                );
              })
            ) : query.trim() ? (
              /* No Results State */
              <div className="py-8 px-4 text-center">
                <div className="w-10 h-10 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mx-auto mb-3 text-slate-400">
                  <Search className="w-5 h-5" />
                </div>
                <h4 className="text-xs font-semibold text-white">No results found for &ldquo;{query}&rdquo;</h4>
                <p className="text-[11px] text-slate-400 mt-1 max-w-sm mx-auto">
                  Try searching for contacts like &ldquo;Robert&rdquo; or &ldquo;Tanuj&rdquo;, companies like &ldquo;TechCorp&rdquo;, or &ldquo;AI Agents&rdquo;.
                </p>
                <div className="mt-4 flex flex-wrap items-center justify-center gap-1.5">
                  {["Robert Williams", "Tanuj", "TechCorp", "AI Agents", "Deals Pipeline"].map((suggestion) => (
                    <button
                      key={suggestion}
                      onClick={() => {
                        setQuery(suggestion);
                        performSearch(suggestion);
                      }}
                      className="text-[11px] px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-indigo-300 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              /* Empty Query Quick Suggestions State */
              <div className="py-3 px-2">
                <div className="px-2 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                  Quick Navigation & Suggestions
                </div>
                <div className="grid grid-cols-2 gap-1.5 mb-3">
                  {[
                    { label: "Robert Williams", type: "contact", query: "Robert" },
                    { label: "Tanuj (Account)", type: "contact", query: "Tanuj" },
                    { label: "TechCorp Deals", type: "deal", query: "TechCorp" },
                    { label: "Lead Scoring Agent", type: "agent", query: "lead scoring" },
                  ].map((s) => (
                    <button
                      key={s.label}
                      onClick={() => {
                        setQuery(s.query);
                        performSearch(s.query);
                      }}
                      className="flex items-center gap-2 p-2 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-left transition-colors cursor-pointer group"
                    >
                      <Search className="w-3 h-3 text-indigo-400 group-hover:scale-110 transition-transform" />
                      <span className="text-xs text-slate-200 group-hover:text-white font-medium truncate">
                        {s.label}
                      </span>
                    </button>
                  ))}
                </div>

                <div className="px-2 pt-2 border-t border-white/10 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                  Jump to Section
                </div>
                <div className="grid grid-cols-3 gap-1.5 mt-2">
                  {[
                    { name: "Deals", href: "/deals", icon: Kanban },
                    { name: "Contacts", href: "/contacts", icon: Users },
                    { name: "AI Agents", href: "/ai-agents", icon: Sparkles },
                    { name: "Campaigns", href: "/campaigns", icon: Megaphone },
                    { name: "Tickets", href: "/tickets", icon: LifeBuoy },
                    { name: "Analytics", href: "/analytics", icon: Compass },
                  ].map((dest) => {
                    const Icon = dest.icon;
                    return (
                      <button
                        key={dest.name}
                        onClick={() => {
                          handleClose();
                          router.push(dest.href);
                        }}
                        className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-xs text-slate-300 hover:text-white transition-colors"
                      >
                        <Icon className="w-3.5 h-3.5 text-indigo-400" />
                        <span>{dest.name}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* ─── Footer with Navigation Shortcuts ─── */}
          <div className="mt-2.5 pt-2 border-t border-white/10 flex items-center justify-between text-[10px] text-slate-400 px-1">
            <div className="flex items-center gap-3">
              <span className="flex items-center gap-1">
                <kbd className="px-1 py-0.5 bg-white/5 border border-white/10 rounded font-mono">↑</kbd>
                <kbd className="px-1 py-0.5 bg-white/5 border border-white/10 rounded font-mono">↓</kbd>
                <span className="hidden sm:inline">to navigate</span>
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-white/5 border border-white/10 rounded font-mono">↵</kbd>
                <span className="hidden sm:inline">to select</span>
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-white/5 border border-white/10 rounded font-mono">esc</kbd>
                <span className="hidden sm:inline">to close</span>
              </span>
            </div>
            <div className="flex items-center gap-1 text-slate-400">
              <span>NeuronForce Omnisearch</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
