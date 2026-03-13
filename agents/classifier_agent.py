"""
Ticket classification specialist (Classifier agent).
"""

from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from state import State
from tools import analyze_keywords, history_stats


def classifier_agent(state: State) -> Dict[str, Any]:
    """
    Classify the ticket into one of the predefined categories and
    return a structured classification result plus an agent message.
    """
    ticket_text = state.get("ticket_text", "")

    kw = analyze_keywords(ticket_text)
    hist = history_stats(ticket_text)

    system_prompt = """You are a ticket classification specialist in a customer support team.
Your job is to assign ONE main category to the ticket based on its text.

Available categories:
- billing: billing, invoice, charges, refunds, payments, subscriptions, pricing
- technical_issue: bugs, errors, crashes, performance, service down, API failures
- account_access: login, password, account locked, verification, suspension, access rights
- feature_request: users asking for new features or improvements
- general_inquiry: general questions that do not clearly fit the above categories

You are given:
- The raw ticket text
- Simple keyword analysis (category scores, urgency, impact signals)
- A simple history statistic about similar tickets

Decide:
1) The single best category (billing, technical_issue, account_access, feature_request, general_inquiry)
2) A confidence level: high / medium / low
3) A short reason (1–2 sentences) explaining your choice.

Output MUST follow this exact pattern:
Category: <one of the category labels>
Confidence: <high|medium|low>
Reason: <short explanation>"""

    user_prompt = f"""Ticket text:
----------------
{ticket_text}

Keyword analysis:
{kw}

History stats:
{hist}
"""

    llm = ChatOpenAI(model="gpt-5-mini", temperature=1)
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    content = str(response.content).strip()

    category = "general_inquiry"
    confidence = "medium"
    reason = ""
    for line in content.splitlines():
        line_lower = line.lower()
        if line_lower.startswith("category:"):
            category = line.split(":", 1)[1].strip()
        elif line_lower.startswith("confidence:"):
            confidence = line.split(":", 1)[1].strip()
        elif line_lower.startswith("reason:"):
            reason = line.split(":", 1)[1].strip()

    classification = {
        "category": category,
        "confidence": confidence,
        "reason": reason or content,
        "raw_output": content,
        "keyword_analysis": kw,
        "history": hist,
    }

    message = {
        "role": "assistant",
        "name": "classifier_agent",
        "content": f"[Classifier] Category: {category} (confidence: {confidence})\nReason: {reason or 'See raw output.'}",
    }

    return {
        "classification": classification,
        "messages": [message],
        "next_step": "prioritize",
    }

