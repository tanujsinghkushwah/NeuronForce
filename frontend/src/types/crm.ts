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
  ai_model?: string;
  real_ai_enabled?: boolean;
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

export interface User {
  id: number;
  email: string;
  full_name: string;
  avatar_url?: string | null;
  role: 'admin' | 'revops_lead' | 'sales_rep' | 'viewer' | string;
  is_active: boolean;
  is_verified: boolean;
  last_login_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface GoogleAuthPayload {
  credential?: string;
  email?: string;
  full_name?: string;
  avatar_url?: string;
  sub?: string;
  role?: string;
}

export interface UserSession {
  id: number;
  user_id: number;
  session_token: string;
  ip_address?: string | null;
  user_agent?: string | null;
  expires_at: string;
  is_revoked: boolean;
  created_at: string;
  last_active_at: string;
}

// ─── Service Cloud (Support Tickets & Cases) ──────────────────────────────────

export type TicketStatus = 'open' | 'in_progress' | 'pending_customer' | 'resolved' | 'closed';
export type TicketPriority = 'low' | 'medium' | 'high' | 'critical';
export type TicketCategory = 'bug' | 'billing' | 'feature_request' | 'technical' | 'general' | 'onboarding';

export interface TicketMessage {
  id: number;
  author_name: string;
  author_email?: string | null;
  body: string;
  is_internal: boolean;
  is_ai_generated: boolean;
  created_at: string;
}

export interface Ticket {
  id: number;
  ticket_number: string;
  title: string;
  description?: string | null;
  status: TicketStatus;
  priority: TicketPriority;
  category: TicketCategory;
  assigned_to?: string | null;
  reporter_name?: string | null;
  reporter_email?: string | null;
  contact_id?: number | null;
  deal_id?: number | null;
  sla_due_at?: string | null;
  sla_breached?: boolean;
  first_response_at?: string | null;
  resolved_at?: string | null;
  ai_triage: {
    urgency_score?: number;
    sentiment?: string;
    category?: string;
    priority?: string;
    suggested_response?: string;
    resolution_steps?: string[];
    escalate?: boolean;
    estimated_resolution_hours?: number;
    is_real_ai?: boolean;
  };
  sentiment?: string | null;
  ai_suggested_response?: string | null;
  tags: string[];
  internal_notes?: string | null;
  messages: TicketMessage[];
  created_at: string;
  updated_at: string;
}

export interface TicketStats {
  total: number;
  open: number;
  in_progress: number;
  resolved: number;
  critical: number;
  sla_breached: number;
  resolution_rate: number;
  by_category: Array<{ category: string; count: number }>;
  by_priority: Array<{ priority: string; count: number }>;
}

// ─── Marketing Cloud (Campaigns & Email Marketing) ───────────────────────────

export type CampaignStatus = 'draft' | 'scheduled' | 'active' | 'paused' | 'completed' | 'cancelled';
export type CampaignType = 'email' | 'sms' | 'nurture_sequence' | 'announcement' | 'promotional';

export interface Campaign {
  id: number;
  name: string;
  type: CampaignType;
  status: CampaignStatus;
  description?: string | null;
  subject?: string | null;
  preview_text?: string | null;
  body_html?: string | null;
  body_text?: string | null;
  from_name: string;
  from_email: string;
  audience_filter: Record<string, any>;
  recipient_count: number;
  scheduled_at?: string | null;
  sent_at?: string | null;
  completed_at?: string | null;
  emails_sent: number;
  emails_delivered: number;
  emails_opened: number;
  emails_clicked: number;
  emails_bounced: number;
  emails_unsubscribed: number;
  open_rate: number;
  click_rate: number;
  conversion_rate: number;
  revenue_attributed: number;
  ai_score?: number | null;
  ai_insights: {
    strengths?: string[];
    improvements?: string[];
    optimal_send_time?: string;
    predicted_open_rate?: number;
    predicted_click_rate?: number;
    ab_test_suggestion?: string;
    recommendation?: string;
    is_real_ai?: boolean;
  };
  ab_test_enabled: boolean;
  ab_variant_subject?: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface CampaignStats {
  total: number;
  active: number;
  completed: number;
  draft: number;
  total_emails_sent: number;
  total_revenue_attributed: number;
  avg_open_rate: number;
  avg_click_rate: number;
}

export interface CampaignTemplate {
  id: string;
  name: string;
  type: CampaignType;
  subject: string;
  preview_text: string;
  body_html: string;
  body_text: string;
  suggested_audience: Record<string, any>;
}

// ─── BI Reports, Funnel & Forecast ──────────────────────────────────────────

export interface FunnelStage {
  stage: string;
  count: number;
  rate: number;
}

export interface ConversionFunnel {
  funnel: FunnelStage[];
  total_revenue: number;
  overall_conversion: number;
}

export interface RevenueForecast {
  total_pipeline: number;
  weighted_forecast: number;
  ai_weighted_forecast: number;
  deals_in_pipeline: number;
  avg_probability: number;
  by_stage: Array<{
    stage: string;
    count: number;
    value: number;
    weighted_value: number;
  }>;
}

// ─── Autonomous Multi-Agent LangGraph Studio Types ─────────────────────────

export interface GraphNodeStep {
  node: string;
  status: 'idle' | 'running' | 'completed' | 'skipped' | 'failed';
  label: string;
  latency_ms: number;
  summary: string;
  data?: Record<string, any> | null;
}

export interface AIAgentChatResponse {
  reply: string;
  intent?: string | null;
  target_subagent?: string | null;
  action_type?: string | null;
  subagent_result?: Record<string, any> | null;
  tool_result?: Record<string, any> | null;
  graph_steps: GraphNodeStep[];
  telemetry: {
    model?: string;
    total_latency_ms?: number;
    confidence?: number;
    cost?: number;
  };
  confidence_score: number;
}

export interface AgentChatMessage {
  id: string;
  sender: 'user' | 'agent';
  text: string;
  timestamp: string;
  response?: AIAgentChatResponse;
  isStreaming?: boolean;
}

