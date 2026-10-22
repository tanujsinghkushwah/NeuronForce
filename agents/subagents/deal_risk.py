"""
Deal Risk & Probability Sub-Agent
Detects deal stall indicators, competitor undercutting, missing champions, and forecasts win probability.
"""

from typing import Dict, Any, Optional
from agents.subagents.llm_client import call_llm_json


def run_deal_risk_analysis(
    prompt: str,
    context: Dict[str, Any],
    target_deal: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Execute Deal Risk & Win Probability reasoning on a specific deal or the most active deal in context.
    """
    deal = target_deal or context.get("target_deal")
    if not deal:
        matching = context.get("matching_deals") or []
        if matching:
            deal = matching[0]

    system_prompt = (
        "You are an enterprise Revenue Intelligence and Deal Strategy AI. Analyze deal dynamics, stage age, "
        "and stakeholder engagement to identify risk factors and predict win probability for the targeted deal. "
        "Return a JSON object with this exact structure:\n"
        "{\n"
        '  "deal_title": "<exact deal name>",\n'
        '  "company": "<account name or stakeholders>",\n'
        '  "win_probability": <float 0.0-1.0>,\n'
        '  "risk_tier": "<low|medium|high|critical>",\n'
        '  "key_risk_factors": ["<risk 1>", "<risk 2>", "<risk 3>"],\n'
        '  "buying_signals": ["<positive signal 1>", "<positive signal 2>"],\n'
        '  "mitigation_actions": ["<mitigation 1>", "<mitigation 2>"],\n'
        '  "decision_timeline": "<e.g. Closing within 21 days>"\n'
        "}"
    )

    deal_context_str = f"Specific Deal to Evaluate:\n{deal}\n\n" if deal else ""
    user_prompt = f"Prompt: {prompt}\n\n{deal_context_str}CRM Context: {context}"
    result = call_llm_json(system_prompt, user_prompt)

    if result and "data" in result and isinstance(result["data"], dict):
        output = result["data"]
        # Ensure deal_title is preserved from targeted deal if output missed it
        if deal and (
            not output.get("deal_title")
            or output.get("deal_title") == "Global Enterprise AI Automation"
        ):
            output["deal_title"] = deal.get("title", output.get("deal_title"))
        output["_meta"] = {"model": result["model"], "latency_ms": result["latency_ms"]}
        return output

    # Fallback simulation
    deal_title = (
        deal.get("title") if deal else None
    ) or "Global Enterprise AI Automation"
    company = (deal.get("company") if deal else None) or "HyperScale Corp"
    raw_stage = deal.get("stage") if deal else "prospecting"
    stage = str(raw_stage).lower() if raw_stage else "prospecting"
    value = float(deal.get("value", 1000000)) if deal else 1000000.0

    is_early_stage = stage in ("prospecting", "qualification", "discovery")
    win_prob = 0.55 if is_early_stage else 0.78
    risk_tier = "high" if (value >= 1000000 and is_early_stage) else "medium"

    return {
        "deal_title": deal_title,
        "company": company,
        "win_probability": win_prob,
        "risk_tier": risk_tier,
        "key_risk_factors": [
            f"Early stage ({stage.title()}) for high-value (${value:,.0f}) transaction",
            "Executive procurement envelope and ROI business case pending validation",
            "Multi-threaded champion alignment required across technical and financial buyers",
        ],
        "buying_signals": [
            "Strong initial interest expressed by key decision-makers",
            "Urgent timeline to modernize sales operations with autonomous AI",
        ],
        "mitigation_actions": [
            "Schedule tailored technical deep-dive and executive business case review",
            "Map all procurement and security evaluation criteria to avoid late-stage roadblocks",
        ],
        "decision_timeline": "Target close within 45–60 days",
        "_meta": {"model": "simulation-fallback", "latency_ms": 130},
    }
