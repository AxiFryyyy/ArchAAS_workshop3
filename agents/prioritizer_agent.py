"""
Priority evaluation specialist (Prioritizer agent).
"""

from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from state import State
from tools import analyze_keywords, sla_rules_lookup


def prioritizer_agent(state: State) -> Dict[str, Any]:
    """
    Decide ticket priority level and impact scope based on
    ticket text, classification, and keyword/SLA helpers.
    """
    ticket_text = state.get("ticket_text", "")
    classification = state.get("classification") or {}
    category = classification.get("category", "general_inquiry")

    kw = analyze_keywords(ticket_text)
    urgency_signals = kw.get("urgency_signals", [])
    impact_bucket = kw.get("impact_bucket", "unknown")

    sla_suggestion = sla_rules_lookup(category, urgency_signals, impact_bucket)

    system_prompt = """You are a ticket prioritization specialist.
Your job is to decide how urgent and important a ticket is.

Priority levels:
- P1_critical: system-wide or business-critical outage, many users affected, must be handled immediately
- P2_high: important issues affecting core functionality, multiple users or important workflows impacted
- P3_normal: standard issues affecting a single user or non-critical paths
- P4_low: low-impact issues, feature requests, general questions

You will be given:
- Ticket text
- The chosen category
- Simple keyword analysis (urgency / impact signals)
- A recommended SLA / priority suggestion from rules

Use the SLA suggestion as a strong guideline, but you may adjust slightly
if the ticket text clearly suggests a different severity.

Output MUST follow this exact pattern:
Priority: <P1_critical|P2_high|P3_normal|P4_low>
Impact scope: <single_user|multiple_users|system_wide|unknown>
SLA target: <short SLA description>
Reason: <1–3 short sentences>"""

    user_prompt = f"""Ticket text:
----------------
{ticket_text}

Category: {category}

Keyword analysis:
{kw}

SLA suggestion:
{sla_suggestion}
"""

    llm = ChatOpenAI(model="gpt-5-mini", temperature=1)
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    content = str(response.content).strip()

    level = sla_suggestion.get("priority_level", "P3_normal")
    impact_scope = sla_suggestion.get("impact_scope", "single_user")
    sla_target = sla_suggestion.get("sla_target", "Respond within 1 business day")
    reason = sla_suggestion.get("reason", "")

    for line in content.splitlines():
        line_lower = line.lower()
        if line_lower.startswith("priority:"):
            level = line.split(":", 1)[1].strip()
        elif line_lower.startswith("impact scope:"):
            impact_scope = line.split(":", 1)[1].strip()
        elif line_lower.startswith("sla target:"):
            sla_target = line.split(":", 1)[1].strip()
        elif line_lower.startswith("reason:"):
            reason = line.split(":", 1)[1].strip()

    priority: Dict[str, Any] = {
        "level": level,
        "impact_scope": impact_scope,
        "sla_target": sla_target,
        "reason": reason or content,
        "raw_output": content,
        "sla_suggestion": sla_suggestion,
        "keyword_analysis": kw,
    }

    message = {
        "role": "assistant",
        "name": "prioritizer_agent",
        "content": (
            f"[Prioritizer] Priority: {level} (impact: {impact_scope})\n"
            f"SLA: {sla_target}\n"
            f"Reason: {reason or 'See raw output.'}"
        ),
    }

    return {
        "priority": priority,
        "messages": [message],
        "next_step": "summarize",
    }

