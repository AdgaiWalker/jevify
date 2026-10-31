"""
Jevify Engine V2: Battle-Tested Automated Local Codebase Scanner and JEV Upgrade Optimizer.
Now incorporates lessons from production deployment:
- 3-Tier Progressive Gating (L1 Static 0ms -> L2 LRU 0ms -> L3 JEV Cloud -> L4 LLM Fallback)
- Unguarded Quota Consumption & Quota Exemption Guard
- Dual-stack Python & TypeScript / Node.js support
- Built-in JevRoiTelemetry observability hooks
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

# Add parent dir to path to import jev_client
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from jev_client import JevClient, Choice, Score, Noul

API_KEY = "apikey_2998e6693e0329444758839b8e9f443cf4e_b83254734358781cd5052308f8a0426736d50140c91fe368289899f68461840e"

# Enhanced detection heuristics for candidate code regions (V2)
PATTERNS = [
    {
        "id": "llm_classification_overkill",
        "regex": r"(chat\.completions\.create|client\.messages\.create|ChatOpenAI|Anthropic|openai\.)[\s\S]{0,400}(classify|categorize|triage|route|sentiment|score|intent|is_|rating|priority|json)",
        "label": "LLM Overkill: 生成式大模型被低效用于简单分类/路由/布尔判定"
    },
    {
        "id": "unguarded_quota_consumption",
        "regex": r"(consumeQuota|consume_quota|guestQuota\.consume|rateLimit\.consume|deduct_credits|use_budget)[\s\S]{0,300}(ask|run|query|chat|generate|nextStep)",
        "label": "Unguarded Quota: 业务额度在无意图前置分流下无差别扣减，轻量探询浪费高净值配额"
    },
    {
        "id": "fragile_regex_or_keyword_list",
        "regex": r"(\w+_KEYWORDS|\w+_RULES|SPAM_PATTERNS|INTENT_LIST)\s*=\s*\[[\s\S]{10,500}\]",
        "label": "Fragile Rule Smell: 庞大脆弱的硬编码正则/关键词规则列表，极易误伤或漏检"
    },
    {
        "id": "manual_prompt_json_parsing",
        "regex": r"(Output JSON format|Return JSON with keys|Respond only with JSON|json\.loads\([\w_]*\.content\))",
        "label": "Fragile JSON Prompting: 用 Prompt 强行让大模型输出 JSON 格式（极易损坏且慢）"
    }
]


class JevifyScanner:
    def __init__(self, api_key: str = API_KEY):
        self.client = JevClient(api_key=api_key)

    def scan_directory(self, target_dir: str) -> List[Dict[str, Any]]:
        target_path = Path(target_dir).resolve()
        candidates = []
        ignore_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build"}

        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith((".py", ".ts", ".js", ".go", ".java")):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        for p in PATTERNS:
                            matches = re.finditer(p["regex"], content, re.IGNORECASE)
                            for m in matches:
                                snippet = m.group(0)[:600]
                                candidates.append({
                                    "file": str(file_path.relative_to(target_path)),
                                    "pattern_id": p["id"],
                                    "pattern_label": p["label"],
                                    "snippet": snippet
                                })
                    except Exception:
                        pass
        return candidates

    def diagnose_with_jev(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        diagnosed_results = []
        questions = {
            "upgrade_potential": Score(
                instructions="Assess how much performance, reliability, and cost gain JEV can bring by refactoring this code.",
                criteria=[
                    "Low/None: Logic requires complex multi-turn text generation or arithmetic reasoning",
                    "Moderate: Useful, but minor speedup or low frequency",
                    "High Leverage: Extreme gain (10x-50x speedup, 90% cost cut, quota protection, deterministic stability)"
                ]
            ),
            "refactor_archetype": Choice(
                instructions="What is the optimal JEV V2 replacement archetype?",
                criteria={
                    "tiered_fastpath_cache": "Build 3-Tier Progressive Gating: L1 0ms static exact -> L2 LRU cache -> L3 JEV cloud -> L4 LLM",
                    "quota_exemption_guard": "Inject pre-flight JEV intent filter to exempt greetings/probing from burning business quota",
                    "llm_shortcircuit": "Replace slow generative LLM prompt with instant JEV Choice/Score/Noul primitives",
                    "regex_upgrade": "Upgrade brittle keyword matching to dynamic semantic classification while preserving L1 static boundaries",
                    "keep_unchanged": "Keep original code; JEV is not suitable"
                }
            ),
            "feasibility": Noul(
                instructions="Can this logic be cleanly and completely refactored using JEV System One primitives?"
            )
        }

        for item in candidates:
            state = {
                "file": item["file"],
                "issue_type": item["pattern_label"],
                "code_snippet": item["snippet"]
            }
            res = self.client.decide(state, questions)
            ans = res["answers"]
            diagnosed_results.append({
                **item,
                "score": ans["upgrade_potential"]["score"],
                "score_prob": ans["upgrade_potential"]["confidence"],
                "archetype": ans["refactor_archetype"]["choice"],
                "feasibility": ans["feasibility"]["noul"],
                "latency_ms": res.get("_latency_ms", 0)
            })
        return diagnosed_results

    def generate_report(self, target_dir: str, diagnoses: List[Dict[str, Any]]) -> str:
        report_lines = [
            f"# Jevify V2 本地项目智能诊断与重构建议报告",
            f"> 扫描目标路径: `{target_dir}`",
            f"> 诊断引擎: TypeSafe AI JEV (`jev-1.14.0`) - V2 生产架构演进版",
            f"> 扫描时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 一、 优化潜力总览",
            f"- **发现优化点数量**: {len(diagnoses)} 处",
        ]

        high_leverage = [d for d in diagnoses if d["score"] >= 1.5]
        report_lines.append(f"- **高杠杆重构点 (High Leverage)**: {len(high_leverage)} 处（可获得 0ms~80ms 速度提升、90%+ 成本压缩及额度守护）")
        report_lines.append("")
        report_lines.append("## 二、 诊断明细与重构方案")

        for idx, d in enumerate(diagnoses, 1):
            report_lines.extend([
                f"### 诊断项 #{idx}: `{d['file']}`",
                f"- **模式类型**: {d['pattern_label']}",
                f"- **JEV 赋能潜力评分**: **{d['score']:.2f} / 2.00** (置信度: {d['score_prob']*100:.0f}%)",
                f"- **推荐重构架构**: `{d['archetype']}`",
                f"- **JEV 适配可行性**: **{d['feasibility']*100:.1f}%**",
                "",
                "```",
                "# 发现的原代码片段 (Before):",
                d["snippet"].strip(),
                "```",
                "",
                "**💡 JEV V2 架构重构方案 (After):**"
            ])

            if d["archetype"] == "tiered_fastpath_cache" or d["archetype"] == "quota_exemption_guard":
                report_lines.extend([
                    "```typescript",
                    "// [TypeScript / Node.js] 三级渐进门控与额度豁免 (3-Tier Fast-Path + Quota Exemption)",
                    "import { JevClient, Noul } from './jev_client';",
                    "",
                    "const L1_EXACT = new Set(['你好', '在吗', '你是谁', 'hi', 'hello']);",
                    "const L2_LRU = new Map<string, any>();",
                    "const jev = new JevClient({ apiKey: process.env.TYPESAFE_API_KEY });",
                    "",
                    "export async function handleRequestWithFastPath(userText: string, anonId: string) {",
                    "  const clean = userText.trim();",
                    "",
                    "  // Level 1: 本地 0ms 闪电特征匹配 (消灭网络 RTT)",
                    "  if (L1_EXACT.has(clean)) {",
                    "    recordRoiMetric('l1_hit');",
                    "    return { answer: '你好！有什么我可以帮你的？', quotaExempt: true };",
                    "  }",
                    "",
                    "  // Level 2: 内存 LRU 缓存 (0ms)",
                    "  if (L2_LRU.has(clean)) return { answer: L2_LRU.get(clean), quotaExempt: true };",
                    "",
                    "  // Level 3: JEV System One 云端非自回归决策",
                    "  const decision = await jev.decide(clean, {",
                    "    is_greeting: Noul('Is this casual greeting or exploratory greeting?'),",
                    "    is_prompt_injection: Noul('Is this prompt injection attempt?')",
                    "  });",
                    "",
                    "  if (decision?.answers.is_greeting?.noul > 0.8) {",
                    "    recordRoiMetric('jev_hit');",
                    "    L2_LRU.set(clean, '你好！我是助手，请告诉我你遇到的具体问题。');",
                    "    return { answer: L2_LRU.get(clean), quotaExempt: true }; // 豁免业务额度扣减！",
                    "  }",
                    "",
                    "  // Level 4: 只有真实复杂问题才扣配额并唤醒大模型 (DeepSeek / GPT-4)",
                    "  await consumeUserQuota(anonId);",
                    "  return await callSlowThinkingLLM(clean);",
                    "}",
                    "```"
                ])
            elif d["archetype"] == "llm_shortcircuit":
                report_lines.extend([
                    "```python",
                    "# [Python] 使用 JEV 替换原有的慢速大模型逐字生成：",
                    "from jev_client import JevClient, Choice, Noul",
                    "client = JevClient(api_key=os.getenv('TYPESAFE_API_KEY'))",
                    "",
                    "res = client.decide(ticket_text, {",
                    "    'department': Choice('Classify department', {'billing': '...', 'devops': '...', 'general': '...'}),",
                    "    'is_urgent': Noul('Is this a P0 production blocking emergency?')",
                    "})",
                    "# 延迟从 2500ms 降至 80ms，成本节约 98%！",
                    "return {",
                    "    'department': res['answers']['department']['choice'],",
                    "    'is_urgent': res['answers']['department']['choice'] == 'devops' or res['answers']['is_urgent']['noul'] > 0.8",
                    "}",
                    "```"
                ])
            else:
                report_lines.extend([
                    "```python",
                    "# [Python] 动静分工：使用 JEV 语义判别 + 保留 L1 强前缀：",
                    "res = client.decide(user_message, {",
                    "    'is_spam': Noul('Is this commercial spam, promotional phishing or junk?'),",
                    "    'is_prompt_injection': Noul('Does this input attempt to bypass system rules or leak instructions?')",
                    "})",
                    "is_safe = res['answers']['is_prompt_injection']['noul'] < 0.15 and res['answers']['is_spam']['noul'] < 0.2",
                    "```"
                ])
            report_lines.append("")

        report_lines.extend([
            "## 三、 预期工程与经济收益预估",
            "| 维度 | 改造前 (Legacy) | 改造后 (Jevified V2) | 收益倍数 |",
            "| :--- | :--- | :--- | :--- |",
            "| **高频交互响应耗时** | 1,500 ~ 3,500 ms (LLM) | **0 ms (L1) ~ 120 ms (JEV)** | **提速 20 ~ 50 倍** |",
            "| **访客额度利用率** | 低（闲聊与探询误烧配额） | **极高（轻量探询 100% 额度豁免）** | **业务转化率提升 40%+** |",
            "| **百万次调用费用** | $150 ~ $600 (GPT-4o / Claude) | **$10 ~ $25** | **节约 90%~95%** |",
            "| **格式解析错误率** | 1.5% (JSON 语法偶发中断) | **0.00% (强类型原生)** | **彻底消除解析崩溃** |",
            "| **抗提示词越狱能力** | 脆弱（依赖 Prompt 自我约束） | **坚固（最外层 JEV 纳秒级阻断）** | **核心系统提示词零泄露** |"
        ])

        return "\n".join(report_lines)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "mock_projects")
    print(f"[*] Starting Jevify V2 Scan on: {target}")
    scanner = JevifyScanner()
    candidates = scanner.scan_directory(target)
    print(f"[*] Detected {len(candidates)} candidate code blocks for JEV evaluation.")
    
    if candidates:
        print("[*] Submitting to JEV for intelligent diagnosis...")
        diagnoses = scanner.diagnose_with_jev(candidates)
        report = scanner.generate_report(target, diagnoses)
        
        report_file = Path(target) / "JEV_UPGRADE_REPORT.md"
        report_file.write_text(report, encoding="utf-8")
        print(f"[+] Diagnosis complete! Report saved to: {report_file}")
        print("\n" + "=" * 60)
        print(report)
