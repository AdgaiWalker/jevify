"""
A typical legacy/existing user project: An Express/FastAPI or simple Python bot
Problem 1: Using expensive GPT-4o for simple ticket classification (takes 2.5s, $0.03/call)
Problem 2: Fragile regex checking for prompt injection and spam
"""

import re
import os

# Legacy Pattern 1: Fragile regex hell for spam & injection detection
SPAM_KEYWORDS = ["buy now", "free crypto", "urgent transfer", "click link", "discount code"]
INJECTION_KEYWORDS = ["ignore previous", "system prompt", "you are now", "override"]

def check_spam_and_safety_legacy(user_message: str):
    # Fragile rule: missed easily by typos or obfuscation
    for kw in SPAM_KEYWORDS:
        if kw in user_message.lower():
            return {"is_spam": True, "action": "block"}
    for kw in INJECTION_KEYWORDS:
        if kw in user_message.lower():
            return {"is_safe": False, "action": "block"}
    return {"is_safe": True, "is_spam": False, "action": "pass"}


# Legacy Pattern 2: Heavy LLM overkill for simple intent routing
def route_support_ticket_with_gpt4(ticket_text: str):
    # This is a slow, expensive 2500ms call to an LLM
    prompt = f"""
    You are a customer support triage bot.
    Please classify the following ticket into: billing, devops, or general.
    Also decide if it is P0 emergency.
    Ticket: {ticket_text}
    Output JSON format: {{"department": "...", "is_urgent": true/false}}
    """
    # simulated heavy LLM call (in real life: openai.chat.completions.create)
    return {"department": "billing", "is_urgent": True, "_simulated_latency_ms": 2450}
