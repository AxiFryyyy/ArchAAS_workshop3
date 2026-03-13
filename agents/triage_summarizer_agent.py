"""
Summarizer agent for the smart triage project.
"""

from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from state import State


def triage_summarizer_agent(state: State) -> Dict[str, Any]:
    """
    Generate a human-readable triage summary and routing recommendation.
    """
    ticket_text = state.get("ticket_text", "")
    classification = state.get("classification") or {}
    priority = state.get("priority") or {}

    category = classification.get("category", "general_inquiry")
    priority_level = priority.get("level", "P3_normal")
    impact_scope = priority.get("impact_scope", "unknown")
    sla_target = priority.get("sla_target", "Respond within 1 business day")

    system_prompt = """You are the triage summarizer in a customer support system.
Your goal is to produce a short, clear summary that helps support agents
quickly understand how to handle the ticket.

You will be given:
- The original ticket text
- The chosen category
- The chosen priority and impact scope
- Any SLA target and reasoning

You should:
1) Restate the core problem in 1–2 sentences.
2) Explicitly mention the category and priority level.
3) Recommend a routing queue or team, such as:
   - "Billing Team - L2" for complex billing issues
   - "Tech Support - L1" for standard technical issues
   - "Account Support" for account and login issues
   - "Product Management" for feature requests
4) Optionally, give a short note to the agent (1 sentence) with any special attention points.

Output in this format:
Summary: <1–2 sentences>
Category: <category>
Priority: <priority level> (<impact scope>)
Recommended routing: <queue/team>
Notes: <short note>"""

    user_prompt = f"""Ticket text:
----------------
{ticket_text}

Category: {category}
Priority: {priority_level}
Impact scope: {impact_scope}
SLA target: {sla_target}

Classification detail:
{classification}

Priority detail:
{priority}
"""

    llm = ChatOpenAI(model="gpt-5-nano", temperature=1)
    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
    )

    content = str(response.content).strip()

    routing_queue = "General Support"
    for line in content.splitlines():
        if line.lower().startswith("recommended routing:"):
            routing_queue = line.split(":", 1)[1].strip()
            break

    routing: Dict[str, Any] = {
        "queue": routing_queue,
        "summary": content,
    }

    message = {
        "role": "assistant",
        "name": "triage_summarizer",
        "content": content,
    }

    return {
        "routing": routing,
        "messages": [message],
        "next_step": "done",
    }

