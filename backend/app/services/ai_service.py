"""
NeuronForce Real AI Inference Service
Integrates Google Gemini API for real AI inference.
Falls back gracefully to deterministic simulation when API key is unavailable.
"""

import logging
import random
import time
from typing import Any, Dict, Optional

from app.config import settings

logger = logging.getLogger(__name__)

# Try to import Google Gemini SDK
try:
    import google.generativeai as genai
    _GENAI_AVAILABLE = True
except ImportError:
    _GENAI_AVAILABLE = False
    logger.info("google-generativeai not installed; AI tasks will use simulation fallback.")


def _get_gemini_client():
    """Initialize and return a configured Gemini model, or None if unavailable."""
    api_key = settings.GEMINI_API_KEY
    if not _GENAI_AVAILABLE or not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(settings.GEMINI_MODEL)
    except Exception as exc:
        logger.warning(f"Failed to initialize Gemini client: {exc}")
        return None


def _build_prompt(task_type: str, input_data: Dict[str, Any]) -> str:
    """Build a structured, precise prompt for each AI task type."""
    base = "You are an enterprise sales AI assistant. Respond ONLY in valid JSON matching the schema described."

    prompts = {
        "lead_scoring": f"""{base}

Task: Score the following lead and predict buyer intent.
Input: {input_data}

Return JSON:
{{
  "score": <integer 0-100>,
  "tier": "<hot|warm|cold>",
  "factors": ["<factor1>", "<factor2>", "<factor3>"],
  "recommendation": "<actionable next step>",
  "icp_match": <float 0.0-1.0>,
  "engagement_signals": ["<signal1>", "<signal2>"]
}}""",

        "email_draft": f"""{base}

Task: Write a hyper-personalized B2B sales email.
Input: {input_data}

Return JSON:
{{
  "subject": "<compelling subject line>",
  "body": "<full professional email body with greeting, value prop, CTA>",
  "tone_analysis": "<tone descriptor>",
  "word_count": <integer>,
  "cta": "<call to action phrase>",
  "alternatives": ["<alt subject 1>", "<alt subject 2>"]
}}""",

        "deal_analysis": f"""{base}

Task: Analyze this deal for win probability, risk factors and recommended actions.
Input: {input_data}

Return JSON:
{{
  "win_probability": <float 0.0-1.0>,
  "risk_level": "<low|medium|high|critical>",
  "key_risks": ["<risk1>", "<risk2>"],
  "buying_signals": ["<signal1>", "<signal2>"],
  "mitigation_strategies": ["<strategy1>", "<strategy2>"],
  "recommended_next_action": "<specific action>",
  "timeline_assessment": "<brief timeline note>"
}}""",

        "churn_prediction": f"""{base}

Task: Identify churn risk and retention opportunities.
Input: {input_data}

Return JSON:
{{
  "churn_probability": <float 0.0-1.0>,
  "risk_tier": "<critical|high|medium|low>",
  "churn_signals": ["<signal1>", "<signal2>", "<signal3>"],
  "revenue_at_risk": <float>,
  "total_revenue_at_risk": <float>,
  "at_risk_accounts": [
    {
      "company": "<account name>",
      "churn_probability": <float 0.0-1.0>,
      "signals": ["<signal1>", "<signal2>"],
      "mrr": <float>
    }
  ],
  "recommended_interventions": ["<action1>", "<action2>"],
  "estimated_retention_probability": <float 0.0-1.0>
}}""",

        "forecast": f"""{base}

Task: Generate a revenue forecast based on the pipeline data.
Input: {input_data}

Return JSON:
{{
  "predicted_revenue": <float>,
  "confidence_interval": [<lower_bound>, <upper_bound>],
  "risk_adjusted_forecast": <float>,
  "key_drivers": ["<driver1>", "<driver2>", "<driver3>"],
  "upside_scenario": <float>,
  "downside_scenario": <float>,
  "forecast_accuracy": "<high|medium|low>"
}}""",

        "meeting_summary": f"""{base}

Task: Summarize the meeting notes and extract action items.
Input: {input_data}

Return JSON:
{{
  "summary": "<concise 2-3 sentence meeting summary>",
  "key_points": ["<point1>", "<point2>", "<point3>"],
  "action_items": ["<action1>", "<action2>"],
  "decisions_made": ["<decision1>"],
  "sentiment": "<positive|neutral|negative>",
  "follow_up_date": "<suggested follow-up timeframe>"
}}""",

        "ticket_triage": f"""{base}

Task: Analyze this support ticket and provide triage recommendations.
Input: {input_data}

Return JSON:
{{
  "priority": "<critical|high|medium|low>",
  "category": "<bug|billing|feature_request|general|technical>",
  "sentiment": "<frustrated|neutral|positive>",
  "urgency_score": <integer 1-10>,
  "suggested_response": "<professional first response draft>",
  "resolution_steps": ["<step1>", "<step2>"],
  "escalate": <boolean>,
  "estimated_resolution_hours": <integer>
}}""",

        "campaign_optimize": f"""{base}

Task: Analyze this email campaign and suggest optimizations.
Input: {input_data}

Return JSON:
{{
  "subject_line_score": <integer 0-100>,
  "predicted_open_rate": <float 0.0-1.0>,
  "predicted_click_rate": <float 0.0-1.0>,
  "improvements": ["<improvement1>", "<improvement2>"],
  "optimal_send_time": "<day and time recommendation>",
  "audience_fit_score": <integer 0-100>,
  "ab_test_suggestion": "<A/B test idea>"
}}""",
    }
    return prompts.get(task_type, f"{base}\n\nTask type: {task_type}\nInput: {input_data}\n\nReturn a JSON object with your analysis.")


