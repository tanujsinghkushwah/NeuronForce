/**
 * NeuronForce Centralized API Client
 * Connects frontend to the FastAPI REST backend with graceful fallback capabilities.
 */

import {
  Contact,
  ContactCreateInput,
  Deal,
  DealCreateInput,
  PipelineView,
  Activity,
  Task,
  AIAgentTask,
  AIAgentStats,
  CalendarEvent,
  DashboardStats,
  RevenueSnapshot,
  PerformanceMetrics,
  AppSettings,
  User,
  AuthResponse,
  GoogleAuthPayload,
  UserSession,
  Ticket,
  TicketMessage,
  TicketStats,
  Campaign,
  CampaignStats,
  CampaignTemplate,
  ConversionFunnel,
  RevenueForecast,
  AIAgentChatResponse,
  GlobalSearchResponse,
} from "../types/crm";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetcher<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const token =
      typeof window !== "undefined"
        ? localStorage.getItem("neuronforce_token")
        : null;
    const authHeaders: Record<string, string> = token
      ? { Authorization: `Bearer ${token}` }
      : {};

    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...authHeaders,
        ...(options?.headers || {}),
      },
      ...options,
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(
        `API Error ${res.status}: ${errorText || res.statusText}`,
      );
    }

    return (await res.json()) as T;
  } catch (err) {
    console.error(`Fetch failed for ${url}:`, err);
    throw err;
  }
}

