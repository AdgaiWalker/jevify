# Agent-Reflex ⚡️
### The Sub-100ms System-1 Spinal Cord for Autonomous AI Agents

> **"Your AI Agent doesn't need a bigger brain to stop doing stupid things in production. It needs a spinal cord."**

---

## 📌 The Problem (Late 2026 Reality)

In late 2026, autonomous coding agents (Claude Code, Cursor Agent, Devin, Aider, custom LangGraph swarms) have graduated from cute demos to production infrastructure. But when running multi-step autonomous loops in live terminals and codebases, every engineering team hits the same three catastrophic walls:

1. **The Stagnation Loop Trap**: An agent encounters a build/import error and repeats the exact same doomed command 8 times with tiny cosmetic variations (e.g. `pip install pkg` -> `pip install pkg --no-cache` -> `pip install pkg==1.0`), burning $5 in tokens before timing out.
2. **The Brittle Regex Fallacy**: Teams try to guard terminal execution with keyword blacklists (`rm -rf`, `DROP TABLE`). A stray prompt injection, alias, or base64 flag bypasses it instantly. Meanwhile, using a 70B LLM to review every shell command introduces 2–3 seconds of latency per keystroke.
3. **The "Fake Done" Hallucination**: The agent claims *"I have resolved the issue and the system is ready to ship!"* when it merely touched an irrelevant comment and never executed the test suite.

---

## 💡 The Solution: Dual-System Reflex Architecture

In human biology, the brain (System 2) plans complex chess moves, but the **spinal cord (System 1)** pulls your hand away from a hot stove in 40ms without waiting for cortical cognition.

**Agent-Reflex** is a lightweight, drop-in runtime middleware powered by **TypeSafe AI JEV** (`jev-1.14.0`). It operates non-autoregressively in sub-100ms to enforce semantic invariants before commands touch your OS.

```
       [ User Objective: "Fix production DB connection timeout" ]
                                  │
                                  ▼
      🧠 System 2 (Claude 3.5 Sonnet / o1 / DeepSeek-R1)
          └─ Planning & Code Generation (3,000 ~ 10,000 ms)
                                  │
                       [ Proposed Tool Action ]
                                  │
                                  ▼
      ⚡️ Agent-Reflex Sentry (JEV Non-Autoregressive - ~50 ms)
       ├── 1. Physical Destructive Risk Gate (Noul) ──> Block dangerous actions
       ├── 2. Stagnation / Loop Detector (Score) ────> Shatter dead loops
       └── 3. Fake-Done Truth Verifier (Choice) ──────> Reject untested completion
                                  │
                        [ Safe & Verified ]
                                  │
                                  ▼
              💻 Execution Environment (Bash / OS / DB)
```

---

## 🚀 Quickstart

### 1. Install
```bash
pip install agent-reflex
```

### 2. Wrap Any Agent Tool Loop in 3 Lines
```python
from agent_reflex import ReflexSentry

# Initialize the sentry (uses JEV System-1 non-autoregressive backend)
sentry = ReflexSentry(api_key="your_typesafe_key")

# Intercept tool calls before execution
verdict = sentry.intercept_tool(
    objective="Update dependencies and restart service",
    tool_name="run_bash",
    tool_args={"command": "rm -rf /var/cache/* /etc/systemd/*"},
    step_history=agent_history
)

if not verdict.allowed:
    # Sub-100ms physical intervention!
    print(f"🚨 Blocked: {verdict.reason}")
    agent.inject_error_correction(verdict.suggested_correction)
else:
    execute_tool()
```

### 3. Verify Completion Before Exiting
```python
verdict = sentry.verify_completion(
    objective="Fix ZeroDivisionError in invoice_calculator.py",
    claimed_summary=agent.last_message,
    execution_evidence={
        "tests_executed": False,  # Agent forgot to run tests!
        "tests_passed": False,
        "git_diff": git_diff_output
    }
)

if not verdict.verified:
    # Forces the agent back to work!
    agent.continue_execution(verdict.feedback)
```

---

## 📊 Live Verification Benchmarks (Oct 2026 Live API)

| Interception Scenario | Traditional LLM-as-a-Judge | Agent-Reflex (JEV System 1) | Improvement |
| :--- | :--- | :--- | :--- |
| **Destructive Command Gate** | 2,850 ms / $0.015 | **68 ms / $0.0001** | **42x Faster, 99.3% Cheaper** |
| **Dead Loop Detection** | Fails after 10 turns ($3.50) | **Intercepts at Step 2 ($0.0002)** | **Saved 80% Token Waste** |
| **Untested Fake-Done** | 2,400 ms (often hallucinated) | **72 ms (100% Typed Confidence)** | **Deterministic Safety** |

---

## 🛠️ Verification Demo
Run the included live benchmark suite against the real JEV API:
```bash
python3 demo_agent_reflex.py
```
Outputs:
```text
⚡️ SCENARIO 1: Destructive Command Interception (50ms Physical Guard)
   🚨 Destructive action blocked! Physical safety probability check failed (destructive_prob=0.98).
   ✅ TEST 1 PASSED in sub-100ms.

⚡️ SCENARIO 2: Agent Loop / Stagnation Breaker (Score-based Reflex)
   🛑 Loop/Stagnation detected! Agent is trapped repeating failing actions (progress_score=0.94/3.0).
   💡 Forced Agent Correction: You are repeating an approach that has already failed.
   ✅ TEST 2 PASSED.

⚡️ SCENARIO 3: Fake Done / Hallucinated Completion Rejection
   🚨 Rejection: Cannot exit task. Status is 'fake_done_untested' (confidence=1.00).
   ✅ TEST 3 PASSED.
```

---

## License
MIT. Built with ❤️ for the 2026 Autonomous Agent Ecosystem.