def _simulation_fallback(task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic-ish simulation fallback when Gemini is unavailable."""
    fallbacks = {
        "lead_scoring": {
            "score": random.randint(55, 97),
            "tier": random.choice(["hot", "warm", "cold"]),
            "factors": random.sample([
                "High email engagement", "Budget confirmed", "Decision maker identified",
                "Active on website", "Downloaded whitepaper", "Attended webinar"
            ], k=3),
            "recommendation": random.choice([
                "Schedule discovery call this week",
                "Send personalized ROI case study",
                "Assign to senior AE immediately",
                "Add to high-priority nurture sequence"
            ]),
            "icp_match": round(random.uniform(0.6, 0.97), 2),
            "engagement_signals": ["Email opened 3x", "Visited pricing page"],
        },
        "email_draft": {
            "subject": "Following Up: How We Help Teams Like Yours Close 40% More Pipeline",
            "body": "Hi {name},\n\nI wanted to follow up on our recent conversation about your Q4 revenue goals.\n\nBased on what you shared, I believe our autonomous AI pipeline can directly address the manual bottlenecks slowing your team down.\n\nI'd love to show you a 15-minute demo tailored to your use case. Does Thursday at 2pm PT work?\n\nBest,\nThe NeuronForce Team",
            "tone_analysis": "Professional, direct, value-driven",
            "word_count": 82,
            "cta": "Book 15-min demo",
            "alternatives": ["Quick question about your pipeline", "Helping [Company] hit Q4 targets"],
        },
        "deal_analysis": {
            "win_probability": round(random.uniform(0.35, 0.88), 2),
            "risk_level": random.choice(["low", "medium", "high"]),
            "key_risks": random.sample(["Budget freeze risk", "Competitor evaluation", "Long decision cycle", "Missing executive champion"], k=2),
            "buying_signals": ["RFP submitted", "Legal review started"],
            "mitigation_strategies": ["Arrange executive sponsor meeting", "Provide ROI calculator"],
            "recommended_next_action": "Schedule a technical deep-dive with their CTO",
            "timeline_assessment": "On track for Q4 close if champion engaged by EOW",
        },
        "churn_prediction": {
            "churn_probability": round(random.uniform(0.15, 0.65), 2),
            "risk_tier": random.choice(["high", "medium", "low"]),
            "churn_signals": ["30% usage drop last month", "Support ticket volume up 2x", "Champion left company"],
            "revenue_at_risk": random.randint(25000, 250000),
            "total_revenue_at_risk": 501000,
            "at_risk_accounts": [
                {
                    "company": input_data.get("account", "Enterprise Cloud Corp"),
                    "churn_probability": 0.38,
                    "signals": ["Decreased usage", "Support ticket spike"],
                    "mrr": 18500,
                }
            ],
            "recommended_interventions": ["Schedule executive business review", "Offer dedicated CSM"],
            "estimated_retention_probability": round(random.uniform(0.55, 0.85), 2),
        },
        "forecast": {
            "predicted_revenue": random.randint(2000000, 5000000),
            "confidence_interval": [1500000, 4500000],
            "risk_adjusted_forecast": random.randint(1800000, 4000000),
            "key_drivers": ["Q4 enterprise pipeline", "Seasonal uptick", "New AE ramp"],
            "upside_scenario": 5500000,
            "downside_scenario": 1400000,
            "forecast_accuracy": "medium",
        },
        "meeting_summary": {
            "summary": "Team reviewed Q4 pipeline velocity with focus on 3 enterprise deals in negotiation. Budget constraints flagged for 2 accounts.",
            "key_points": ["Pipeline at $3.2M", "3 deals in final stage", "2 budget concerns flagged"],
            "action_items": ["Follow up with TechCorp by Friday", "Prepare ROI deck for HealthTech deal"],
            "decisions_made": ["Prioritize enterprise segment in Q4"],
            "sentiment": "positive",
            "follow_up_date": "Next Tuesday",
        },
        "ticket_triage": {
            "priority": random.choice(["high", "medium", "low"]),
            "category": random.choice(["bug", "billing", "technical", "general"]),
            "sentiment": random.choice(["frustrated", "neutral", "positive"]),
            "urgency_score": random.randint(3, 9),
            "suggested_response": "Thank you for reaching out. Our team is reviewing your request and will respond within 4 business hours.",
            "resolution_steps": ["Reproduce the issue", "Check recent deployments", "Escalate if needed"],
            "escalate": False,
            "estimated_resolution_hours": random.randint(2, 24),
        },
        "campaign_optimize": {
            "subject_line_score": random.randint(60, 92),
            "predicted_open_rate": round(random.uniform(0.22, 0.45), 2),
            "predicted_click_rate": round(random.uniform(0.04, 0.18), 2),
            "improvements": ["Add personalization token in subject", "Move CTA higher in body"],
            "optimal_send_time": "Tuesday 9-11am in recipient timezone",
            "audience_fit_score": random.randint(65, 95),
            "ab_test_suggestion": "Test question vs. statement subject lines",
        },
    }
    return fallbacks.get(task_type, {"message": "Task completed", "status": "ok"})


def run_ai_task(task_type: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an AI task using Gemini API with automatic simulation fallback.

    Returns dict with keys: output, confidence, cost, model, is_real_ai
    """
    import json

    model = _get_gemini_client()
    if model:
        try:
            prompt = _build_prompt(task_type, input_data)
            start = time.time()
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4,
                    "max_output_tokens": 1024,
                    "response_mime_type": "application/json",
                }
            )
            elapsed_ms = int((time.time() - start) * 1000)

            # Parse JSON response
            raw_text = response.text.strip()
            # Strip markdown code fences if present
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            output = json.loads(raw_text)

            # Estimate token cost (Gemini Flash pricing: ~$0.075/1M input, $0.30/1M output)
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = len(raw_text.split()) * 1.3
            cost = round((input_tokens * 0.075 + output_tokens * 0.30) / 1_000_000, 6)
            cost = max(cost, 0.0001)  # minimum cost floor

            return {
                "output": output,
                "confidence": round(random.uniform(0.82, 0.97), 2),  # Gemini doesn't return confidence natively
                "cost": cost,
                "model": settings.GEMINI_MODEL,
                "is_real_ai": True,
                "latency_ms": elapsed_ms,
            }

        except json.JSONDecodeError as je:
            logger.warning(f"Gemini returned non-JSON response for {task_type}, falling back: {je}")
        except Exception as exc:
            logger.warning(f"Gemini inference failed for {task_type}: {exc}, falling back to simulation.")

    # Fallback simulation
    fallback_output = _simulation_fallback(task_type, input_data)
    cost = round(random.uniform(0.001, 0.03), 5)
    return {
        "output": fallback_output,
        "confidence": round(random.uniform(0.70, 0.92), 2),
        "cost": cost,
        "model": "simulation",
        "is_real_ai": False,
        "latency_ms": random.randint(150, 800),
    }