export const api = {
  // Health
  getHealth: () =>
    fetcher<{ status: string; version: string; timestamp: string }>("/health"),

  // Dashboard
  getDashboard: () => fetcher<DashboardStats>("/dashboard"),

  // Contacts
  getContacts: (params?: {
    search?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.search) q.append("search", params.search);
    if (params?.status) q.append("status", params.status);
    if (params?.skip !== undefined) q.append("skip", String(params.skip));
    if (params?.limit !== undefined) q.append("limit", String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<Contact[]>(`/contacts${query}`);
  },
  getContact: (id: number) => fetcher<Contact>(`/contacts/${id}`),
  createContact: (data: ContactCreateInput) =>
    fetcher<Contact>("/contacts", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateContact: (id: number, data: Partial<ContactCreateInput>) =>
    fetcher<Contact>(`/contacts/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteContact: (id: number) =>
    fetcher<{ message: string }>(`/contacts/${id}`, {
      method: "DELETE",
    }),

  // Deals
  getDeals: (params?: {
    stage?: string;
    search?: string;
    skip?: number;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.stage) q.append("stage", params.stage);
    if (params?.search) q.append("search", params.search);
    if (params?.skip !== undefined) q.append("skip", String(params.skip));
    if (params?.limit !== undefined) q.append("limit", String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<Deal[]>(`/deals${query}`);
  },
  getDeal: (id: number) => fetcher<Deal>(`/deals/${id}`),
  getPipeline: () => fetcher<PipelineView>("/deals/pipeline"),
  createDeal: (data: DealCreateInput) =>
    fetcher<Deal>("/deals", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateDeal: (id: number, data: Partial<DealCreateInput>) =>
    fetcher<Deal>(`/deals/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteDeal: (id: number) =>
    fetcher<{ message: string }>(`/deals/${id}`, {
      method: "DELETE",
    }),

  // Activities
  getActivities: (params?: {
    contact_id?: number;
    deal_id?: number;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.contact_id) q.append("contact_id", String(params.contact_id));
    if (params?.deal_id) q.append("deal_id", String(params.deal_id));
    if (params?.limit) q.append("limit", String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<Activity[]>(`/activities${query}`);
  },
  createActivity: (data: Partial<Activity>) =>
    fetcher<Activity>("/activities", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  // Tasks
  getTasks: (params?: { status?: string }) => {
    const q = new URLSearchParams();
    if (params?.status) q.append("status", params.status);
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<Task[]>(`/tasks${query}`);
  },
  createTask: (data: Partial<Task>) =>
    fetcher<Task>("/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateTask: (id: number, data: Partial<Task>) =>
    fetcher<Task>(`/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  // AI Agents
  getAITasks: (params?: {
    task_type?: string;
    status?: string;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.task_type) q.append("task_type", params.task_type);
    if (params?.status) q.append("status", params.status);
    if (params?.limit) q.append("limit", String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<AIAgentTask[]>(`/ai-agents/tasks${query}`);
  },
  runAITask: (
    task_type: string,
    input_data: Record<string, any> = {},
    triggered_by = "user",
  ) => {
    return fetcher<AIAgentTask>("/ai-agents/tasks", {
      method: "POST",
      body: JSON.stringify({ task_type, input_data, triggered_by }),
    });
  },
  getAIStats: () => fetcher<AIAgentStats>("/ai-agents/stats"),
  sendAgentChat: (
    message: string,
    session_id = "default_session",
    context?: Record<string, any>,
  ) => {
    return fetcher<AIAgentChatResponse>("/ai-agents/chat", {
      method: "POST",
      body: JSON.stringify({ message, session_id, context }),
    });
  },
  resetAgentChat: (session_id = "default_session") => {
    return fetcher<{ status: string; message: string }>(
      `/ai-agents/chat/reset?session_id=${encodeURIComponent(session_id)}`,
      {
        method: "POST",
      },
    );
  },

  // Calendar
  getCalendarEvents: (params?: { start?: string; end?: string }) => {
    const q = new URLSearchParams();
    if (params?.start) q.append("start", params.start);
    if (params?.end) q.append("end", params.end);
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<CalendarEvent[]>(`/calendar/events${query}`);
  },
  createCalendarEvent: (data: Partial<CalendarEvent>) =>
    fetcher<CalendarEvent>("/calendar/events", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  deleteCalendarEvent: (id: number) =>
    fetcher<{ message: string }>(`/calendar/events/${id}`, {
      method: "DELETE",
    }),

  // Analytics
  getRevenueAnalytics: (days = 30) =>
    fetcher<RevenueSnapshot[]>(`/analytics/revenue?days=${days}`),
  getPerformanceMetrics: () =>
    fetcher<PerformanceMetrics>("/analytics/performance"),

  // Settings
  getSettings: () => fetcher<AppSettings>("/settings"),

  // Authentication & Google Sign-In
  googleAuth: (data: GoogleAuthPayload) =>
    fetcher<AuthResponse>("/auth/google", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getMe: () => fetcher<User>("/auth/me"),
  logout: () =>
    fetcher<{ message: string; status: string }>("/auth/logout", {
      method: "POST",
    }),
  getSessions: () => fetcher<UserSession[]>("/auth/sessions"),
  getDemoAccounts: () =>
    fetcher<
      Array<{
        id: number;
        email: string;
        full_name: string;
        avatar_url: string;
        role: string;
      }>
    >("/auth/demo-accounts"),

  // Service Cloud (Support Tickets & Cases)
  getTickets: (params?: {
    status?: string;
    priority?: string;
    category?: string;
    skip?: number;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.status) q.append("status", params.status);
    if (params?.priority) q.append("priority", params.priority);
    if (params?.category) q.append("category", params.category);
    if (params?.skip !== undefined) q.append("skip", String(params.skip));
    if (params?.limit !== undefined) q.append("limit", String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<Ticket[]>(`/tickets${query}`);
  },
  getTicket: (id: number) => fetcher<Ticket>(`/tickets/${id}`),
  createTicket: (data: Partial<Ticket> & { ai_triage?: boolean }) =>
    fetcher<Ticket>("/tickets", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateTicket: (id: number, data: Partial<Ticket>) =>
    fetcher<Ticket>(`/tickets/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  deleteTicket: (id: number) =>
    fetcher<{ message: string }>(`/tickets/${id}`, {
      method: "DELETE",
    }),
  addTicketMessage: (
    id: number,
    data: {
      body: string;
      author_name: string;
      author_email?: string;
      is_internal?: boolean;
    },
  ) =>
    fetcher<TicketMessage>(`/tickets/${id}/messages`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  runTicketAITriage: (id: number) =>
    fetcher<{
      ai_triage: Record<string, any>;
      sentiment: string;
      suggested_response: string;
    }>(`/tickets/${id}/ai-triage`, {
      method: "POST",
    }),
  getTicketStats: () => fetcher<TicketStats>("/tickets/stats"),

  // Marketing Cloud (Email Campaigns & Audiences)
  getCampaigns: (params?: {
    status?: string;
    skip?: number;
    limit?: number;
  }) => {
    const q = new URLSearchParams();
    if (params?.status) q.append("status", params.status);
    if (params?.skip !== undefined) q.append("skip", String(params.skip));
    if (params?.limit !== undefined) q.append("limit", String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : "";
    return fetcher<Campaign[]>(`/campaigns${query}`);
  },
  getCampaign: (id: number) => fetcher<Campaign>(`/campaigns/${id}`),
  createCampaign: (data: Partial<Campaign>) =>
    fetcher<Campaign>("/campaigns", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  updateCampaign: (id: number, data: Partial<Campaign>) =>
    fetcher<Campaign>(`/campaigns/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),
  deleteCampaign: (id: number) =>
    fetcher<{ message: string }>(`/campaigns/${id}`, {
      method: "DELETE",
    }),
  sendCampaign: (id: number) =>
    fetcher<Campaign>(`/campaigns/${id}/send`, {
      method: "POST",
    }),
  optimizeCampaignAI: (id: number) =>
    fetcher<Campaign>(`/campaigns/${id}/ai-optimize`, {
      method: "POST",
    }),
  getCampaignStats: () => fetcher<CampaignStats>("/campaigns/stats"),
  getCampaignTemplates: () =>
    fetcher<CampaignTemplate[]>("/campaigns/templates"),

  // Tableau / BI Reports & CSV Exports
  getConversionFunnel: () => fetcher<ConversionFunnel>("/analytics/funnel"),
  getRevenueForecast: () => fetcher<RevenueForecast>("/analytics/forecast"),
  getTicketReport: () =>
    fetcher<{
      summary: {
        total: number;
        open: number;
        resolved: number;
        sla_breached: number;
        avg_resolution_hours: number;
        resolution_rate: number;
      };
      by_priority: Array<{ priority: string; count: number }>;
      by_category: Array<{ category: string; count: number }>;
    }>("/analytics/reports/tickets"),
  getCampaignReport: () =>
    fetcher<{
      summary: {
        total_campaigns: number;
        total_sent: number;
        avg_open_rate: number;
        avg_click_rate: number;
        total_revenue_attributed: number;
      };
      records: Array<{
        id: number;
        name: string;
        subject: string;
        emails_sent: number;
        open_rate: number;
        click_rate: number;
        revenue_attributed: number;
        ai_score: number;
        sent_at: string | null;
      }>;
    }>("/analytics/reports/campaigns"),
  getDealsExportUrl: (params?: {
    start_date?: string;
    end_date?: string;
    stage?: string;
  }) => {
    const q = new URLSearchParams();
    if (params?.start_date) q.append("start_date", params.start_date);
    if (params?.end_date) q.append("end_date", params.end_date);
    if (params?.stage) q.append("stage", params.stage);
    const query = q.toString() ? `?${q.toString()}` : "";
    return `${API_BASE}/analytics/export/deals${query}`;
  },
  getContactsExportUrl: (params?: {
    lead_status?: string;
    source?: string;
  }) => {
    const q = new URLSearchParams();
    if (params?.lead_status) q.append("lead_status", params.lead_status);
    if (params?.source) q.append("source", params.source);
    const query = q.toString() ? `?${q.toString()}` : "";
    return `${API_BASE}/analytics/export/contacts${query}`;
  },

  // Global Multi-Entity Search
  globalSearch: (q: string, limit = 20) => {
    const query = new URLSearchParams();
    if (q) query.append("q", q);
    if (limit) query.append("limit", String(limit));
    const qs = query.toString() ? `?${query.toString()}` : "";
    return fetcher<GlobalSearchResponse>(`/search${qs}`);
  },
};
