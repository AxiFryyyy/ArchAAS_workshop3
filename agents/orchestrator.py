"""
Rule-based orchestrator for the smart triage project.
"""

from typing import Dict, Any

from state import State


def orchestrator(state: State) -> Dict[str, Any]:
    """
    Decide the next step based on what has already been computed.

    This is intentionally rule-based (no LLM) for determinism:
      - If no classification yet -> classify
      - Else if no priority yet -> prioritize
      - Else if no routing yet -> summarize
      - Else -> done
    """
    if state.get("classification") is None:
        next_step = "classify"
    elif state.get("priority") is None:
        next_step = "prioritize"
    elif state.get("routing") is None:
        next_step = "summarize"
    else:
        next_step = "done"

    return {"next_step": next_step}

