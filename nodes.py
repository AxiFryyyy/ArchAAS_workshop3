"""
Graph node functions for the smart triage customer support project.
"""

from typing import Dict, Any

from state import State
from agents.orchestrator import orchestrator
from agents.classifier_agent import classifier_agent
from agents.prioritizer_agent import prioritizer_agent
from agents.triage_summarizer_agent import triage_summarizer_agent


def human_node(state: State) -> Dict[str, Any]:
    """
    Entry node: get ticket text from the user. Type 'exit' to end the session.
    """
    ticket_text = input(
        "\nEnter the customer ticket description (or type 'exit' to quit):\n> "
    ).strip()

    human_message = {
        "role": "user",
        "content": ticket_text,
    }

    return {
        "ticket_text": ticket_text,
        "messages": [human_message],
    }


def orchestrator_node(state: State) -> Dict[str, Any]:
    """
    Orchestrator node: decide which specialist agent should run next.
    """
    return orchestrator(state)


def classifier_node(state: State) -> Dict[str, Any]:
    """
    Run classifier agent.
    """
    result = classifier_agent(state)
    for msg in result.get("messages", []):
        print(msg.get("content", ""))
    return result


def prioritizer_node(state: State) -> Dict[str, Any]:
    """
    Run prioritizer agent.
    """
    result = prioritizer_agent(state)
    for msg in result.get("messages", []):
        print(msg.get("content", ""))
    return result


def summarizer_node(state: State) -> Dict[str, Any]:
    """
    Run summarizer agent.
    """
    result = triage_summarizer_agent(state)

    # Also print a visual separator in the CLI
    print("\n=== TRIAGE SUMMARY ===\n")
    for msg in result.get("messages", []):
        print(msg.get("content", ""))

    return result

