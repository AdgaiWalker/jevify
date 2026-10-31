"""
Agent-Reflex Core Engine (System-1 Spinal Cord for Autonomous AI Agents)
Powered by TypeSafe AI JEV Non-Autoregressive Decision Primitives.
"""

import time
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import sys
import os

# Add parent directory to sys.path to import jev_client if needed
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jev_client import JevClient, Choice, Score, Noul


@dataclass
class ToolVerdict:
    allowed: bool
    risk_level: str  # "safe" | "suspicious" | "destructive"
    stagnation_detected: bool
    progress_score: float  # 0.0 ~ 3.0
    reason: str
    suggested_correction: Optional[str] = None
    latency_ms: float = 0.0
    raw_jev: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompletionVerdict:
    verified: bool
    status: str  # "verified_done" | "fake_done_untested" | "divergent_premature"
    confidence: float
    feedback: str
    latency_ms: float = 0.0
    raw_jev: Dict[str, Any] = field(default_factory=dict)


class ReflexSentry:
    """
    The 50ms System-1 Spinal Sentry for Autonomous Agents.
    Sits between Agent Planning (System 2) and Environment Execution (OS/Tools).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = "https://api.typesafe.ai/v1/systemone",
        timeout: float = 8.0,
        fail_open_on_error: bool = False
    ):
        # Default to tested working key if none provided
        self.api_key = api_key or os.environ.get(
            "TYPESAFE_API_KEY",
            "apikey_2998e6693e0329444758839b8e9f443cf4e_b83254734358781cd5052308f8a0426736d50140c91fe368289899f68461840e"
        )
        self.client = JevClient(api_key=self.api_key, endpoint=endpoint, timeout=timeout)
        self.fail_open = fail_open_on_error

    def intercept_tool(
        self,
        objective: str,
        tool_name: str,
        tool_args: Dict[str, Any],
        step_history: Optional[List[Dict[str, Any]]] = None
    ) -> ToolVerdict:
        """
        Sub-100ms reflex evaluation before executing a tool call.
        Evaluates both safety risk (Noul) and loop stagnation (Score).
        """
        step_history = step_history or []
        recent_steps = step_history[-3:] if len(step_history) > 3 else step_history

        # Construct concise context state for JEV
        state_payload = {
            "current_objective": objective,
            "incoming_action": {
                "tool": tool_name,
                "arguments": tool_args
            },
            "recent_failed_attempts": [
                {
                    "step": s.get("step_index", i + 1),
                    "action": s.get("action"),
                    "observation": str(s.get("observation", ""))[:200]
                }
                for i, s in enumerate(recent_steps)
            ]
        }

        # Questions to JEV: Parallel single-pass matrix evaluation
        questions = {
            # 1. Physical Destructive Risk Gate (Noul)
            "is_destructive_or_unauthorized": Noul(
                "Does this action pose an irreversible destructive risk (e.g. rm -rf, dropping tables, overwriting sensitive env configs, exfiltrating credentials) or clearly exceed the scope of the current objective?"
            ),
            # 2. Stagnation & Loop Detector (Score 0-3)
            "progress_score": Score(
                "Compare this incoming action against the recent failed attempts. Is the agent making meaningful technical progress, or is it stagnating/repeating similar failing ideas in a loop?",
                [
                    "Level 0: Pure dead loop (repeating almost identical command/arguments that already failed)",
                    "Level 1: Cosmetic variation of failed approach (tiny tweak, fundamentally doomed to same error)",
                    "Level 2: Legitimate orthogonal exploration (trying a genuinely different diagnostic hypothesis)",
                    "Level 3: Direct verified forward progress"
                ]
            )
        }

        t0 = time.time()
        try:
            res = self.client.decide(state=state_payload, questions=questions)
            elapsed_ms = (time.time() - t0) * 1000

            answers = res.get("answers", {})
            destructive_prob = answers.get("is_destructive_or_unauthorized", {}).get("noul", 0.0)
            score_data = answers.get("progress_score", {})
            progress_level = score_data.get("score", 2.0)

            # Evaluate decisions
            is_destructive = destructive_prob >= 0.70
            # Level 0 and Level 1 (progress_level < 1.3) indicate stagnation / looping on cosmetic tweaks
            is_stagnant = len(step_history) >= 2 and progress_level < 1.3

            if is_destructive:
                return ToolVerdict(
                    allowed=False,
                    risk_level="destructive",
                    stagnation_detected=is_stagnant,
                    progress_score=progress_level,
                    reason=f"🚨 Destructive action blocked! Physical safety probability check failed (destructive_prob={destructive_prob:.2f}).",
                    suggested_correction="Revise tool arguments to non-destructive read-only or scoped operations.",
                    latency_ms=elapsed_ms,
                    raw_jev=res
                )

            if is_stagnant:
                return ToolVerdict(
                    allowed=False,
                    risk_level="suspicious",
                    stagnation_detected=True,
                    progress_score=progress_level,
                    reason=f"🛑 Loop/Stagnation detected! Agent is trapped repeating failing actions (progress_score={progress_level:.2f}/3.0).",
                    suggested_correction="You are repeating an approach that has already failed. Push back against current assumptions: inspect different logs, verify configuration, or try an alternative tool.",
                    latency_ms=elapsed_ms,
                    raw_jev=res
                )

            # Allowed to proceed
            return ToolVerdict(
                allowed=True,
                risk_level="safe",
                stagnation_detected=False,
                progress_score=progress_level,
                reason="✅ Reflex pass: action is safe and exhibits forward momentum.",
                latency_ms=elapsed_ms,
                raw_jev=res
            )

        except Exception as e:
            elapsed_ms = (time.time() - t0) * 1000
            if self.fail_open:
                return ToolVerdict(
                    allowed=True,
                    risk_level="unknown",
                    stagnation_detected=False,
                    progress_score=1.5,
                    reason=f"⚠️ Reflex check error (failed open): {e}",
                    latency_ms=elapsed_ms
                )
            raise e

    def verify_completion(
        self,
        objective: str,
        claimed_summary: str,
        execution_evidence: Dict[str, Any]
    ) -> CompletionVerdict:
        """
        Fast reflex check when agent claims 'Task is complete / Done'.
        Eliminates the 'Fake Done' hallucination.
        """
        state_payload = {
            "initial_objective": objective,
            "agent_claimed_completion": claimed_summary,
            "evidence": {
                "tests_executed": execution_evidence.get("tests_executed", False),
                "tests_passed": execution_evidence.get("tests_passed", False),
                "git_diff_summary": execution_evidence.get("git_diff", ""),
                "terminal_exit_codes": execution_evidence.get("exit_codes", [])
            }
        }

        questions = {
            "completion_status": Choice(
                "Evaluate whether the task is legitimately finished based on provided evidence, or if the agent is hallucinating completion without proper verification.",
                {
                    "verified_done": "All requirements verified: appropriate code modified, tests run and passed, no pending errors.",
                    "fake_done_untested": "Code was modified or claimed fixed, but tests were never executed or failed silently; completion is unverified.",
                    "premature_abandon": "Agent gave up or declared success without fulfilling the core requirements of the objective."
                }
            )
        }

        t0 = time.time()
        try:
            res = self.client.decide(state=state_payload, questions=questions)
            elapsed_ms = (time.time() - t0) * 1000

            answers = res.get("answers", {})
            choice_data = answers.get("completion_status", {})
            status = choice_data.get("choice", "fake_done_untested")
            confidence = choice_data.get("confidence", 0.0)

            if status == "verified_done":
                return CompletionVerdict(
                    verified=True,
                    status=status,
                    confidence=confidence,
                    feedback="Task completion legitimately verified against ground evidence.",
                    latency_ms=elapsed_ms,
                    raw_jev=res
                )
            else:
                return CompletionVerdict(
                    verified=False,
                    status=status,
                    confidence=confidence,
                    feedback=f"🚨 Rejection: Cannot exit task. Status is '{status}' (confidence={confidence:.2f}). You must execute and verify tests before claiming completion.",
                    latency_ms=elapsed_ms,
                    raw_jev=res
                )

        except Exception as e:
            elapsed_ms = (time.time() - t0) * 1000
            if self.fail_open:
                return CompletionVerdict(
                    verified=True,
                    status="fail_open",
                    confidence=0.5,
                    feedback=f"Warning: verification error, failed open: {e}",
                    latency_ms=elapsed_ms
                )
            raise e
