"""
Personalized Email Drafter Sub-Agent
Generates tailored, high-converting B2B outreach and objection-handling emails.
"""

from typing import Dict, Any
from agents.subagents.llm_client import call_llm_json


def run_email_drafter(prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute Personalized Email Drafting reasoning.
    """
    system_prompt = (
        "You are an executive-level B2B Sales Copywriter and Strategist. Draft a hyper-personalized, "
        "concise sales outreach email addressing known business goals and objections. Return a JSON object with this structure:\n"
        "{\n"
        '  "recipient": "<recipient name and role>",\n'
        '  "subject": "<compelling, non-spammy subject line>",\n'
        '  "body": "<complete professional email text formatted with paragraphs and signature placeholder>",\n'
        '  "key_value_prop": "<one sentence value proposition tailored to prospect>",\n'
        '  "call_to_action": "<clear, low-friction CTA>",\n'
        '  "tone": "<executive|collaborative|urgent>",\n'
        '  "alternative_subjects": ["<alt subject 1>", "<alt subject 2>"]\n'
        "}"
    )

    user_prompt = f"Prompt: {prompt}\nCRM Database Context: {context}"
    result = call_llm_json(system_prompt, user_prompt)

    if result and "data" in result:
        output = result["data"]
        output["_meta"] = {"model": result["model"], "latency_ms": result["latency_ms"]}
        return output

    contact = (context.get("matching_contacts") or [{}])[0]
    recipient_name = contact.get("name") or "Sarah Chen"
    company = contact.get("company") or "Stark Industries"

    return {
        "recipient": f"{recipient_name} ({company})",
        "subject": f"Autonomous pipeline acceleration for {company}",
        "body": (
            f"Hi {recipient_name.split()[0]},\n\n"
            f"Given {company}'s focus on enterprise revenue scaling this quarter, I wanted to share how our "
            f"autonomous AI agent fleet eliminates manual CRM overhead while forecasting pipeline risk with 92% confidence.\n\n"
            f"Would you be open to a brief 15-minute walkthrough this Thursday or Friday to benchmark how our agents "
            f"can accelerate deal cycle times?\n\n"
            f"Best regards,\nNeuronForce Sales Team"
        ),
        "key_value_prop": "Autonomous multi-agent execution that eliminates manual data entry and cuts deal cycles by 35%.",
        "call_to_action": "15-minute architecture briefing this Thursday",
        "tone": "executive",
        "alternative_subjects": [
            f"Quick question regarding {company}'s Q4 RevOps tech stack",
            f"Cutting enterprise sales cycle friction at {company}"
        ],
        "_meta": {"model": "simulation-fallback", "latency_ms": 140}
    }
