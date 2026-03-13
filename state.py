"""
State definition for the smart triage customer support project.
"""

from typing import TypedDict, Annotated, Optional, Dict, Any
import operator


class State(TypedDict):
    # Conversation and agent messages (LangGraph-style append behaviour)
    messages: Annotated[list, operator.add]

    # Raw ticket content and optional metadata
    ticket_text: str
    ticket_meta: Dict[str, Any]

    # Classification result
    classification: Optional[Dict[str, Any]]

    # Priority result
    priority: Optional[Dict[str, Any]]

    # Routing / final triage recommendation
    routing: Optional[Dict[str, Any]]

    # Simple step indicator for orchestrator ("classify" / "prioritize" / "summarize" / "done")
    next_step: Optional[str]

