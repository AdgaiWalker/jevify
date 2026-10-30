"""
TypeSafe AI Jev Python Client (Zero Dependencies)
A typed, high-efficiency client for System One non-autoregressive decision models.
Compatible with Python 3.8+, using only standard library urllib.
"""

import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass


@dataclass
class Question:
    type: str
    instructions: str
    criteria: Optional[Union[Dict[str, str], List[str]]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "type": self.type,
            "instructions": self.instructions
        }
        if self.criteria is not None:
            payload["criteria"] = self.criteria
        return payload


def Choice(instructions: str, criteria: Dict[str, str]) -> Question:
    """Creates a categorical choice question (up to 255 named options)."""
    return Question(type="choice", instructions=instructions, criteria=criteria)


def Score(instructions: str, criteria: List[str]) -> Question:
    """Creates an ordered rubric score question (2-10 levels)."""
    return Question(type="score", instructions=instructions, criteria=criteria)


def Noul(instructions: str) -> Question:
    """Creates a boolean / calibrated probability check question."""
    return Question(type="noul", instructions=instructions)


class JevClient:
    def __init__(
        self,
        api_key: str,
        endpoint: str = "https://api.typesafe.ai/v1/systemone",
        timeout: float = 3.5
    ):
        self.api_key = api_key.strip() if api_key else ""
        self.endpoint = endpoint
        self.timeout = timeout

    def is_enabled(self) -> bool:
        return bool(self.api_key)

    def decide(
        self,
        state: Union[str, Dict[str, Any]],
        questions: Dict[str, Question],
        model: str = "jev-latest"
    ) -> Optional[Dict[str, Any]]:
        """
        Sends a single parallel-pass evaluation request to JEV System One.
        Fail-open: returns None on timeout or error to keep host application running.
        """
        if not self.is_enabled():
            return None

        state_str = json.dumps(state) if isinstance(state, (dict, list)) else str(state)
        questions_dict = {
            k: (v.to_dict() if isinstance(v, Question) else v)
            for k, v in questions.items()
        }

        payload = {
            "model": model,
            "state": state_str,
            "questions": questions_dict
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "TypeSafe-JevClient-PY/1.14.0"
            },
            method="POST"
        )

        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                elapsed_ms = (time.time() - t0) * 1000
                res = json.loads(resp.read().decode("utf-8"))
                res["_latency_ms"] = elapsed_ms
                return res
        except Exception:
            # Fail-open: fail gracefully on network timeout
            return None
