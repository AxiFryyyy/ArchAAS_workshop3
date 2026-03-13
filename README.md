## Smart Triage for Customer Support Tickets

This project implements a **multi‑agent smart triage system** that helps route customer support tickets
to the right team with an appropriate priority.

The system is built for the Workshop 3 assignment and showcases:
- Multiple agents with distinct roles (classifier, prioritizer, triage summarizer, orchestrator)
- Tool usage (keyword analysis, SLA rules, simple history stats)
- Shared state to pass information between agents

### 1. High‑level Flow

1. You paste a customer ticket description in the terminal.
2. The **Classifier agent** assigns a ticket category (billing, technical issue, account access, feature request, general inquiry).
3. The **Prioritizer agent** decides the priority level (P1–P4) and impact scope using rules + LLM.
4. The **Triage Summarizer agent** produces a human‑readable summary and recommends a routing queue (e.g. Billing Team, Tech Support).
5. The orchestrator coordinates these steps until the triage is complete.

### 2. Tool Access Control

Each agent has access only to the tools it needs for its role; other tools are not exposed to that agent.

| Agent | Tools allowed | Purpose |
|-------|----------------|---------|
| **Classifier** | `analyze_keywords`, `history_stats` | Category signals and similar-ticket context for classification. |
| **Prioritizer** | `analyze_keywords`, `sla_rules_lookup` | Urgency/impact signals and SLA rules for priority and response time. |
| **Triage Summarizer** | *(none)* | Uses only shared state (classification + priority); no tool calls. |
| **Orchestrator** | *(none)* | Rule-based routing only; no tools. |

So the **Classifier** cannot call SLA rules; the **Prioritizer** cannot call history stats; and the **Summarizer** has no tool access—ensuring clear separation of concerns and tool access control.

### 3. Setup & Run

From the project root:

1. Install dependencies:

```bash
uv sync
```

2. Set your OpenAI API key. Create a `.env` file in the project root (copy from `.env.example`), then set:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the smart triage system:

```bash
uv run python main.py
```

4. When prompted, paste a realistic customer ticket in English, for example:

```text
Our entire team cannot log in to the dashboard since this morning.
It shows a 500 error after we enter our credentials. This is blocking our work.
Please fix this as soon as possible.
```

The system will print the classifier and prioritizer decisions, then show a final **TRIAGE SUMMARY** section.

### 4. Files Overview

- `main.py`: builds and runs the LangGraph workflow for triage.
- `state.py`: defines shared state (ticket text, classification, priority, routing, messages, next_step).
- `nodes.py`: graph nodes (human input, orchestrator, classifier, prioritizer, summarizer).
- `agents/orchestrator.py`: rule‑based orchestrator deciding which agent runs next.
- `agents/classifier_agent.py`: LLM‑based ticket classifier.
- `agents/prioritizer_agent.py`: LLM‑based priority evaluator using keyword + SLA tools.
- `agents/triage_summarizer_agent.py`: LLM‑based triage summary and routing recommendation.
- `tools/keywords.py`: keyword analysis (category scores, urgency, impact signals).
- `tools/sla.py`: simple SLA / priority rules helper.
- `tools/history.py`: stubbed “history stats” for similar tickets.

