"""
Entry point for the smart triage customer support project.
"""

from pathlib import Path

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from state import State
from nodes import (
    human_node,
    orchestrator_node,
    classifier_node,
    prioritizer_node,
    summarizer_node,
)


def build_graph():
    """
    Build the LangGraph workflow for ticket triage.
    """
    builder = StateGraph(State)

    builder.add_node("human", human_node)
    builder.add_node("orchestrator", orchestrator_node)
    builder.add_node("classifier", classifier_node)
    builder.add_node("prioritizer", prioritizer_node)
    builder.add_node("summarizer", summarizer_node)

    builder.add_edge(START, "human")

    def route_after_human(state: State):
        text = (state.get("ticket_text") or "").strip().lower()
        if text == "exit":
            return "__end__"
        return "orchestrator"

    builder.add_conditional_edges(
        "human",
        route_after_human,
        {"orchestrator": "orchestrator", "__end__": END},
    )

    # Dynamic routing based on next_step decided by orchestrator
    def route_from_orchestrator(state: State):
        step = state.get("next_step", "done")
        if step == "classify":
            return "classifier"
        if step == "prioritize":
            return "prioritizer"
        if step == "summarize":
            return "summarizer"
        return "__end__"

    builder.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "classifier": "classifier",
            "prioritizer": "prioritizer",
            "summarizer": "summarizer",
            "__end__": END,
        },
    )

    # After each specialist, return to orchestrator
    builder.add_edge("classifier", "orchestrator")
    builder.add_edge("prioritizer", "orchestrator")
    builder.add_edge("summarizer", END)

    return builder.compile()


def main():
    # Load .env from my_workshop3 directory so you can put OPENAI_API_KEY there
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path, override=True)

    print("=== SMART TRIAGE FOR CUSTOMER SUPPORT TICKETS ===")
    print("Enter ticket descriptions one at a time. Type 'exit' when you are done.\n")

    graph = build_graph()

    try:
        while True:
            initial_state: State = {
                "messages": [],
                "ticket_text": "",
                "ticket_meta": {},
                "classification": None,
                "priority": None,
                "routing": None,
                "next_step": None,
            }
            result = graph.invoke(initial_state)
            if (result.get("ticket_text") or "").strip().lower() == "exit":
                print("\nGoodbye!")
                break
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Ending triage...")


if __name__ == "__main__":
    main()

