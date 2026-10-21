/**
 * NeuronForce CRM TypeScript Interfaces
 * Corresponds to backend Pydantic models & REST schemas.
 */

export type LeadStatus = 'new' | 'contacted' | 'qualified' | 'unqualified' | 'converted';

export type DealStage = 
  | 'prospecting' 
  | 'qualification' 
  | 'proposal' 
  | 'negotiation' 
  | 'closed_won' 
  | 'closed_lost';

export type Priority = 'low' | 'medium' | 'high' | 'critical';

export type TaskStatus = 'todo' | 'in_progress' | 'completed' | 'cancelled';

export interface Contact {
  id: number;
  first_name: string;
  last_name: string;
  email?: string | null;
  phone?: string | null;
  company?: string | null;
  job_title?: string | null;
  department?: string | null;
  industry?: string | null;
  website?: string | null;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  country?: string | null;
  avatar_url?: string | null;
  lead_status: LeadStatus;
  lead_score: number;
  source?: string | null;
  tags: string[];
  notes?: string | null;
  last_contacted?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ContactCreateInput {
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  company?: string;
  job_title?: string;
  department?: string;
  industry?: string;
  lead_status?: LeadStatus;
  lead_score?: number;
  source?: string;
  tags?: string[];
  notes?: string;
}

export interface Deal {
  id: number;
  title: string;
  value: number;
  currency: string;
  stage: DealStage;
  probability: number;
  expected_close_date?: string | null;
  actual_close_date?: string | null;
  description?: string | null;
  company?: string | null;
  owner?: string | null;
  priority: Priority;
  tags: string[];
  ai_win_probability?: number | null;
  ai_insights?: Record<string, any>;
  contacts: Contact[];
  created_at: string;
  updated_at: string;
}

export interface DealCreateInput {
  title: string;
  value?: number;
  currency?: string;
  stage?: DealStage;
  probability?: number;
  expected_close_date?: string;
  description?: string;
  company?: string;
  owner?: string;
  priority?: Priority;
  tags?: string[];
  contact_ids?: number[];
}

export interface PipelineView {
  stages: Record<string, Array<{
    id: number;
    title: string;
    value: number;
    company?: string;
    probability: number;
    owner?: string;
    priority: Priority;
    expected_close_date?: string | null;
    ai_win_probability?: number | null;
    tags: string[];
    contacts: Array<{ id: number; name: string; avatar_url?: string | null }>;
  }>>;
  total_value: number;
  weighted_value: number;
}

export interface Activity {
  id: number;
  type: string;
  subject: string;
  description?: string | null;
  contact_id?: number | null;
  deal_id?: number | null;
  duration_minutes?: number | null;
  outcome?: string | null;
  scheduled_at?: string | null;
  completed_at?: string | null;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string | null;
  status: TaskStatus;
  priority: Priority;
  due_date?: string | null;
  contact_id?: number | null;
  assigned_to?: string | null;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface AIAgentTask {
  id: number;
  task_type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  confidence_score?: number | null;
  cost_estimate?: number | null;
  actual_cost?: number | null;
  latency_ms?: number | null;
  error_message?: string | null;
  triggered_by: string;
  created_at: string;
  completed_at?: string | null;
}

export interface AIAgentStats {
  total_tasks: number;
  completed: number;
  failed: number;
  running: number;
  success_rate: number;
  total_cost: number;
  avg_latency_ms: number;
  avg_confidence: number;
  cost_by_type: Array<{
    type: string;
    cost: number;
    count: number;
    avg_latency: number;
  }>;
  cost_efficiency: {
    cost_per_task: number;
    roi_estimate: number;
    time_saved_hours: number;
  };
}

export interface CalendarEvent {
  id: number;
  title: string;
  description?: string | null;
  start_time: string;
  end_time: string;
  location?: string | null;
  event_type: string;
  attendees: string[];
  contact_id?: number | null;
  deal_id?: number | null;
  color: string;
  is_all_day: boolean;
  reminder_minutes: number;
  created_at: string;
  updated_at: string;
}

export interface DashboardStats {
  total_contacts: number;
  total_deals: number;
  total_revenue: number;
  pipeline_value: number;
  conversion_rate: number;
  avg_deal_size: number;
  deals_won: number;
  deals_lost: number;
  active_deals: number;
  ai_tasks_today: number;
  ai_cost_today: number;
  revenue_trend: Array<{ month: string; revenue: number }>;
  pipeline_by_stage: Array<{ stage: string; count: number; value: number }>;
  top_deals: Array<{
    id: number;
    title: string;
    value: number;
    company: string;
    stage: string;
    probability: number;
    ai_win_probability?: number | null;
  }>;
  recent_activities: Array<{
    id: number;
    type: string;
    subject: string;
    contact?: string | null;
    created_at: string;
  }>;
  lead_sources: Array<{ source: string; count: number }>;
}

export interface RevenueSnapshot {
  date: string;
  total_revenue: number;
  pipeline_value: number;
  deals_won: number;
  deals_lost: number;
  conversion_rate: number;
  avg_deal_size: number;
  new_contacts: number;
  ai_tasks_run: number;
  ai_total_cost: number;
}

export interface PerformanceMetrics {
  team_performance: Array<{
    owner: string;
    deal_count: number;
    total_value: number;
    avg_value: number;
  }>;
  overall: {
    total_pipeline: number;
    total_revenue: number;
    avg_sales_cycle: number;
  };
}

export interface AppSettings {
  company: {
    name: string;
    timezone: string;
    currency: string;
    fiscal_year_start: string;
  };
  ai_config: {
    auto_lead_scoring: boolean;
    auto_email_drafts: boolean;
    churn_prediction_enabled: boolean;
    forecast_model: string;
    max_daily_budget: number;
    confidence_threshold: number;
    model_provider: string;
    cost_optimization: boolean;
  };
  notifications: {
    email_alerts: boolean;
    deal_stage_changes: boolean;
    ai_task_completion: boolean;
    daily_digest: boolean;
  };
  pipeline_stages: Array<{
    key: string;
    label: string;
    probability: number;
  }>;
}
