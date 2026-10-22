"""
LLM Client for NeuronForce Autonomous Agents
Invokes OpenRouter with google/gemini-2.5-flash-lite (or configured model).
"""

import os
import sys
import json
import time
import logging
from typing import Dict, Any, Optional
import httpx

CURRENT_DIR = Path = __import__("pathlib").Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = CURRENT_DIR / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.config import settings
except Exception:

    class MockSettings:
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
        OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")
        OPENROUTER_BASE_URL = os.getenv(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        )
        FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

    settings = MockSettings()

logger = logging.getLogger(__name__)


def call_llm_json(
    system_prompt: str, user_prompt: str, temperature: float = 0.2
) -> Optional[Dict[str, Any]]:
    """
    Call OpenRouter API expecting a JSON object output.
    """
    api_key = getattr(settings, "OPENROUTER_API_KEY", "") or os.getenv(
        "OPENROUTER_API_KEY", ""
    )
    if not api_key:
        logger.warning("No OPENROUTER_API_KEY set.")
        return None

    model = getattr(settings, "OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")
    base_url = getattr(
        settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
    ).rstrip("/")
    url = f"{base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": getattr(settings, "FRONTEND_URL", "http://localhost:3000"),
        "X-Title": "NeuronForce CRM Multi-Agent Studio",
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
                + "\nIMPORTANT: Return ONLY valid parseable JSON. Do not add markdown fences or preamble.",
            },
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    try:
        start_time = time.time()
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload, headers=headers)
        elapsed_ms = int((time.time() - start_time) * 1000)

        if resp.status_code != 200:
            logger.warning(
                f"OpenRouter returned status {resp.status_code}: {resp.text}"
            )
            return None

        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return None

        raw = choices[0].get("message", {}).get("content", "").strip()
        # Clean markdown code blocks if model included them
        if "```" in raw:
            parts = raw.split("```")
            raw = parts[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        parsed = json.loads(raw)
        return {
            "data": parsed,
            "latency_ms": elapsed_ms,
            "model": model,
            "usage": data.get("usage", {}),
        }
    except Exception as exc:
        logger.warning(f"Error calling LLM: {exc}")
        return None


def call_llm_text(
    system_prompt: str, user_prompt: str, temperature: float = 0.3
) -> Optional[str]:
    """
    Call OpenRouter API expecting markdown or conversational text output.
    """
    api_key = getattr(settings, "OPENROUTER_API_KEY", "") or os.getenv(
        "OPENROUTER_API_KEY", ""
    )
    if not api_key:
        logger.warning("No OPENROUTER_API_KEY set.")
        return None

    model = getattr(settings, "OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")
    base_url = getattr(
        settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
    ).rstrip("/")
    url = f"{base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": getattr(settings, "FRONTEND_URL", "http://localhost:3000"),
        "X-Title": "NeuronForce CRM Multi-Agent Studio",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            logger.warning(
                f"OpenRouter returned status {resp.status_code}: {resp.text}"
            )
            return None

        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return None

        return choices[0].get("message", {}).get("content", "").strip()
    except Exception as exc:
        logger.warning(f"Error calling LLM text: {exc}")
        return None
