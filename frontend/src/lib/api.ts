/**
 * NeuronForce Centralized API Client
 * Connects frontend to the FastAPI REST backend with graceful fallback capabilities.
 */

import {
  Contact, ContactCreateInput,
  Deal, DealCreateInput, PipelineView,
  Activity, Task,
  AIAgentTask, AIAgentStats,
  CalendarEvent, DashboardStats,
  RevenueSnapshot, PerformanceMetrics, AppSettings
} from '../types/crm';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

async function fetcher<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
      ...options,
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`API Error ${res.status}: ${errorText || res.statusText}`);
    }

    return await res.json() as T;
  } catch (err) {
    console.error(`Fetch failed for ${url}:`, err);
    throw err;
  }
}

export const api = {
  // Health
  getHealth: () => fetcher<{ status: string; version: string; timestamp: string }>('/health'),

  // Dashboard
  getDashboard: () => fetcher<DashboardStats>('/dashboard'),

  // Contacts
  getContacts: (params?: { search?: string; status?: string; skip?: number; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.search) q.append('search', params.search);
    if (params?.status) q.append('status', params.status);
    if (params?.skip !== undefined) q.append('skip', String(params.skip));
    if (params?.limit !== undefined) q.append('limit', String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : '';
    return fetcher<Contact[]>(`/contacts${query}`);
  },
  getContact: (id: number) => fetcher<Contact>(`/contacts/${id}`),
  createContact: (data: ContactCreateInput) => fetcher<Contact>('/contacts', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateContact: (id: number, data: Partial<ContactCreateInput>) => fetcher<Contact>(`/contacts/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteContact: (id: number) => fetcher<{ message: string }>(`/contacts/${id}`, {
    method: 'DELETE',
  }),

  // Deals
  getDeals: (params?: { stage?: string; search?: string; skip?: number; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.stage) q.append('stage', params.stage);
    if (params?.search) q.append('search', params.search);
    if (params?.skip !== undefined) q.append('skip', String(params.skip));
    if (params?.limit !== undefined) q.append('limit', String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : '';
    return fetcher<Deal[]>(`/deals${query}`);
  },
  getDeal: (id: number) => fetcher<Deal>(`/deals/${id}`),
  getPipeline: () => fetcher<PipelineView>('/deals/pipeline'),
  createDeal: (data: DealCreateInput) => fetcher<Deal>('/deals', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateDeal: (id: number, data: Partial<DealCreateInput>) => fetcher<Deal>(`/deals/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  deleteDeal: (id: number) => fetcher<{ message: string }>(`/deals/${id}`, {
    method: 'DELETE',
  }),

  // Activities
  getActivities: (params?: { contact_id?: number; deal_id?: number; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.contact_id) q.append('contact_id', String(params.contact_id));
    if (params?.deal_id) q.append('deal_id', String(params.deal_id));
    if (params?.limit) q.append('limit', String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : '';
    return fetcher<Activity[]>(`/activities${query}`);
  },
  createActivity: (data: Partial<Activity>) => fetcher<Activity>('/activities', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // Tasks
  getTasks: (params?: { status?: string }) => {
    const q = new URLSearchParams();
    if (params?.status) q.append('status', params.status);
    const query = q.toString() ? `?${q.toString()}` : '';
    return fetcher<Task[]>(`/tasks${query}`);
  },
  createTask: (data: Partial<Task>) => fetcher<Task>('/tasks', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateTask: (id: number, data: Partial<Task>) => fetcher<Task>(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  // AI Agents
  getAITasks: (params?: { task_type?: string; status?: string; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.task_type) q.append('task_type', params.task_type);
    if (params?.status) q.append('status', params.status);
    if (params?.limit) q.append('limit', String(params.limit));
    const query = q.toString() ? `?${q.toString()}` : '';
    return fetcher<AIAgentTask[]>(`/ai-agents/tasks${query}`);
  },
  runAITask: (task_type: string, input_data: Record<string, any> = {}, triggered_by = 'user') => {
    return fetcher<AIAgentTask>('/ai-agents/tasks', {
      method: 'POST',
      body: JSON.stringify({ task_type, input_data, triggered_by }),
    });
  },
  getAIStats: () => fetcher<AIAgentStats>('/ai-agents/stats'),

  // Calendar
  getCalendarEvents: (params?: { start?: string; end?: string }) => {
    const q = new URLSearchParams();
    if (params?.start) q.append('start', params.start);
    if (params?.end) q.append('end', params.end);
    const query = q.toString() ? `?${q.toString()}` : '';
    return fetcher<CalendarEvent[]>(`/calendar/events${query}`);
  },
  createCalendarEvent: (data: Partial<CalendarEvent>) => fetcher<CalendarEvent>('/calendar/events', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  deleteCalendarEvent: (id: number) => fetcher<{ message: string }>(`/calendar/events/${id}`, {
    method: 'DELETE',
  }),

  // Analytics
  getRevenueAnalytics: (days = 30) => fetcher<RevenueSnapshot[]>(`/analytics/revenue?days=${days}`),
  getPerformanceMetrics: () => fetcher<PerformanceMetrics>('/analytics/performance'),

  // Settings
  getSettings: () => fetcher<AppSettings>('/settings'),
};
