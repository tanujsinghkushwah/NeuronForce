"""
NeuronForce Autonomous Agent Evaluation Suite Runner
Executes 15 benchmark scenarios through the LangGraph Orchestrator,
evaluates precision, graph step consistency, entity extraction, and latency,
and produces comprehensive test telemetry.
"""

import sys
import os
import time
import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

# Ensure repository paths are configured
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.orchestrator import run_agent_orchestrator
from agents.evals.dataset import EVAL_SCENARIOS, EvalScenario


@dataclass
class EvalResult:
    scenario_id: str
    name: str
    category: str
    passed: bool
    intent_match: bool
    action_type_match: bool
    subagent_match: bool
    graph_steps_present: bool
    confidence_ok: bool
    keywords_ok: bool
    latency_ms: int
    errors: List[str] = field(default_factory=list)
    executed_steps: List[str] = field(default_factory=list)
    reply_preview: str = ""


@dataclass
class EvalReport:
    total_scenarios: int
    passed_scenarios: int
    failed_scenarios: int
    accuracy_pct: float
    intent_accuracy_pct: float
    action_accuracy_pct: float
    subagent_accuracy_pct: float
    graph_consistency_pct: float
    latency_avg_ms: float
    latency_p95_ms: float
    results: List[EvalResult] = field(default_factory=list)


def run_eval_scenario(scenario: EvalScenario) -> EvalResult:
    """
    Execute a single evaluation scenario against the LangGraph orchestrator.
    """
    start_time = time.time()
    errors: List[str] = []

    try:
        res = run_agent_orchestrator(
            prompt=scenario.prompt,
            session_id=f"eval_sess_{scenario.id}",
        )
    except Exception as e:
        latency = int((time.time() - start_time) * 1000)
        return EvalResult(
            scenario_id=scenario.id,
            name=scenario.name,
            category=scenario.category,
            passed=False,
            intent_match=False,
            action_type_match=False,
            subagent_match=False,
            graph_steps_present=False,
            confidence_ok=False,
            keywords_ok=False,
            latency_ms=latency,
            errors=[f"Exception during execution: {str(e)}"],
            executed_steps=[],
            reply_preview="",
        )

    latency = int((time.time() - start_time) * 1000)
    actual_intent = res.get("intent")
    actual_action = res.get("action_type")
    actual_subagent = res.get("target_subagent")
    actual_reply = str(res.get("reply") or "")
    actual_confidence = float(res.get("confidence_score") or 0.0)
    graph_steps = res.get("graph_steps", [])
    step_nodes = [s.get("node") for s in graph_steps]

    # 1. Intent Validation
    if scenario.expected_intent == "compound":
        intent_match = actual_intent == "compound" or (
            bool(actual_action) and bool(actual_subagent)
        )
    else:
        intent_match = actual_intent == scenario.expected_intent

    if not intent_match:
        errors.append(
            f"Intent mismatch: expected '{scenario.expected_intent}', got '{actual_intent}'"
        )

    # 2. Action Type Validation
    if scenario.expected_action_type is not None:
        action_match = actual_action == scenario.expected_action_type
        if not action_match:
            errors.append(
                f"Action mismatch: expected '{scenario.expected_action_type}', got '{actual_action}'"
            )
    else:
        action_match = actual_action is None or scenario.expected_intent == "general"

    # 3. Target Subagent Validation
    if scenario.expected_subagent is not None:
        subagent_match = actual_subagent == scenario.expected_subagent
        if not subagent_match:
            errors.append(
                f"Subagent mismatch: expected '{scenario.expected_subagent}', got '{actual_subagent}'"
            )
    else:
        subagent_match = (
            actual_subagent is None or scenario.expected_intent == "general"
        )

    # 4. Graph Steps Validation
    missing_steps = [req for req in scenario.required_steps if req not in step_nodes]
    graph_steps_present = len(missing_steps) == 0
    if not graph_steps_present:
        errors.append(
            f"Missing required graph steps: {missing_steps}. Executed: {step_nodes}"
        )

    # 5. Confidence Validation
    confidence_ok = actual_confidence >= (scenario.min_confidence - 0.05)
    if not confidence_ok:
        errors.append(
            f"Low confidence: {actual_confidence} < {scenario.min_confidence}"
        )

    # 6. Keywords Validation
    keywords_ok = True
    for kw in scenario.expected_reply_keywords:
        if kw.lower() not in actual_reply.lower():
            # Check if keyword might be in subagent_result
            sub_res_str = json.dumps(res.get("subagent_result") or {})
            tool_res_str = json.dumps(res.get("tool_result") or {})
            if (
                kw.lower() not in sub_res_str.lower()
                and kw.lower() not in tool_res_str.lower()
            ):
                keywords_ok = False
                errors.append(
                    f"Expected keyword '{kw}' missing from reply and payloads"
                )
                break

    passed = (
        intent_match
        and action_match
        and subagent_match
        and graph_steps_present
        and confidence_ok
        and keywords_ok
    )

    return EvalResult(
        scenario_id=scenario.id,
        name=scenario.name,
        category=scenario.category,
        passed=passed,
        intent_match=intent_match,
        action_type_match=action_match,
        subagent_match=subagent_match,
        graph_steps_present=graph_steps_present,
        confidence_ok=confidence_ok,
        keywords_ok=keywords_ok,
        latency_ms=latency,
        errors=errors,
        executed_steps=step_nodes,
        reply_preview=actual_reply[:140].replace("\n", " "),
    )


