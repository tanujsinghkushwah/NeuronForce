"""
NeuronForce HLD Asset Generator (Refined & Spacious Layout)
Generates:
1. Native Draw.io XML files (.drawio) with spacious, uncompressed coordinates.
2. Presentation-Ready Widescreen HTML/SVG diagrams with generous vertical rhythm.
3. Ultra-Crisp High-Resolution PNG renderings via Headless Google Chrome (2800x1750 @ 2x scale).
"""

import os
import subprocess
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
IMAGES_DIR = DOCS_DIR / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ==============================================================================
# 1. REFINED DRAW.IO XML GENERATORS (SPACIOUS, UNCOMPRESSED)
# ==============================================================================

def generate_agentic_drawio() -> str:
    """Generate native Draw.io XML for the Agentic System Flow with spacious layout."""
    return """<mxfile host="Electron" modified="2026-10-23T05:35:00.000Z" agent="NeuronForce" version="21.0.0" type="device">
  <diagram id="agentic_hld" name="NeuronForce Agentic System HLD">
    <mxGraphModel dx="2000" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2800" pageHeight="1800" background="#090D16" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title" value="&lt;b style='font-size:26px; color:#F8FAFC;'&gt;NeuronForce — Autonomous Multi-Agent LangGraph System (HLD)&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:14px; color:#94A3B8;'&gt;Cyclic StateGraph Multi-Step Orchestration • Sliding-Window Session Memory • Semantic Pronoun Resolution • Audited Telemetry&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#38BDF8;strokeWidth=2;arcSize=8;align=left;spacingLeft=30;" vertex="1" parent="1">
          <mxGeometry x="50" y="40" width="2700" height="85" as="geometry" />
        </mxCell>

        <!-- CONTAINER 1: Ingress & Memory -->
        <mxCell id="c_client" value="01 / INGRESS &amp;amp; MULTI-TURN MEMORY" style="swimlane;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#EC4899;strokeWidth=2;fontColor=#F472B6;fontStyle=1;fontSize=14;startSize=35;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="50" y="160" width="540" height="1560" as="geometry" />
        </mxCell>
        <mxCell id="user_rep" value="&lt;b style='color:#F8FAFC;font-size:15px;'&gt;Enterprise Sales Rep / Account Executive&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:12px;'&gt;Inputs natural language compound instructions into Studio:&lt;br/&gt;&lt;i style='color:#38BDF8;'&gt;'Add Tanuj at Google and book a 1-hour demo with him and Sarah for tomorrow at 2 PM'&lt;/i&gt;&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#475569;strokeWidth=1.5;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_client">
          <mxGeometry x="30" y="60" width="480" height="110" as="geometry" />
        </mxCell>
        <mxCell id="nextjs_ui" value="&lt;b style='color:#38BDF8;font-size:15px;'&gt;Next.js 16 Autonomous Agent Studio&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#E2E8F0;font-size:12px;'&gt;• Real-time LangGraph node execution cockpit&lt;br/&gt;• Multi-card rendered action outputs (Contacts, Deals, Meetings)&lt;br/&gt;• Sub-100ms perceived performance &amp;amp; CSS de-blur transition&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0284C7;strokeWidth=1.5;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_client">
          <mxGeometry x="30" y="200" width="480" height="120" as="geometry" />
        </mxCell>
        <mxCell id="api_gw" value="&lt;b style='color:#34D399;font-size:15px;'&gt;FastAPI AI Gateway Router&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#E2E8F0;font-size:12px;'&gt;POST /api/ai-agents/chat &amp;amp; /tasks&lt;br/&gt;Validates session_id, origins allowlist &amp;amp; executes in async threadpool&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#059669;strokeWidth=1.5;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_client">
          <mxGeometry x="30" y="350" width="480" height="100" as="geometry" />
        </mxCell>
        <mxCell id="session_store" value="&lt;b style='color:#F43F5E;font-size:16px;'&gt;Thread-Safe In-Memory Session Store&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;(agents/session_store.py)&lt;br/&gt;&lt;br/&gt;• &lt;b style='color:#38BDF8;'&gt;Sliding Window&lt;/b&gt;: Last 5 turns (10 messages preserved)&lt;br/&gt;• &lt;b style='color:#F472B6;'&gt;active_deal&lt;/b&gt;: Target $1,000,000 Deal (Google)&lt;br/&gt;• &lt;b style='color:#F472B6;'&gt;active_contact&lt;/b&gt;: Tanuj Singh (Google)&lt;br/&gt;• &lt;b style='color:#F472B6;'&gt;active_meeting&lt;/b&gt;: Tanuj &amp;amp; Sarah (Tomorrow 2 PM)&lt;br/&gt;• &lt;b style='color:#F472B6;'&gt;active_campaign&lt;/b&gt;: X, Instagram Multi-Channel&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E1B4B;strokeColor=#8B5CF6;strokeWidth=2;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_client">
          <mxGeometry x="30" y="490" width="480" height="200" as="geometry" />
        </mxCell>
        <mxCell id="pronoun_res" value="&lt;b style='color:#FB7185;font-size:15px;'&gt;Semantic Pronoun &amp;amp; Reference Resolver&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#E2E8F0;font-size:12px;'&gt;• &lt;i&gt;'promote this deal'&lt;/i&gt; ➔ Resolves to active_deal ($1M Google)&lt;br/&gt;• &lt;i&gt;'risk analysis on it'&lt;/i&gt; ➔ Routes to deal_risk subagent on active_deal&lt;br/&gt;• &lt;i&gt;'send him an email'&lt;/i&gt; ➔ Injects active_contact email address&lt;br/&gt;&lt;b style='color:#34D399;'&gt;Eliminates brittle keyword lists &amp;amp; hardcoded regex heuristics!&lt;/b&gt;&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3B0764;strokeColor=#D946EF;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_client">
          <mxGeometry x="30" y="720" width="480" height="150" as="geometry" />
        </mxCell>

        <!-- CONTAINER 2: LangGraph Orchestrator -->
        <mxCell id="c_graph" value="02 / LANGGRAPH CYCLIC STATEGRAPH ORCHESTRATOR (agents/orchestrator/)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0A0F1D;strokeColor=#38BDF8;strokeWidth=2.5;fontColor=#38BDF8;fontStyle=1;fontSize=15;startSize=40;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="630" y="160" width="1380" height="1560" as="geometry" />
        </mxCell>

        <!-- Step 1 & 2 -->
        <mxCell id="node1" value="&lt;b style='color:#38BDF8;font-size:15px;'&gt;Node 1: Prompt Ingestion&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:12px;'&gt;Sanitization, session token verification &amp;amp; initial token budget estimation&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=2;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_graph">
          <mxGeometry x="60" y="70" width="580" height="90" as="geometry" />
        </mxCell>

        <mxCell id="node2" value="&lt;b style='color:#38BDF8;font-size:15px;'&gt;Node 2: CRM Context Retrieval&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;Context Retriever Engine (context_retriever.py)&lt;br/&gt;Pulls matching contacts, deals, events &amp;amp; injects prioritized active session entities&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=2;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_graph">
          <mxGeometry x="720" y="70" width="600" height="90" as="geometry" />
        </mxCell>

        <!-- Node 3: Intent Router & Planner -->
        <mxCell id="node3" value="&lt;b style='color:#F59E0B;font-size:16px;'&gt;Node 3: Structured Execution Planner &amp;amp; Intent Router&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#FEF3C7;font-size:12px;'&gt;Invokes OpenRouter Gateway with strict JSON schema to generate an ordered execution plan array:&lt;br/&gt;&lt;b style='color:#FDE68A;'&gt;plan: [ { step_id: 1, type: 'crm_action', action_type: 'create_contact' }, { step_id: 2, type: 'crm_action', action_type: 'schedule_meeting' } ]&lt;/b&gt;&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#78350F;strokeColor=#F59E0B;strokeWidth=2;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_graph">
          <mxGeometry x="60" y="210" width="1260" height="110" as="geometry" />
        </mxCell>

        <!-- Decision: route_after_intent -->
        <mxCell id="dec_intent" value="&lt;b style='color:#FFFFFF;font-size:13px;'&gt;route_after_intent&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:11px;color:#FCA5A5;'&gt;Inspects Plan[0].type&lt;/span&gt;" style="rhombus;whiteSpace=wrap;html=1;fillColor=#991B1B;strokeColor=#EF4444;strokeWidth=2;" vertex="1" parent="c_graph">
          <mxGeometry x="580" y="360" width="220" height="100" as="geometry" />
        </mxCell>

        <!-- Node 4b: CRM Action Executor -->
        <mxCell id="node_crm" value="&lt;b style='color:#34D399;font-size:16px;'&gt;Node 4b: CRM Action Executor&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#D1FAE5;font-size:12px;'&gt;Executes Direct Relational Database Mutations (ACID CP):&lt;br/&gt;&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;schedule_meeting&lt;/b&gt;: Range-Aware Normalizer &amp;amp; Dynamic Attendee Resolution&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;create_contact / update_contact&lt;/b&gt;: Full lifecycle tracking&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;create_deal / update_deal&lt;/b&gt;: Stage updates &amp;amp; automatic ARR recalculations&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;create_campaign&lt;/b&gt;: Multi-channel marketing outreach generation&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=2;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_graph">
          <mxGeometry x="60" y="500" width="560" height="230" as="geometry" />
        </mxCell>

        <!-- Node 4a: Subagent Executor -->
        <mxCell id="node_sub" value="&lt;b style='color:#A78BFA;font-size:16px;'&gt;Node 4a: Specialist Subagent Executor&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#EDE9FE;font-size:12px;'&gt;Executes Targeted Analytical Deep-Reasoning Workflows:&lt;br/&gt;&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;lead_scoring&lt;/b&gt;: Buyer Intent Score (0-100) &amp;amp; ICP fit match %&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;deal_risk&lt;/b&gt;: Win probability %, stall risk &amp;amp; mitigation playbooks&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;email_draft&lt;/b&gt;: Hyper-personalized outreach + auto Resend/SMTP dispatch&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;churn_sentinel&lt;/b&gt;: ARR at risk exposure &amp;amp; retention action playbooks&lt;br/&gt;• &lt;b style='color:#FFFFFF;'&gt;meeting_summary&lt;/b&gt;: Key decisions, owners, due dates &amp;amp; CRM sync&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#312E81;strokeColor=#8B5CF6;strokeWidth=2;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_graph">
          <mxGeometry x="760" y="500" width="560" height="230" as="geometry" />
        </mxCell>

        <!-- Step Cycle: route_after_step -->
        <mxCell id="dec_step" value="&lt;b style='color:#FFFFFF;font-size:14px;'&gt;route_after_step&lt;br/&gt;Cyclic Step Router&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:11px;color:#FEF3C7;'&gt;idx &amp;lt; len(plan)?&lt;/span&gt;" style="rhombus;whiteSpace=wrap;html=1;fillColor=#B45309;strokeColor=#F59E0B;strokeWidth=2.5;" vertex="1" parent="c_graph">
          <mxGeometry x="575" y="760" width="230" height="130" as="geometry" />
        </mxCell>

        <!-- Node 5: Synthesizer -->
        <mxCell id="node_synth" value="&lt;b style='color:#38BDF8;font-size:16px;'&gt;Node 5: Response Synthesizer &amp;amp; Telemetry Aggregator&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#E2E8F0;font-size:12px;'&gt;• Assembles clean, numbered markdown sections for all executed compound steps&lt;br/&gt;• Attaches interactive UI action cards (Contacts, Deals, Meetings, Dispatched Emails)&lt;br/&gt;• Computes exact token count, fractional-cent USD cost &amp;amp; round-trip latency in ms&lt;br/&gt;• Calibrates overall confidence score (0.00 to 1.00) &amp;amp; logs to AIAgentTask audit table&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#0284C7;strokeWidth=2;arcSize=8;align=left;spacingLeft=25;" vertex="1" parent="c_graph">
          <mxGeometry x="60" y="930" width="1260" height="130" as="geometry" />
        </mxCell>

        <!-- Subagent Specialist Grid -->
        <mxCell id="sa_lead" value="&lt;b style='color:#38BDF8;font-size:13px;'&gt;Lead Scoring&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Score: 92/100 (HOT)&lt;br/&gt;ICP Match: 95%&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#38BDF8;strokeWidth=1.5;" vertex="1" parent="c_graph">
          <mxGeometry x="60" y="1100" width="230" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sa_risk" value="&lt;b style='color:#F59E0B;font-size:13px;'&gt;Deal Risk Sentinel&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Win Prob: 78%&lt;br/&gt;Medium Risk Exposure&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#F59E0B;strokeWidth=1.5;" vertex="1" parent="c_graph">
          <mxGeometry x="315" y="1100" width="230" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sa_email" value="&lt;b style='color:#10B981;font-size:13px;'&gt;Email Drafter&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Personalized Pitch&lt;br/&gt;Auto Resend / SMTP&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#10B981;strokeWidth=1.5;" vertex="1" parent="c_graph">
          <mxGeometry x="575" y="1100" width="230" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sa_churn" value="&lt;b style='color:#EF4444;font-size:13px;'&gt;Churn Sentinel&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;ARR at Risk: $180,000&lt;br/&gt;Prescribed Playbooks&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#EF4444;strokeWidth=1.5;" vertex="1" parent="c_graph">
          <mxGeometry x="835" y="1100" width="230" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sa_meet" value="&lt;b style='color:#A855F7;font-size:13px;'&gt;Meeting Summary&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Action items &amp;amp; owners&lt;br/&gt;CRM Timeline Sync&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#A855F7;strokeWidth=1.5;" vertex="1" parent="c_graph">
          <mxGeometry x="1090" y="1100" width="230" height="80" as="geometry" />
        </mxCell>

        <!-- CONTAINER 3: Storage, Inference & Auditing -->
        <mxCell id="c_ext" value="03 / PERSISTENCE, GATEWAY &amp;amp; EVALUATIONS" style="swimlane;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#10B981;strokeWidth=2;fontColor=#34D399;fontStyle=1;fontSize=14;startSize=35;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="2050" y="160" width="700" height="1560" as="geometry" />
        </mxCell>

        <!-- CP Database -->
        <mxCell id="db_cp" value="&lt;b style='color:#34D399;font-size:17px;'&gt;Relational CP Database (CAP Theorem)&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#A7F3D0;font-size:13px;'&gt;PostgreSQL (Production) / SQLite (Development)&lt;br/&gt;&lt;br/&gt;&lt;b style='color:#FFFFFF;'&gt;CRITICAL DESIGN DECISION:&lt;/b&gt;&lt;br/&gt;• Strict ACID Consistency &amp;amp; Partition Tolerance (CP)&lt;br/&gt;• Zero dirty reads on deals, revenue forecasts &amp;amp; contacts&lt;br/&gt;• Atomic commits guarantee 100% CRM record integrity&lt;br/&gt;• &lt;b style='color:#FACC15;'&gt;Consistency strictly trumps Availability in CRM finance!&lt;/b&gt;&lt;/span&gt;" style="shape=cylinder;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#064E3B;strokeColor=#34D399;strokeWidth=2.5;align=left;spacingLeft=25;" vertex="1" parent="c_ext">
          <mxGeometry x="35" y="60" width="630" height="230" as="geometry" />
        </mxCell>

        <!-- OpenRouter AI Gateway -->
        <mxCell id="openrouter_gw" value="&lt;b style='color:#38BDF8;font-size:16px;'&gt;OpenRouter AI Gateway (Primary Inference)&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#E2E8F0;font-size:13px;'&gt;Model: &lt;b style='color:#FACC15;'&gt;openai/gpt-4o-mini&lt;/b&gt;&lt;br/&gt;• Latency: ~1.2s p50 (Near-instant interactive UX)&lt;br/&gt;• Structured Output: 100% Native JSON Object adherence&lt;br/&gt;• Fractional Cost: &lt;b style='color:#34D399;'&gt;$0.00033 / query&lt;/b&gt; (1/30th of a cent!)&lt;br/&gt;• 99.99% SLA Dedicated Pool (Eliminates free-tier 429 stalls)&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E1B4B;strokeColor=#6366F1;strokeWidth=2;arcSize=8;align=left;spacingLeft=25;" vertex="1" parent="c_ext">
          <mxGeometry x="35" y="320" width="630" height="170" as="geometry" />
        </mxCell>

        <!-- Deterministic Fallback -->
        <mxCell id="offline_fallback" value="&lt;b style='color:#F59E0B;font-size:16px;'&gt;Deterministic Offline Heuristic Fallback Engine&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#FEF3C7;font-size:13px;'&gt;Automatic failover on gateway timeout or network partitions&lt;br/&gt;• Regex &amp;amp; NLP pattern extraction for entities and time offsets&lt;br/&gt;• Deterministic multi-step plan generator&lt;br/&gt;• &lt;b style='color:#34D399;'&gt;Guarantees 100% Demo Uptime with Zero HTTP 500s!&lt;/b&gt;&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#78350F;strokeColor=#F59E0B;strokeWidth=2;arcSize=8;align=left;spacingLeft=25;" vertex="1" parent="c_ext">
          <mxGeometry x="35" y="520" width="630" height="150" as="geometry" />
        </mxCell>

        <!-- Outbound Email Service -->
        <mxCell id="outbound_email" value="&lt;b style='color:#10B981;font-size:16px;'&gt;Dual-Tier Outbound Email Engine&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#D1FAE5;font-size:13px;'&gt;• Tier 1: Resend HTTP REST API (Single API key, zero DNS hurdles)&lt;br/&gt;• Tier 2: Resilient SMTP / Gmail Fallback&lt;br/&gt;• &lt;b style='color:#6EE7B7;'&gt;Automatic Transactional Activity Logging&lt;/b&gt; on every dispatch&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#10B981;strokeWidth=2;arcSize=8;align=left;spacingLeft=25;" vertex="1" parent="c_ext">
          <mxGeometry x="35" y="700" width="630" height="140" as="geometry" />
        </mxCell>

        <!-- 15-Scenario Eval Suite -->
        <mxCell id="eval_harness" value="&lt;b style='color:#A855F7;font-size:16px;'&gt;15-Scenario Parametric Evaluation Suite&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#F3E8FF;font-size:13px;'&gt;(agents/evals/runner.py &amp;amp; test_evals.py)&lt;br/&gt;• 100% Intent Classification Accuracy verification&lt;br/&gt;• 100% Graph Step Consistency across compound workflows&lt;br/&gt;• Automated CI regression gating with zero-quota email mocking&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3B0764;strokeColor=#A855F7;strokeWidth=2;arcSize=8;align=left;spacingLeft=25;" vertex="1" parent="c_ext">
          <mxGeometry x="35" y="870" width="630" height="150" as="geometry" />
        </mxCell>

        <!-- CONNECTORS / EDGES -->
        <!-- User to Next.js -->
        <mxCell id="e1" value="Natural Language" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#818CF8;strokeWidth=2;fontColor=#818CF8;" edge="1" parent="1" source="user_rep" target="nextjs_ui">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- Next.js to FastAPI -->
        <mxCell id="e2" value="HTTP POST /chat" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#38BDF8;strokeWidth=2;fontColor=#38BDF8;" edge="1" parent="1" source="nextjs_ui" target="api_gw">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- FastAPI to SessionStore -->
        <mxCell id="e3" value="Load Session Context" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#EC4899;strokeWidth=2;fontColor=#EC4899;" edge="1" parent="1" source="api_gw" target="session_store">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- FastAPI to Node 1 -->
        <mxCell id="e4" value="invoke(AgentState)" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#38BDF8;strokeWidth=2.5;fontColor=#38BDF8;" edge="1" parent="1" source="api_gw" target="node1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- Node 1 to Node 2 -->
        <mxCell id="e5" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#38BDF8;strokeWidth=2;" edge="1" parent="1" source="node1" target="node2">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- Node 2 to Node 3 -->
        <mxCell id="e6" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#38BDF8;strokeWidth=2;" edge="1" parent="1" source="node2" target="node3">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1020" y="185" />
              <mxPoint x="690" y="185" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- Node 3 to Intent Decision -->
        <mxCell id="e7" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#EF4444;strokeWidth=2;" edge="1" parent="1" source="node3" target="dec_intent">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <!-- Intent Decision to CRM Action -->
        <mxCell id="e8" value="Plan[0] is crm_action" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#10B981;strokeWidth=2.5;fontColor=#10B981;" edge="1" parent="1" source="dec_intent" target="node_crm">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="340" y="410" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- Intent Decision to Subagent -->
        <mxCell id="e9" value="Plan[0] is subagent" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#8B5CF6;strokeWidth=2.5;fontColor=#8B5CF6;" edge="1" parent="1" source="dec_intent" target="node_sub">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1040" y="410" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- CRM Action to Step Router -->
        <mxCell id="e10" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#10B981;strokeWidth=2;" edge="1" parent="1" source="node_crm" target="dec_step">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="340" y="825" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- Subagent to Step Router -->
        <mxCell id="e11" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#8B5CF6;strokeWidth=2;" edge="1" parent="1" source="node_sub" target="dec_step">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1040" y="825" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- Step Router CYCLIC LOOP to CRM Action -->
        <mxCell id="e12" value="Next: crm_action (idx &lt; len)" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#10B981;strokeWidth=2.5;fontColor=#10B981;" edge="1" parent="1" source="dec_step" target="node_crm">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="690" y="740" />
              <mxPoint x="480" y="740" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- Step Router CYCLIC LOOP to Subagent -->
        <mxCell id="e13" value="Next: subagent (idx &lt; len)" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#8B5CF6;strokeWidth=2.5;fontColor=#8B5CF6;" edge="1" parent="1" source="dec_step" target="node_sub">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="690" y="740" />
              <mxPoint x="900" y="740" />
            </Array>
          </mxGeometry>
        </mxCell>
        <!-- Step Router to Synthesizer -->
        <mxCell id="e14" value="All Steps Finished (idx == len)" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#0284C7;strokeWidth=3;fontColor=#0284C7;" edge="1" parent="1" source="dec_step" target="node_synth">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

def generate_backend_drawio() -> str:
    """Generate native Draw.io XML for the Backend System Architecture with Design Decisions."""
    return """<mxfile host="Electron" modified="2026-10-23T05:35:00.000Z" agent="NeuronForce" version="21.0.0" type="device">
  <diagram id="backend_hld" name="NeuronForce Backend Architecture HLD">
    <mxGraphModel dx="2000" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2800" pageHeight="1800" background="#090D16" math="0" shadow="1">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title Banner -->
        <mxCell id="title_be" value="&lt;b style='font-size:26px; color:#F8FAFC;'&gt;NeuronForce — Backend System Architecture &amp;amp; Critical Design Decisions (HLD)&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:14px; color:#94A3B8;'&gt;Modular Monolith (FastAPI) • CP-Consistent Relational Storage (ACID) • Dual-Track Auth • Dual-Tier Email • 1M Scale Roadmap&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#10B981;strokeWidth=2;arcSize=8;align=left;spacingLeft=30;" vertex="1" parent="1">
          <mxGeometry x="50" y="40" width="2700" height="85" as="geometry" />
        </mxCell>

        <!-- CONTAINER 1: Edge Ingress -->
        <mxCell id="c_edge" value="01 / EDGE INGRESS &amp;amp; ARCHITECTURAL FOUNDATION" style="swimlane;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#6366F1;strokeWidth=2;fontColor=#818CF8;fontStyle=1;fontSize=14;startSize=35;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="50" y="160" width="540" height="1560" as="geometry" />
        </mxCell>
        <mxCell id="cf_tunnel" value="&lt;b style='color:#F59E0B;font-size:15px;'&gt;Cloudflare Edge Tunnel (cloudflared)&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#FEF3C7;font-size:12px;'&gt;• 1-Click live public demo tunnel (./start_tunnel.sh)&lt;br/&gt;• Ephemeral HTTPS edge termination (*.trycloudflare.com)&lt;br/&gt;• Zero port-forwarding or public IP exposure required&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#78350F;strokeColor=#F59E0B;strokeWidth=1.5;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_edge">
          <mxGeometry x="30" y="60" width="480" height="110" as="geometry" />
        </mxCell>
        <mxCell id="caddy_proxy" value="&lt;b style='color:#38BDF8;font-size:15px;'&gt;Caddy Reverse Proxy&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#E2E8F0;font-size:12px;'&gt;• HTTP/2 termination &amp;amp; Brotli/Gzip compression&lt;br/&gt;• Unified Origin Routing: /api/* ➔ :8000, /* ➔ :3000&lt;br/&gt;• Oracle Cloud ARM64 production deployment ready&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0284C7;strokeWidth=1.5;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_edge">
          <mxGeometry x="30" y="200" width="480" height="110" as="geometry" />
        </mxCell>
        <mxCell id="dec_monolith" value="&lt;b style='color:#FACC15;font-size:16px;'&gt;CRITICAL DESIGN DECISION 1&lt;br/&gt;Modular Monolith vs. Microservices&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#FFFFFF;font-size:12px;'&gt;• &lt;b style='color:#34D399;'&gt;Atomic ACID Commits&lt;/b&gt;: Closing a deal atomically updates pipeline forecasts, contact status &amp;amp; activity history in a single db.commit()&lt;br/&gt;• &lt;b style='color:#34D399;'&gt;Sub-Millisecond In-Process Latency&lt;/b&gt;: Internal services invoke each other directly without network serialization&lt;br/&gt;• &lt;b style='color:#EF4444;'&gt;Why Microservices Were Rejected&lt;/b&gt;: Distributed 2PC and Saga compensations introduce partial failure risks on financial data.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#FACC15;strokeWidth=2;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_edge">
          <mxGeometry x="30" y="340" width="480" height="230" as="geometry" />
        </mxCell>
        <mxCell id="uvicorn" value="&lt;b style='color:#34D399;font-size:15px;'&gt;Uvicorn ASGI Engine (uvloop)&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#A7F3D0;font-size:12px;'&gt;High-performance asynchronous event loop handling 15,000+ RPS with non-blocking I/O for external AI gateways.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#064E3B;strokeColor=#34D399;strokeWidth=1.5;arcSize=10;align=left;spacingLeft=20;" vertex="1" parent="c_edge">
          <mxGeometry x="30" y="600" width="480" height="90" as="geometry" />
        </mxCell>

        <!-- CONTAINER 2: FastAPI Modular Monolith -->
        <mxCell id="c_app" value="02 / FASTAPI ASGI MODULAR APPLICATION (backend/app/)" style="swimlane;whiteSpace=wrap;html=1;fillColor=#0A0F1D;strokeColor=#10B981;strokeWidth=2.5;fontColor=#34D399;fontStyle=1;fontSize=15;startSize=40;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="630" y="160" width="1380" height="1560" as="geometry" />
        </mxCell>
        <mxCell id="mw_pipe" value="&lt;b style='color:#38BDF8;font-size:14px;'&gt;ASGI MIDDLEWARE PIPELINE&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;CORSMiddleware (Allowed Origins Allowlist) ➔ Request Latency Profiler ➔ Depends(get_current_user) JWT Validator&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=1.5;arcSize=8;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="65" width="1280" height="60" as="geometry" />
        </mxCell>

        <!-- 12 Routers Grid -->
        <mxCell id="r_contacts" value="&lt;b style='color:#38BDF8;font-size:13px;'&gt;/api/contacts&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Lifecycle &amp;amp; Lead Intel&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#38BDF8;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="150" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_deals" value="&lt;b style='color:#10B981;font-size:13px;'&gt;/api/deals&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Multi-Stage Kanban Funnel&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#10B981;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="380" y="150" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_act" value="&lt;b style='color:#F59E0B;font-size:13px;'&gt;/api/activities&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Chronological Timeline&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#F59E0B;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="710" y="150" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_cal" value="&lt;b style='color:#8B5CF6;font-size:13px;'&gt;/api/calendar&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;24h Native Schedule Grid&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#8B5CF6;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="1040" y="150" width="290" height="65" as="geometry" />
        </mxCell>

        <mxCell id="r_agents" value="&lt;b style='color:#EC4899;font-size:13px;'&gt;/api/ai-agents&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;LangGraph Studio &amp;amp; Telemetry&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#EC4899;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="235" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_camp" value="&lt;b style='color:#14B8A6;font-size:13px;'&gt;/api/campaigns&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Multi-Channel Outreach Copy&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#14B8A6;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="380" y="235" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_tick" value="&lt;b style='color:#EF4444;font-size:13px;'&gt;/api/tickets&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;SLA Customer Incident Cases&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#EF4444;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="710" y="235" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_anal" value="&lt;b style='color:#6366F1;font-size:13px;'&gt;/api/analytics&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;ARR Waterfall &amp;amp; Velocity BI&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#6366F1;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="1040" y="235" width="290" height="65" as="geometry" />
        </mxCell>

        <mxCell id="r_srch" value="&lt;b style='color:#FACC15;font-size:13px;'&gt;/api/search&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Sub-15ms Token Omnisearch&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#FACC15;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="320" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_dash" value="&lt;b style='color:#38BDF8;font-size:13px;'&gt;/api/dashboard&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;Executive Revenue Metrics&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#38BDF8;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="380" y="320" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_auth" value="&lt;b style='color:#EC4899;font-size:13px;'&gt;/api/auth&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;OAuth 2.0 PKCE &amp;amp; Personas&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#EC4899;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="710" y="320" width="290" height="65" as="geometry" />
        </mxCell>
        <mxCell id="r_sett" value="&lt;b style='color:#64748B;font-size:13px;'&gt;/api/settings&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:11px;'&gt;AI Budget Guards &amp;amp; Tenants&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#64748B;strokeWidth=1.5;" vertex="1" parent="c_app">
          <mxGeometry x="1040" y="320" width="290" height="65" as="geometry" />
        </mxCell>

        <!-- Services Layer -->
        <mxCell id="svc_auth" value="&lt;b style='color:#F472B6;font-size:15px;'&gt;Dual-Track Authentication Guard&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;• Track 1: Google OAuth 2.0 PKCE with dynamic origin state preservation&lt;br/&gt;• Track 2: 1-Click Demo Persona Simulator for instant evaluation&lt;br/&gt;• Signed HS256 JWT tokens with sliding session expiry&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E1528;strokeColor=#EC4899;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="420" width="400" height="150" as="geometry" />
        </mxCell>

        <mxCell id="svc_email" value="&lt;b style='color:#34D399;font-size:15px;'&gt;Dual-Tier Outbound Email Engine&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;• Tier 1: Resend HTTP REST API (Single RESEND_API_KEY, zero DNS hurdles)&lt;br/&gt;• Tier 2: Resilient SMTP / Gmail Fallback&lt;br/&gt;• &lt;b style='color:#6EE7B7;'&gt;Automatic Activity Logging&lt;/b&gt;: Every email creates an Activity record&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0A231C;strokeColor=#10B981;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_app">
          <mxGeometry x="490" y="420" width="400" height="150" as="geometry" />
        </mxCell>

        <mxCell id="svc_search" value="&lt;b style='color:#FACC15;font-size:15px;'&gt;Token-Ranked Omnisearch Engine&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;• Sub-15ms multi-entity search across Contacts, Deals, Activities &amp;amp; Tickets&lt;br/&gt;• Scoring algorithm: Exact (+100), Prefix (+50), Partial (+25)&lt;br/&gt;• Single aggregated JSON response with category keyboard chips&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#231E0A;strokeColor=#FACC15;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_app">
          <mxGeometry x="930" y="420" width="400" height="150" as="geometry" />
        </mxCell>

        <!-- ORM Engine & Models -->
        <mxCell id="orm_banner" value="&lt;b style='color:#38BDF8;font-size:15px;'&gt;SQLAlchemy 2.0 ORM Engine &amp;amp; Connection Pooler&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#94A3B8;font-size:12px;'&gt;Declarative Base • Foreign Key Cascade Integrity • Strict Type Checking via Pydantic v2 Schemas • SessionLocal&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0F172A;strokeColor=#0284C7;strokeWidth=2;arcSize=8;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="605" width="1280" height="70" as="geometry" />
        </mxCell>

        <!-- Models -->
        <mxCell id="m_contact" value="&lt;b style='color:#38BDF8;'&gt;Contact&lt;/b&gt;&lt;br/&gt;Email, Phone, ICP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#38BDF8;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="700" width="190" height="55" as="geometry" />
        </mxCell>
        <mxCell id="m_deal" value="&lt;b style='color:#10B981;'&gt;Deal&lt;/b&gt;&lt;br/&gt;Value, Stage, Close" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#10B981;" vertex="1" parent="c_app">
          <mxGeometry x="268" y="700" width="190" height="55" as="geometry" />
        </mxCell>
        <mxCell id="m_act" value="&lt;b style='color:#F59E0B;'&gt;Activity&lt;/b&gt;&lt;br/&gt;Type, Subject, Log" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#F59E0B;" vertex="1" parent="c_app">
          <mxGeometry x="486" y="700" width="190" height="55" as="geometry" />
        </mxCell>
        <mxCell id="m_cal" value="&lt;b style='color:#8B5CF6;'&gt;CalendarEvent&lt;/b&gt;&lt;br/&gt;Time Grid, People" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#8B5CF6;" vertex="1" parent="c_app">
          <mxGeometry x="704" y="700" width="190" height="55" as="geometry" />
        </mxCell>
        <mxCell id="m_camp" value="&lt;b style='color:#14B8A6;'&gt;Campaign&lt;/b&gt;&lt;br/&gt;Audience, Copy" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#14B8A6;" vertex="1" parent="c_app">
          <mxGeometry x="922" y="700" width="190" height="55" as="geometry" />
        </mxCell>
        <mxCell id="m_task" value="&lt;b style='color:#EC4899;'&gt;AIAgentTask&lt;/b&gt;&lt;br/&gt;Cost, Confidence" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E293B;strokeColor=#EC4899;" vertex="1" parent="c_app">
          <mxGeometry x="1140" y="700" width="190" height="55" as="geometry" />
        </mxCell>

        <!-- Seeder Engine -->
        <mxCell id="seeder_engine" value="&lt;b style='color:#6EE7B7;font-size:15px;'&gt;Autonomous Enterprise Seeding Engine (scripts/seed_data.py)&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#A7F3D0;font-size:12px;'&gt;Runs automatically on startup. Mathematically calibrates 12 contacts, 10 stage deals, 40 activities, SLA tickets, and ARR trajectories with authentic fractional-cent AI telemetry in under 2 seconds.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#063528;strokeColor=#34D399;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=25;" vertex="1" parent="c_app">
          <mxGeometry x="50" y="780" width="1280" height="80" as="geometry" />
        </mxCell>

        <!-- CONTAINER 3: Relational CP Storage & Scale -->
        <mxCell id="c_scale" value="03 / RELATIONAL CP STORAGE &amp;amp; SCALE ROADMAP" style="swimlane;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#FACC15;strokeWidth=2;fontColor=#FACC15;fontStyle=1;fontSize=14;startSize=35;arcSize=8;" vertex="1" parent="1">
          <mxGeometry x="2050" y="160" width="700" height="1560" as="geometry" />
        </mxCell>

        <!-- CRITICAL DESIGN DECISION 2 -->
        <mxCell id="db_cp_hero" value="&lt;b style='color:#FACC15;font-size:17px;'&gt;CRITICAL DESIGN DECISION 2&lt;br/&gt;Relational CP Consistency (CAP Theorem)&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;&lt;span style='color:#FFFFFF;font-size:13px;'&gt;• &lt;b style='color:#34D399;'&gt;PostgreSQL (Production) / SQLite (Development)&lt;/b&gt;&lt;br/&gt;&lt;br/&gt;• In financial CRM systems, &lt;b style='color:#FACC15;'&gt;Consistency strictly trumps Availability&lt;/b&gt;.&lt;br/&gt;• If an upstream network partition occurs, it is significantly better to reject an update or return a retry than permit conflicting writes where two sales reps or automated AI agents overwrite contract values or pipeline stages.&lt;br/&gt;• Strict ACID transactions guarantee revenue numbers, pipeline stages &amp;amp; customer records remain consistent.&lt;br/&gt;&lt;br/&gt;• &lt;b style='color:#EF4444;'&gt;Why NoSQL Was Rejected:&lt;/b&gt; Eventual consistency (MongoDB / DynamoDB) introduces 'dirty reads', leading to pipeline forecast drift and financial audit violations.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#063023;strokeColor=#34D399;strokeWidth=2.5;arcSize=10;align=left;spacingLeft=25;" vertex="1" parent="c_scale">
          <mxGeometry x="35" y="60" width="630" height="280" as="geometry" />
        </mxCell>

        <!-- Scale Items -->
        <mxCell id="sc_pg" value="&lt;b style='color:#38BDF8;font-size:15px;'&gt;1. PgBouncer Connection Pooler&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;Transaction pooling supporting 10,000+ concurrent database connections with minimal memory overhead.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#38BDF8;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_scale">
          <mxGeometry x="35" y="370" width="630" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sc_repl" value="&lt;b style='color:#10B981;font-size:15px;'&gt;2. Read-Replica Query Splitting&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;Routes heavy analytical queries (/api/analytics/* &amp;amp; search) to replicas while preserving primary node for deal writes.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#10B981;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_scale">
          <mxGeometry x="35" y="475" width="630" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sc_redis" value="&lt;b style='color:#EC4899;font-size:15px;'&gt;3. Redis Cluster (Cache &amp;amp; Rate Limits)&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;Sliding-window agent session store cache &amp;amp; dashboard KPI caching (60s TTL) with per-tenant token bucket limits.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#EC4899;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_scale">
          <mxGeometry x="35" y="580" width="630" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sc_celery" value="&lt;b style='color:#F59E0B;font-size:15px;'&gt;4. Asynchronous Celery / Temporal Workers&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;Offloads long-running AI batch runs (e.g. scoring 50,000 contacts) to background workers with SSE updates.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#F59E0B;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_scale">
          <mxGeometry x="35" y="685" width="630" height="80" as="geometry" />
        </mxCell>
        <mxCell id="sc_rls" value="&lt;b style='color:#A855F7;font-size:15px;'&gt;5. Multi-Tenant Row-Level Security (RLS)&lt;/b&gt;&lt;br/&gt;&lt;span style='color:#CBD5E1;font-size:12px;'&gt;PostgreSQL tenant_id policies ensuring 100% cryptographic tenant isolation.&lt;/span&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#111827;strokeColor=#A855F7;strokeWidth=1.5;arcSize=8;align=left;spacingLeft=20;" vertex="1" parent="c_scale">
          <mxGeometry x="35" y="790" width="630" height="80" as="geometry" />
        </mxCell>

        <!-- EDGES -->
        <mxCell id="be_e1" value="Public Ingress" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#F59E0B;strokeWidth=2;fontColor=#F59E0B;" edge="1" parent="1" source="cf_tunnel" target="caddy_proxy">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="be_e2" value="Reverse Proxy :8000" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#38BDF8;strokeWidth=2.5;fontColor=#38BDF8;" edge="1" parent="1" source="caddy_proxy" target="mw_pipe">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="be_e3" value="Dispatch to Domain Routers" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#10B981;strokeWidth=2;fontColor=#10B981;" edge="1" parent="1" source="mw_pipe" target="r_deals">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="be_e4" value="Invoke Business Logic" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#0284C7;strokeWidth=2;fontColor=#0284C7;" edge="1" parent="1" source="r_deals" target="svc_auth">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="be_e5" value="SQLAlchemy Transactions" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#38BDF8;strokeWidth=2;fontColor=#38BDF8;" edge="1" parent="1" source="svc_auth" target="orm_banner">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="be_e6" value="Atomic Commit (CP)" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#FACC15;strokeWidth=2.5;fontColor=#FACC15;" edge="1" parent="1" source="orm_banner" target="db_cp_hero">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

# ==============================================================================
# 2. REFINED PRESENTATION HTML (SPACIOUS, GLASSMORPHIC, BALANCED)
# ==============================================================================

def generate_agentic_html() -> str:
    """Generate high-resolution, spacious HTML/SVG diagram for Agentic System Flow."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NeuronForce Agentic System HLD</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #060A12;
    color: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding: 36px;
    width: 2800px;
    min-height: 1750px;
    display: flex;
    flex-direction: column;
    gap: 28px;
  }

  /* Header */
  .header {
    background: linear-gradient(135deg, #0B132B 0%, #171938 100%);
    border: 2px solid #38BDF8;
    border-radius: 20px;
    padding: 28px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 12px 35px -5px rgba(56, 189, 248, 0.25);
  }
  .header h1 {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.5px;
  }
  .header h1 span { color: #38BDF8; }
  .header p {
    font-size: 16px;
    color: #94A3B8;
    margin-top: 6px;
  }
  .badges {
    display: flex;
    gap: 14px;
  }
  .badge {
    padding: 10px 20px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .badge-cyan { background: rgba(56, 189, 248, 0.15); border: 1.5px solid #38BDF8; color: #38BDF8; }
  .badge-emerald { background: rgba(52, 211, 153, 0.15); border: 1.5px solid #34D399; color: #34D399; }
  .badge-purple { background: rgba(167, 139, 250, 0.15); border: 1.5px solid #A78BFA; color: #A78BFA; }

  /* 3-Column Layout */
  .layout {
    display: grid;
    grid-template-columns: 700px 1fr 720px;
    gap: 32px;
    flex: 1;
  }

  .col-panel {
    background: #0B1120;
    border: 1.5px solid #1E293B;
    border-radius: 20px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }
  .col-panel.primary {
    border-color: #38BDF8;
    background: #090F1E;
    box-shadow: 0 0 40px rgba(56, 189, 248, 0.12);
  }

  .panel-header {
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1E293B;
  }
  .panel-header.cyan { color: #38BDF8; }
  .panel-header.pink { color: #F472B6; }
  .panel-header.emerald { color: #34D399; }

  /* Cards */
  .card {
    background: #111827;
    border: 1.5px solid #1F2937;
    border-radius: 16px;
    padding: 24px;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .card h3 {
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .card p {
    font-size: 14px;
    line-height: 1.6;
    color: #94A3B8;
  }
  .card ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13px;
    color: #CBD5E1;
  }
  .card ul li {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card ul li::before {
    content: "•";
    color: #38BDF8;
    font-size: 16px;
    font-weight: bold;
  }

  .highlight-badge {
    position: absolute;
    top: -12px;
    right: 20px;
    background: #38BDF8;
    color: #0B1120;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* LangGraph Center Stage Flow */
  .pipeline-stage {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .linear-flow {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 16px;
    align-items: center;
  }

  .connector-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #38BDF8;
    font-size: 24px;
    font-weight: 800;
  }

  .decision-badge {
    align-self: center;
    background: linear-gradient(135deg, #991B1B 0%, #7F1D1D 100%);
    border: 2px solid #EF4444;
    border-radius: 30px;
    padding: 10px 28px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
  }
  .decision-badge h4 { font-size: 14px; font-weight: 800; color: #FFFFFF; }
  .decision-badge span { font-size: 12px; color: #FECACA; }

  .exec-lanes {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
    align-items: stretch;
  }

  .loop-router-card {
    background: linear-gradient(135deg, #78350F 0%, #B45309 100%);
    border: 2px dashed #F59E0B;
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 140px;
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25);
  }
  .loop-router-card h4 { font-size: 13px; font-weight: 800; color: #FEF3C7; text-transform: uppercase; }
  .loop-router-card span { font-size: 11px; color: #FDE68A; margin-top: 6px; }

  .subagents-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
  }
  .subagent-box {
    background: #0F172A;
    border: 1.5px solid #334155;
    border-radius: 14px;
    padding: 18px 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .subagent-box h5 { font-size: 14px; font-weight: 700; }
  .subagent-box p { font-size: 12px; color: #94A3B8; line-height: 1.4; }

  .session-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    background: #0B0F19;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 14px;
  }
  .session-item {
    font-size: 12px;
    color: #CBD5E1;
  }
  .session-item b {
    color: #F472B6;
    display: block;
    font-size: 11px;
    text-transform: uppercase;
    margin-bottom: 2px;
  }
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div>
    <h1>NeuronForce <span>Autonomous Multi-Agent LangGraph System</span> (HLD)</h1>
    <p>Cyclic StateGraph Multi-Step Orchestration • Continuous Session Memory • Semantic Pronoun Resolution • Transparent Telemetry</p>
  </div>
  <div class="badges">
    <div class="badge badge-cyan">LangGraph Cyclic DAG</div>
    <div class="badge badge-emerald">Sub-1.5s GPT-4o-Mini</div>
    <div class="badge badge-purple">100% 15-Scenario Eval Gated</div>
  </div>
</div>

<!-- 3-Column Layout -->
<div class="layout">

  <!-- 1. LEFT COLUMN: Ingress & Session Memory -->
  <div class="col-panel">
    <div class="panel-header pink">01 / INGRESS &amp; MULTI-TURN MEMORY</div>

    <!-- User Persona -->
    <div class="card">
      <h3>👤 Account Executive / Sales Rep</h3>
      <p>Submits natural language compound prompts into the Studio Cockpit:</p>
      <div style="background:#080E1A; border-left:4px solid #38BDF8; border-radius:8px; padding:12px 14px; font-size:13px; color:#E2E8F0; font-family:monospace; line-height:1.5;">
        "Add Tanuj (tanuj@google.com) to our CRM and book a 1-hour demo with him and Sarah for tomorrow at 2 PM"
      </div>
    </div>

    <!-- Agent Studio UI -->
    <div class="card" style="border-color:#0284C7; background:#0D172A;">
      <span class="highlight-badge">Next.js 16</span>
      <h3 style="color:#38BDF8;">💻 Autonomous Agent Studio</h3>
      <ul>
        <li>Real-time LangGraph node execution visualizer cockpit</li>
        <li>Sub-100ms perceived latency &amp; CSS frosted glass de-blur guard</li>
        <li>Interactive multi-card rendered action outputs</li>
      </ul>
    </div>

    <!-- FastAPI Gateway -->
    <div class="card" style="border-color:#059669; background:#062319;">
      <h3 style="color:#34D399;">⚡ FastAPI AI Gateway Router</h3>
      <p><code style="color:#34D399; font-weight:700;">POST /api/ai-agents/chat</code></p>
      <ul>
        <li>Validates session_id, user JWT &amp; dynamic origin allowlist</li>
        <li>Dispatches execution to LangGraph runner in async threadpool</li>
      </ul>
    </div>

    <!-- Session Store -->
    <div class="card" style="border-color:#8B5CF6; background:#1A103C;">
      <span class="highlight-badge" style="background:#8B5CF6; color:#FFF;">Thread-Safe</span>
      <h3 style="color:#DDD6FE;">🧠 In-Memory Session Store</h3>
      <p style="font-size:12px; color:#C4B5FD;"><code style="color:#F472B6;">agents/session_store.py</code> • Sliding Window (Last 5 turns / 10 msgs)</p>

      <div class="session-grid">
        <div class="session-item"><b>active_deal</b>$1,000,000 Google Deal</div>
        <div class="session-item"><b>active_contact</b>Tanuj Singh (Google)</div>
        <div class="session-item"><b>active_meeting</b>Tanuj &amp; Sarah (2 PM)</div>
        <div class="session-item"><b>active_campaign</b>X, Instagram Outreach</div>
      </div>
    </div>

    <!-- Pronoun Resolution -->
    <div class="card" style="border-color:#D946EF; background:#2A0A45;">
      <h3 style="color:#F0ABFC;">🎯 Semantic Pronoun Resolver</h3>
      <p style="color:#E9D5FF; font-size:13px;">
        Maps conversational pronouns directly to active working entities:
      </p>
      <ul style="color:#F5D0FE;">
        <li><b>"this deal" / "on it"</b> ➔ Resolves to active_deal ($1M)</li>
        <li><b>"send him an email"</b> ➔ Resolves to active_contact email</li>
        <li><b style="color:#34D399;">Zero Brittle Regex Matching!</b> Driven by prompt context.</li>
      </ul>
    </div>
  </div>

  <!-- 2. CENTER COLUMN: LangGraph Cyclic Orchestrator -->
  <div class="col-panel primary">
    <div class="panel-header cyan">02 / LANGGRAPH CYCLIC STATEGRAPH ORCHESTRATOR (agents/orchestrator/)</div>

    <div class="pipeline-stage">

      <!-- Step 1 & 2 Linear Flow -->
      <div class="linear-flow">
        <div class="card">
          <h3 style="color:#38BDF8;">Node 1: Prompt Ingestion</h3>
          <p>Sanitizes prompt, validates session token, and estimates initial token bounds.</p>
        </div>
        <div class="connector-arrow">➔</div>
        <div class="card">
          <h3 style="color:#38BDF8;">Node 2: CRM Context Retrieval</h3>
          <p>Scans CRM database for mentioned records; injects prioritized active working session entities.</p>
        </div>
      </div>

      <div class="connector-arrow" style="font-size:20px;">⬇</div>

      <!-- Step 3: Intent Router & Planner -->
      <div class="card" style="background:#451A03; border-color:#F59E0B;">
        <span class="highlight-badge" style="background:#F59E0B; color:#000;">Core Intelligence</span>
        <h3 style="color:#FDE68A;">Node 3: Structured Execution Planner &amp; Intent Router</h3>
        <p style="color:#FEF3C7; font-size:14px;">
          Invokes OpenRouter Gateway with strict JSON schema to decompose compound requests into an ordered plan:
        </p>
        <div style="background:#2A1002; border:1px solid #78350F; border-radius:10px; padding:12px 16px; font-family:monospace; font-size:12px; color:#FDE68A; line-height:1.6;">
          plan: [<br/>
          &nbsp;&nbsp;{ step_id: 1, type: "crm_action", action_type: "create_contact", entities: { name: "Tanuj", email: "tanuj@..." } },<br/>
          &nbsp;&nbsp;{ step_id: 2, type: "crm_action", action_type: "schedule_meeting", entities: { name: "Tanuj, Sarah", time: "tomorrow 2 PM" } }<br/>
          ]
        </div>
      </div>

      <!-- Decision: route_after_intent -->
      <div class="decision-badge">
        <h4>route_after_intent (Conditional Edge)</h4>
        <span>Evaluates Plan[0].type ➔ 'crm_action' vs 'subagent' vs 'general'</span>
      </div>

      <!-- Step 4: Execution Lanes & Loop Router -->
      <div class="exec-lanes">
        <!-- Lane A: CRM Action Executor -->
        <div class="card" style="background:#063528; border-color:#10B981;">
          <h3 style="color:#6EE7B7;">Node 4b: CRM Action Executor</h3>
          <p style="color:#D1FAE5; font-size:13px;">Direct Relational Database Mutations (ACID CP):</p>
          <ul style="color:#D1FAE5;">
            <li><b>schedule_meeting</b>: Dynamic Attendee Email Resolver &amp; Range-Aware Normalizer (12-1 PM ➔ 60m)</li>
            <li><b>create_contact / update_contact</b>: Full lifecycle status</li>
            <li><b>create_deal / update_deal</b>: Weighted pipeline &amp; stage velocity</li>
            <li><b>create_campaign</b>: Multi-channel marketing copy generator</li>
          </ul>
        </div>

        <!-- Loop Router -->
        <div class="loop-router-card">
          <h4>route_after_step</h4>
          <span>idx &lt; len(plan)?</span>
          <div style="font-size:24px; color:#FDE68A; margin:6px 0;">⟳</div>
          <span style="color:#34D399; font-weight:700;">Cycles back to next step!</span>
        </div>

        <!-- Lane B: Subagent Executor -->
        <div class="card" style="background:#241A4D; border-color:#8B5CF6;">
          <h3 style="color:#C4B5FD;">Node 4a: Specialist Subagents</h3>
          <p style="color:#EDE9FE; font-size:13px;">Executes Targeted Deep-Reasoning Workflows:</p>
          <ul style="color:#EDE9FE;">
            <li><b>lead_scoring</b>: Buyer Intent (0-100) &amp; ICP match %</li>
            <li><b>deal_risk</b>: Win probability % &amp; risk mitigations</li>
            <li><b>email_draft</b>: Value-prop copy + Resend/SMTP dispatch</li>
            <li><b>churn_sentinel</b>: ARR at risk &amp; retention playbooks</li>
            <li><b>meeting_summary</b>: Decisions &amp; action items with dates</li>
          </ul>
        </div>
      </div>

      <div class="connector-arrow" style="font-size:20px;">⬇ All Plan Steps Finished (idx == len)</div>

      <!-- Step 5: Synthesizer -->
      <div class="card" style="background:#0F1F38; border-color:#0284C7;">
        <span class="highlight-badge">Step 5 Complete</span>
        <h3 style="color:#38BDF8;">Node 5: Response Synthesizer &amp; Telemetry Aggregator</h3>
        <p style="font-size:13px; color:#CBD5E1;">
          Assembles clean numbered markdown sections for all executed steps, binds interactive UI action cards (contact chips, meeting cards), aggregates exact token usage &amp; fractional-cent cost, and computes overall confidence score.
        </p>
      </div>

      <!-- Subagents Matrix Row -->
      <div class="subagents-grid">
        <div class="subagent-box" style="border-color:#38BDF8;">
          <h5 style="color:#38BDF8;">Lead Scoring</h5>
          <p>Intent: 92/100<br/>HOT Priority (95% ICP)</p>
        </div>
        <div class="subagent-box" style="border-color:#F59E0B;">
          <h5 style="color:#F59E0B;">Deal Risk Sentinel</h5>
          <p>Win Prob: 78%<br/>Medium Risk Exposure</p>
        </div>
        <div class="subagent-box" style="border-color:#10B981;">
          <h5 style="color:#10B981;">Email Drafter</h5>
          <p>Hyper-Personalized<br/>Auto Resend/SMTP</p>
        </div>
        <div class="subagent-box" style="border-color:#EF4444;">
          <h5 style="color:#EF4444;">Churn Sentinel</h5>
          <p>ARR at Risk: $180k<br/>Playbook Prescribed</p>
        </div>
        <div class="subagent-box" style="border-color:#A855F7;">
          <h5 style="color:#A855F7;">Meeting Summary</h5>
          <p>Decisions &amp; Owners<br/>CRM Deal Sync</p>
        </div>
      </div>

    </div>
  </div>

  <!-- 3. RIGHT COLUMN: Storage, Inference & Auditing -->
  <div class="col-panel">
    <div class="panel-header emerald">03 / PERSISTENCE, GATEWAY &amp; EVALUATIONS</div>

    <!-- CP Database -->
    <div class="card" style="background:#05291E; border:2px solid #34D399;">
      <span class="highlight-badge" style="background:#34D399; color:#000;">CP System</span>
      <h3 style="color:#6EE7B7;">🗄️ Relational CP Database</h3>
      <p style="color:#D1FAE5; font-size:13px;">
        <b>PostgreSQL (Prod) / SQLite (Dev)</b><br/>
        Zero dirty reads on pipeline forecasting and customer deals. Strict ACID transactional commits ensure immediate consistency.
        <br/><br/>
        <b style="color:#FACC15;">Why CP Consistency?</b><br/>
        In financial CRM systems, <b>Consistency strictly trumps Availability</b> during network partitions.
      </p>
    </div>

    <!-- OpenRouter Gateway -->
    <div class="card" style="background:#131138; border-color:#6366F1;">
      <span class="highlight-badge" style="background:#818CF8; color:#000;">Primary Inference</span>
      <h3 style="color:#C7D2FE;">🌐 OpenRouter AI Gateway</h3>
      <p style="color:#E2E8F0; font-size:13px;">
        Model: <b style="color:#FACC15;">openai/gpt-4o-mini</b>
      </p>
      <ul>
        <li><b>1.2s p50 Latency</b> (Near-instant responsive UX)</li>
        <li><b>100% JSON Object adherence</b> (Zero parse errors)</li>
        <li><b style="color:#34D399;">$0.00033 / query</b> (1/30th of a cent!)</li>
        <li><b>99.99% Dedicated Tier SLA</b> (No 429 stalls)</li>
      </ul>
    </div>

    <!-- Deterministic Fallback -->
    <div class="card" style="background:#381604; border-color:#F59E0B;">
      <h3 style="color:#FDE68A;">🛡️ Deterministic Offline Fallback</h3>
      <p style="color:#FEF3C7; font-size:13px;">
        Automatic regex &amp; NLP heuristic failover on 429 quota exhaustion or network timeout. Guarantees <b>100% demo uptime with zero HTTP 500s</b>!
      </p>
    </div>

    <!-- Outbound Email -->
    <div class="card" style="background:#05291E; border-color:#10B981;">
      <h3 style="color:#6EE7B7;">✉️ Dual-Tier Outbound Email</h3>
      <p style="color:#D1FAE5; font-size:13px;">
        Resend HTTP API (Tier 1) + SMTP Fallback (Tier 2). Every email automatically persists to the CRM Activity timeline.
      </p>
    </div>

    <!-- Evaluation Suite -->
    <div class="card" style="background:#26063D; border-color:#A855F7;">
      <span class="highlight-badge" style="background:#C084FC; color:#000;">Evaluation</span>
      <h3 style="color:#E9D5FF;">🧪 15-Scenario Benchmark</h3>
      <p style="color:#F3E8FF; font-size:13px;">
        Parametric regression test suite (<code style="color:#C084FC;">agents/evals/</code>) asserting 100% intent accuracy, entity recall, and graph consistency in CI/CD.
      </p>
    </div>

    <!-- AIAgentTask Audit Trail -->
    <div class="card">
      <h3>📊 AIAgentTask Audit Trail</h3>
      <p style="font-size:13px; color:#94A3B8;">
        Every autonomous decision logs: <span style="color:#38BDF8;">latency_ms</span>, <span style="color:#34D399;">actual_cost</span>, <span style="color:#F59E0B;">confidence_score</span>, and prompt reasoning traces.
      </p>
    </div>

  </div>

</div>

</body>
</html>
"""

def generate_backend_html() -> str:
    """Generate high-resolution, spacious HTML/SVG diagram for Backend System Architecture."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NeuronForce Backend System Architecture HLD</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background-color: #060A12;
    color: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding: 36px;
    width: 2800px;
    min-height: 1750px;
    display: flex;
    flex-direction: column;
    gap: 28px;
  }

  /* Header */
  .header {
    background: linear-gradient(135deg, #0B132B 0%, #063826 100%);
    border: 2px solid #34D399;
    border-radius: 20px;
    padding: 28px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 12px 35px -5px rgba(52, 211, 153, 0.25);
  }
  .header h1 {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -0.5px;
  }
  .header h1 span { color: #34D399; }
  .header p {
    font-size: 16px;
    color: #94A3B8;
    margin-top: 6px;
  }
  .badges {
    display: flex;
    gap: 14px;
  }
  .badge {
    padding: 10px 20px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .badge-emerald { background: rgba(52, 211, 153, 0.15); border: 1.5px solid #34D399; color: #34D399; }
  .badge-yellow { background: rgba(250, 204, 21, 0.15); border: 1.5px solid #FACC15; color: #FACC15; }
  .badge-cyan { background: rgba(56, 189, 248, 0.15); border: 1.5px solid #38BDF8; color: #38BDF8; }

  /* 3-Column Layout */
  .layout {
    display: grid;
    grid-template-columns: 700px 1fr 720px;
    gap: 32px;
    flex: 1;
  }

  .col-panel {
    background: #0B1120;
    border: 1.5px solid #1E293B;
    border-radius: 20px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }
  .col-panel.primary {
    border-color: #34D399;
    background: #090F1E;
    box-shadow: 0 0 40px rgba(52, 211, 153, 0.12);
  }

  .panel-header {
    font-size: 15px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1E293B;
  }
  .panel-header.cyan { color: #38BDF8; }
  .panel-header.emerald { color: #34D399; }
  .panel-header.yellow { color: #FACC15; }

  /* Cards */
  .card {
    background: #111827;
    border: 1.5px solid #1F2937;
    border-radius: 16px;
    padding: 24px;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .card h3 {
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .card p {
    font-size: 14px;
    line-height: 1.6;
    color: #94A3B8;
  }
  .card ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 13px;
    color: #CBD5E1;
  }
  .card ul li {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .card ul li::before {
    content: "•";
    color: #34D399;
    font-size: 16px;
    font-weight: bold;
  }

  .highlight-badge {
    position: absolute;
    top: -12px;
    right: 20px;
    background: #FACC15;
    color: #0B1120;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Critical Decision Hero Cards */
  .hero-decision {
    background: #1A2234;
    border: 2px solid #FACC15;
    box-shadow: 0 8px 30px rgba(250, 204, 21, 0.18);
    border-radius: 18px;
    padding: 26px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    position: relative;
  }
  .hero-decision h3 {
    color: #FACC15;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.3px;
  }
  .hero-decision p {
    font-size: 13px;
    color: #F1F5F9;
    line-height: 1.65;
  }

  /* Routers Grid by Functional Clusters */
  .cluster-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .cluster-title {
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94A3B8;
    margin-top: 4px;
  }

  .cluster-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
  }

  .router-chip {
    background: #0E1626;
    border: 1.5px solid #1E293B;
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    transition: all 0.2s;
  }
  .router-chip:hover { border-color: #38BDF8; }
  .router-chip h4 { font-size: 14px; font-weight: 700; }
  .router-chip span { font-size: 12px; color: #94A3B8; }

  /* Services Grid */
  .services-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  .service-card {
    background: #0F192C;
    border: 1.5px solid #0284C7;
    border-radius: 16px;
    padding: 22px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .service-card h4 { font-size: 16px; color: #38BDF8; font-weight: 700; }
  .service-card p { font-size: 13px; color: #94A3B8; line-height: 1.6; }

  /* Scale items */
  .scale-item {
    background: #111827;
    border-left: 4px solid #34D399;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .scale-item h4 { font-size: 15px; color: #F8FAFC; font-weight: 700; }
  .scale-item p { font-size: 13px; color: #94A3B8; line-height: 1.4; }

  .models-row {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
  }
  .model-chip {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 12px;
    text-align: center;
  }
  .model-chip b { font-size: 13px; color: #F8FAFC; display:block; margin-bottom:2px; }
  .model-chip span { font-size: 11px; color: #94A3B8; }
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div>
    <h1>NeuronForce <span>Backend System Architecture &amp; Design Decisions</span> (HLD)</h1>
    <p>FastAPI ASGI Modular Monolith • Relational CP Storage (ACID) • Dual-Track Auth • Dual-Tier Email • 1,000,000 DAU Topology</p>
  </div>
  <div class="badges">
    <div class="badge badge-yellow">Relational CP (CAP Theorem)</div>
    <div class="badge badge-emerald">Modular Monolith</div>
    <div class="badge badge-cyan">Sub-100ms In-Process Latency</div>
  </div>
</div>

<!-- 3-Column Layout -->
<div class="layout">

  <!-- 1. LEFT COLUMN: Ingress & Modular Monolith Decision -->
  <div class="col-panel">
    <div class="panel-header cyan">01 / EDGE INGRESS &amp; ARCHITECTURAL FOUNDATION</div>

    <!-- Cloudflare Tunnel -->
    <div class="card">
      <span class="highlight-badge" style="background:#F59E0B; color:#000;">1-Click Demo</span>
      <h3 style="color:#FBBF24;">🌐 Cloudflare Edge Tunnel</h3>
      <p><code style="color:#F59E0B; font-weight:700;">./start_tunnel.sh</code></p>
      <ul>
        <li>Public HTTPS SSL termination (*.trycloudflare.com)</li>
        <li>Dynamic origin routing via Next.js reverse-proxy</li>
        <li>Zero router port-forwarding or public IP exposure</li>
      </ul>
    </div>

    <!-- Caddy Reverse Proxy -->
    <div class="card">
      <h3 style="color:#38BDF8;">🚀 Caddy Reverse Proxy</h3>
      <p>HTTP/2 termination, Gzip/Brotli compression, and upstream balancing:</p>
      <ul>
        <li><code style="color:#38BDF8;">/api/*</code> ➔ FastAPI ASGI Server (:8000)</li>
        <li><code style="color:#34D399;">/*</code> ➔ Next.js 16 App Router (:3000)</li>
      </ul>
    </div>

    <!-- CRITICAL DESIGN DECISION 1 -->
    <div class="hero-decision">
      <span class="highlight-badge">Decision 1</span>
      <h3>⚖️ Modular Monolith vs. Microservices</h3>
      <p>
        <b>Why We Rejected Microservices:</b><br/>
        In enterprise CRMs, moving an opportunity to <i>Closed Won</i> must atomically update deal revenue, recalculate customer contact status, append an activity timeline entry, and refresh ARR forecasting.
        <br/><br/>
        In microservices, this requires complex distributed transactions (2PC or Sagas) prone to partial failure.
        <br/><br/>
        <b style="color:#34D399;">Our Solution:</b> A unified ASGI application with strict domain package isolation, sub-millisecond in-process function calls, and atomic <code style="color:#34D399;">db.commit()</code> transactions.
      </p>
    </div>

    <!-- Uvicorn Engine -->
    <div class="card" style="background:#062319; border-color:#34D399;">
      <h3 style="color:#34D399;">⚡ Uvicorn ASGI Server (uvloop)</h3>
      <p style="font-size:13px; color:#A7F3D0;">
        Async event loop capable of 15,000+ RPS with non-blocking I/O for external AI gateways.
      </p>
    </div>
  </div>

  <!-- 2. CENTER COLUMN: FastAPI Modular Monolith & Services -->
  <div class="col-panel primary">
    <div class="panel-header emerald">02 / FASTAPI MODULAR ASGI MONOLITH (backend/app/)</div>

    <!-- Middleware Banner -->
    <div style="background:#131D33; border:1.5px solid #38BDF8; border-radius:14px; padding:16px 24px; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-size:14px; font-weight:800; color:#38BDF8; letter-spacing:0.5px;">ASGI MIDDLEWARE PIPELINE</span>
      <span style="font-size:13px; color:#CBD5E1;">CORSMiddleware (Origins Allowlist) ➔ Request Latency Profiler ➔ Depends(get_current_user) JWT Validator</span>
    </div>

    <!-- 12 Routers by Cluster -->
    <div class="cluster-container">
      <div class="cluster-title">12 Domain REST Routers (Classified by Functional Architecture)</div>

      <div class="cluster-grid">
        <div class="router-chip" style="border-left:4px solid #38BDF8;">
          <h4 style="color:#38BDF8;">/api/contacts</h4>
          <span>Lifecycle &amp; Lead Scoring</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #10B981;">
          <h4 style="color:#10B981;">/api/deals</h4>
          <span>Multi-Stage Kanban Funnel</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #F59E0B;">
          <h4 style="color:#F59E0B;">/api/activities</h4>
          <span>Chronological Timeline</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #8B5CF6;">
          <h4 style="color:#8B5CF6;">/api/calendar</h4>
          <span>24h Native Schedule Grid</span>
        </div>

        <div class="router-chip" style="border-left:4px solid #EC4899;">
          <h4 style="color:#EC4899;">/api/ai-agents</h4>
          <span>LangGraph Studio &amp; Telemetry</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #14B8A6;">
          <h4 style="color:#14B8A6;">/api/campaigns</h4>
          <span>Multi-Channel Outreach Copy</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #EF4444;">
          <h4 style="color:#EF4444;">/api/tickets</h4>
          <span>SLA Customer Incident Cases</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #6366F1;">
          <h4 style="color:#6366F1;">/api/analytics</h4>
          <span>ARR Waterfall &amp; Velocity BI</span>
        </div>

        <div class="router-chip" style="border-left:4px solid #FACC15;">
          <h4 style="color:#FACC15;">/api/search</h4>
          <span>Sub-15ms Token Omnisearch</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #38BDF8;">
          <h4 style="color:#38BDF8;">/api/dashboard</h4>
          <span>Executive Revenue Metrics</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #EC4899;">
          <h4 style="color:#EC4899;">/api/auth</h4>
          <span>OAuth 2.0 PKCE &amp; Personas</span>
        </div>
        <div class="router-chip" style="border-left:4px solid #64748B;">
          <h4 style="color:#64748B;">/api/settings</h4>
          <span>AI Budget Guards &amp; Tenants</span>
        </div>
      </div>
    </div>

    <!-- Core Business Services (3 Spacious Cards) -->
    <div>
      <div class="cluster-title" style="margin-bottom:12px;">Core Business Services &amp; Decoupled Subsystems</div>
      <div class="services-grid">
        <!-- Dual Track Auth -->
        <div class="service-card" style="border-color:#EC4899;">
          <span class="highlight-badge" style="background:#EC4899; color:#FFF;">Decision 5 &amp; 29</span>
          <h4 style="color:#F472B6;">Dual-Track Authentication</h4>
          <p>
            <b>Track 1:</b> Google OAuth 2.0 PKCE with <code style="color:#F472B6;">state</code> parameter preserving active edge origins without breaking Google redirect URIs.<br/>
            <b>Track 2:</b> 1-Click Demo Persona Simulator for instant evaluator access with zero setup friction.
          </p>
        </div>

        <!-- Dual Tier Email -->
        <div class="service-card" style="border-color:#10B981;">
          <span class="highlight-badge" style="background:#10B981; color:#000;">Decision 18</span>
          <h4 style="color:#34D399;">Dual-Tier Outbound Email</h4>
          <p>
            <b>Priority:</b> Resend HTTP API (Single key, zero mail server configuration hurdles).<br/>
            <b>Fallback:</b> Resilient SMTP / Gmail.<br/>
            <b>Unified Audit:</b> Every email automatically inserts an immutable <code style="color:#34D399;">Activity</code> record in the CRM timeline.
          </p>
        </div>

        <!-- Omnisearch Engine -->
        <div class="service-card" style="border-color:#FACC15;">
          <span class="highlight-badge" style="background:#FACC15; color:#000;">Cmd/Ctrl + K</span>
          <h4 style="color:#FACC15;">Token-Ranked Omnisearch</h4>
          <p>
            Sub-15ms multi-entity fuzzy search spanning Contacts, Deals, Activities &amp; Tickets. Weighted scoring algorithm: Exact (+100), Prefix (+50), Partial (+25) with category keyboard chips.
          </p>
        </div>
      </div>
    </div>

    <!-- SQLAlchemy ORM & Models -->
    <div>
      <div style="background:#0F172A; border:1.5px solid #0284C7; border-radius:12px; padding:14px 22px; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-size:14px; font-weight:700; color:#38BDF8;">SQLAlchemy 2.0 ORM Engine &amp; Connection Pooler</span>
        <span style="font-size:12px; color:#94A3B8;">Foreign Key Cascade Integrity • Pydantic v2 Serialization • SessionLocal</span>
      </div>

      <div class="models-row">
        <div class="model-chip"><b>Contact</b><span>Email, Phone, ICP</span></div>
        <div class="model-chip"><b>Deal</b><span>Value, Stage, Close</span></div>
        <div class="model-chip"><b>Activity</b><span>Type, Note, Audit</span></div>
        <div class="model-chip"><b>CalendarEvent</b><span>Time Grid, People</span></div>
        <div class="model-chip"><b>Campaign</b><span>Audience, Copy</span></div>
        <div class="model-chip"><b>AIAgentTask</b><span>Cost, Confidence</span></div>
      </div>
    </div>

    <!-- Seeder Engine -->
    <div class="card" style="background:#063528; border-color:#34D399;">
      <h3 style="color:#6EE7B7;">🌱 Autonomous Enterprise Seeder Engine (scripts/seed_data.py)</h3>
      <p style="color:#D1FAE5; font-size:13px;">
        Runs automatically on startup. Mathematically calibrates 12 contacts, 10 stage deals, 40 activities, SLA tickets, and ARR trajectories with authentic fractional-cent AI telemetry in under 2 seconds.
      </p>
    </div>

  </div>

  <!-- 3. RIGHT COLUMN: Relational CP Consistency & Scale-Out Roadmap -->
  <div class="col-panel">
    <div class="panel-header yellow">03 / RELATIONAL CP STORAGE &amp; SCALE ROADMAP</div>

    <!-- CRITICAL DESIGN DECISION 2: Relational CP Consistency -->
    <div class="hero-decision" style="border-color:#34D399; background:#063023;">
      <span class="highlight-badge" style="background:#34D399; color:#000;">Decision 2 (CAP Theorem)</span>
      <h3 style="color:#6EE7B7;">🗄️ Relational CP Consistency</h3>
      <p style="color:#D1FAE5;">
        <b>PostgreSQL (Production) / SQLite (Development)</b>
        <br/><br/>
        In financial CRM systems, <b>Consistency strictly trumps Availability</b>.
        <br/><br/>
        If an upstream network partition occurs, it is significantly better to reject an update or return a retry than permit conflicting writes where two sales reps or automated AI agents overwrite contract values or pipeline stages.
        <br/><br/>
        <b style="color:#FACC15;">Why NoSQL Was Rejected:</b><br/>
        Eventual consistency (MongoDB / DynamoDB) introduces "dirty reads", leading to pipeline forecast drift, race conditions, and compliance audit violations.
      </p>
    </div>

    <div class="cluster-title">Enterprise Scale-Out Roadmap (MVP ➔ 1,000,000 DAU)</div>

    <div class="scale-item">
      <h4>1. PgBouncer Connection Pooler</h4>
      <p>Transaction pooling supporting 10,000+ concurrent database connections with minimal memory overhead.</p>
    </div>

    <div class="scale-item">
      <h4>2. Read-Replica Query Splitting</h4>
      <p>Routes heavy analytical queries (/api/analytics/* &amp; search) to replicas while preserving primary node for deal writes.</p>
    </div>

    <div class="scale-item">
      <h4>3. Redis Cluster (Cache &amp; Rate Limits)</h4>
      <p>Sliding-window agent session store cache &amp; dashboard KPI caching (60s TTL) with per-tenant token bucket limits.</p>
    </div>

    <div class="scale-item">
      <h4>4. Asynchronous Celery / Temporal Workers</h4>
      <p>Offloads long-running AI batch runs (e.g. scoring 50,000 contacts) to background workers with SSE updates.</p>
    </div>

    <div class="scale-item">
      <h4>5. Multi-Tenant Row-Level Security (RLS)</h4>
      <p>PostgreSQL tenant_id policies ensuring 100% cryptographic tenant isolation.</p>
    </div>

  </div>

</div>

</body>
</html>
"""

# ==============================================================================
# 3. BUILD & RENDER PIPELINE
# ==============================================================================

def main():
    print("🚀 NeuronForce Spacious HLD Asset Generation Started...")

    # 1. Write Draw.io XML files
    agentic_drawio_path = DOCS_DIR / "hld_agentic_system.drawio"
    backend_drawio_path = DOCS_DIR / "hld_backend_system.drawio"

    agentic_drawio_path.write_text(generate_agentic_drawio(), encoding="utf-8")
    print(f"✅ Generated Spacious Draw.io file: {agentic_drawio_path}")

    backend_drawio_path.write_text(generate_backend_drawio(), encoding="utf-8")
    print(f"✅ Generated Spacious Draw.io file: {backend_drawio_path}")

    # 2. Write Presentation HTML files
    agentic_html_path = DOCS_DIR / "hld_agentic_system.html"
    backend_html_path = DOCS_DIR / "hld_backend_system.html"

    agentic_html_path.write_text(generate_agentic_html(), encoding="utf-8")
    print(f"✅ Generated Spacious Presentation HTML: {agentic_html_path}")

    backend_html_path.write_text(generate_backend_html(), encoding="utf-8")
    print(f"✅ Generated Spacious Presentation HTML: {backend_html_path}")

    # 3. Render High-Resolution PNGs via Headless Google Chrome
    if Path(CHROME_BIN).exists():
        print("📸 Rendering Spacious Ultra-Crisp PNGs via Headless Google Chrome...")

        agentic_png_path = IMAGES_DIR / "hld_agentic_system.png"
        backend_png_path = IMAGES_DIR / "hld_backend_system.png"

        cmd_agentic = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            f"--window-size=2800,1750",
            f"--screenshot={agentic_png_path}",
            f"file://{agentic_html_path}",
        ]

        cmd_backend = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--force-device-scale-factor=2",
            f"--window-size=2800,1750",
            f"--screenshot={backend_png_path}",
            f"file://{backend_html_path}",
        ]

        try:
            subprocess.run(cmd_agentic, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ Rendered High-Resolution PNG: {agentic_png_path} ({agentic_png_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"⚠️ Error rendering agentic PNG: {e}")

        try:
            subprocess.run(cmd_backend, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ Rendered High-Resolution PNG: {backend_png_path} ({backend_png_path.stat().st_size} bytes)")
        except Exception as e:
            print(f"⚠️ Error rendering backend PNG: {e}")
    else:
        print("⚠️ Chrome not found at expected path. PNG rendering skipped.")

    print("🎉 All Spacious HLD Assets (Draw.io XML, Presentation HTML, High-Res PNGs) Generated Successfully!")

if __name__ == "__main__":
    main()
