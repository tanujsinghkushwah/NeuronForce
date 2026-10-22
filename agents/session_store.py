"""
NeuronForce Session Store
Maintains multi-turn conversation history and active working entity context
(active deal, active contact, active meeting, active campaign) across agent chat turns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import threading


class SessionContext:
    def __init__(self, session_id: str):
        self.session_id: str = session_id
        self.messages: List[Dict[str, Any]] = []
        self.active_deal: Optional[Dict[str, Any]] = None
        self.active_contact: Optional[Dict[str, Any]] = None
        self.active_meeting: Optional[Dict[str, Any]] = None
        self.active_campaign: Optional[Dict[str, Any]] = None
        self.recent_entities: Dict[str, Any] = {}
        self.created_at: datetime = datetime.now(timezone.utc)
        self.updated_at: datetime = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "messages": self.messages,
            "active_deal": self.active_deal,
            "active_contact": self.active_contact,
            "active_meeting": self.active_meeting,
            "active_campaign": self.active_campaign,
            "recent_entities": self.recent_entities,
            "updated_at": self.updated_at.isoformat(),
        }


# Thread-safe in-memory session registry
_SESSIONS: Dict[str, SessionContext] = {}
_LOCK = threading.Lock()


def get_or_create_session(session_id: Optional[str] = None) -> SessionContext:
    """Retrieve existing session or initialize a fresh SessionContext."""
    sid = (session_id or "default_session").strip()
    with _LOCK:
        if sid not in _SESSIONS:
            _SESSIONS[sid] = SessionContext(session_id=sid)
        return _SESSIONS[sid]


def update_session(
    session_id: str,
    user_prompt: str,
    assistant_reply: str,
    tool_results: Optional[List[Dict[str, Any]]] = None,
    subagent_results: Optional[List[Dict[str, Any]]] = None,
    extracted_entities: Optional[Dict[str, Any]] = None,
) -> SessionContext:
    """
    Record a completed turn: appends messages (keeping sliding window)
    and extracts active entities from tool and subagent results.
    """
    session = get_or_create_session(session_id)
    with _LOCK:
        # 1. Append user and assistant messages
        timestamp = datetime.now(timezone.utc).strftime("%I:%M %p")
        session.messages.append(
            {
                "role": "user",
                "content": user_prompt,
                "timestamp": timestamp,
            }
        )
        session.messages.append(
            {
                "role": "assistant",
                "content": assistant_reply,
                "timestamp": timestamp,
            }
        )

        # Keep sliding window of last 10 messages (5 turns) to maintain tight token budget
        if len(session.messages) > 10:
            session.messages = session.messages[-10:]

        # 2. Extract and update active entities from tool results
        for tr in tool_results or []:
            if not isinstance(tr, dict) or not tr.get("success"):
                continue
            act = tr.get("action")
            if act == "create_deal" or act == "update_deal":
                deal = tr.get("deal")
                if deal:
                    session.active_deal = deal
            elif act == "create_contact" or act == "update_contact":
                contact = tr.get("contact")
                if contact:
                    session.active_contact = contact
            elif act == "schedule_meeting":
                event = tr.get("event")
                if event:
                    session.active_meeting = event
            elif act == "create_campaign":
                camp = tr.get("campaign")
                if camp:
                    session.active_campaign = camp

        # 3. Extract from subagent results if relevant
        for sr in subagent_results or []:
            if not isinstance(sr, dict):
                continue
            if "deal_title" in sr:
                if not session.active_deal:
                    session.active_deal = {}
                session.active_deal["title"] = sr.get("deal_title")
                session.active_deal["company"] = sr.get("company")
            if "lead_name" in sr:
                if not session.active_contact:
                    session.active_contact = {}
                session.active_contact["name"] = sr.get("lead_name")

        # 4. Merge extracted entities into recent entity map
        if extracted_entities:
            for k, v in extracted_entities.items():
                if v:
                    session.recent_entities[k] = v

        session.updated_at = datetime.now(timezone.utc)
        return session


def clear_session(session_id: str) -> None:
    """Clear session history and active entities (invoked on Reset button)."""
    sid = (session_id or "default_session").strip()
    with _LOCK:
        if sid in _SESSIONS:
            del _SESSIONS[sid]


def format_session_context_for_prompt(session_id: str) -> str:
    """
    Format conversation history and active working entities as a clean markdown block
    to inject into the LLM system prompt.
    """
    session = get_or_create_session(session_id)
    with _LOCK:
        sections: List[str] = []

        # 1. Active Working Entities
        entity_lines: List[str] = []
        if session.active_deal:
            d = session.active_deal
            val_str = (
                f"${float(d.get('value', 0)):,.2f}"
                if d.get("value")
                else "Unspecified Value"
            )
            stg = d.get("stage", "Prospecting")
            co = d.get("company", "")
            co_suffix = f" (Company: {co})" if co else ""
            entity_lines.append(
                f"- **Active Deal**: '{d.get('title')}' — {val_str} [Stage: {stg}]{co_suffix} (ID: {d.get('id')})"
            )

        if session.active_contact:
            c = session.active_contact
            em = c.get("email", "")
            em_suffix = f" <{em}>" if em else ""
            co = c.get("company", "")
            co_suffix = f" at {co}" if co else ""
            entity_lines.append(
                f"- **Active Contact**: {c.get('name')}{em_suffix}{co_suffix} (ID: {c.get('id')})"
            )

        if session.active_meeting:
            m = session.active_meeting
            entity_lines.append(
                f"- **Active Meeting**: '{m.get('title')}' at {m.get('start_time')} (Attendees: {m.get('attendees')})"
            )

        if session.active_campaign:
            cp = session.active_campaign
            entity_lines.append(
                f"- **Active Campaign**: '{cp.get('name')}' (Subject: {cp.get('subject')})"
            )

        if entity_lines:
            sections.append(
                "ACTIVE WORKING CONTEXT (Entities created or referenced in this session):\n"
                + "\n".join(entity_lines)
            )

        # 2. Conversation History
        if session.messages:
            history_lines: List[str] = []
            for msg in session.messages[-6:]:  # last 3 turns
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_lines.append(f"{role}: {msg.get('content')}")
            sections.append(
                "CONVERSATION HISTORY (Previous turns in this session):\n"
                + "\n".join(history_lines)
            )

        if not sections:
            return ""

        return "\n\n" + "\n\n".join(sections) + "\n\n"