def run_all_evals(
    scenarios: Optional[List[EvalScenario]] = None,
    verbose: bool = True,
    output_json: Optional[str] = None,
) -> EvalReport:
    """
    Run all evaluation scenarios and compile summary telemetry.
    """
    eval_list = scenarios or EVAL_SCENARIOS
    results: List[EvalResult] = []

    if verbose:
        print("\n" + "=" * 90)
        print("🚀 NEURONFORCE AUTONOMOUS MULTI-AGENT EVALUATION SUITE")
        print(f"Targeting: 15 Diverse Scenarios (LangGraph Orchestration & Sub-Agents)")
        print("=" * 90 + "\n")

    for idx, sc in enumerate(eval_list, 1):
        if verbose:
            print(
                f"[{idx:02d}/15] Running: {sc.name} ({sc.category})...",
                end="",
                flush=True,
            )

        res = run_eval_scenario(sc)
        results.append(res)

        if verbose:
            if res.passed:
                print(f" ✅ PASS ({res.latency_ms}ms)")
            else:
                print(f" ❌ FAIL ({res.latency_ms}ms)")
                for err in res.errors:
                    print(f"     ↳ [!] {err}")

    # Metrics calculation
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    accuracy = round((passed / total) * 100, 2) if total else 0.0
    intent_acc = (
        round((sum(1 for r in results if r.intent_match) / total) * 100, 2)
        if total
        else 0.0
    )
    action_acc = (
        round((sum(1 for r in results if r.action_type_match) / total) * 100, 2)
        if total
        else 0.0
    )
    subagent_acc = (
        round((sum(1 for r in results if r.subagent_match) / total) * 100, 2)
        if total
        else 0.0
    )
    graph_consistency = (
        round((sum(1 for r in results if r.graph_steps_present) / total) * 100, 2)
        if total
        else 0.0
    )

    latencies = sorted(r.latency_ms for r in results)
    avg_latency = round(sum(latencies) / total, 1) if total else 0.0
    p95_idx = int(0.95 * total) - 1 if total else 0
    p95_latency = float(latencies[max(0, p95_idx)]) if total else 0.0

    report = EvalReport(
        total_scenarios=total,
        passed_scenarios=passed,
        failed_scenarios=failed,
        accuracy_pct=accuracy,
        intent_accuracy_pct=intent_acc,
        action_accuracy_pct=action_acc,
        subagent_accuracy_pct=subagent_acc,
        graph_consistency_pct=graph_consistency,
        latency_avg_ms=avg_latency,
        latency_p95_ms=p95_latency,
        results=results,
    )

    if verbose:
        print("\n" + "=" * 90)
        print("📊 EVALUATION RESULTS SUMMARY")
        print("=" * 90)
        print(
            f"  • Overall Success Rate:          {report.accuracy_pct}% ({report.passed_scenarios}/{report.total_scenarios} passed)"
        )
        print(f"  • Intent Routing Accuracy:       {report.intent_accuracy_pct}%")
        print(f"  • CRM Action Accuracy:           {report.action_accuracy_pct}%")
        print(f"  • Specialist Sub-Agent Accuracy: {report.subagent_accuracy_pct}%")
        print(f"  • Graph Step Consistency:        {report.graph_consistency_pct}%")
        print(
            f"  • Latency Distribution:          Average {report.latency_avg_ms}ms | p95 {report.latency_p95_ms}ms"
        )
        print("=" * 90 + "\n")

    if output_json:
        out_path = Path(output_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(asdict(report), f, indent=2)
        if verbose:
            print(f"📄 Full JSON evaluation report saved to: {out_path}\n")

    return report


if __name__ == "__main__":
    report_file = REPO_ROOT / "agents" / "evals" / "eval_report.json"
    report = run_all_evals(output_json=str(report_file))
    sys.exit(0 if report.failed_scenarios == 0 else 1)
