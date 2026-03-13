"""
Simple stub for history-based stats.
In a real system this might query a database or analytics store.
Here we just return a deterministic, fake summary based on ticket length.
"""

from typing import Dict, Any


def history_stats(ticket_text: str) -> Dict[str, Any]:
    text = ticket_text or ""
    length = len(text)

    if length > 400:
        count = 20
        trend = "increasing"
        comment = "Similar long-form complaints have increased in the last 24 hours."
    elif length > 150:
        count = 8
        trend = "stable"
        comment = "A moderate number of similar tickets seen recently."
    else:
        count = 2
        trend = "low"
        comment = "Few similar tickets seen; might be an isolated case."

    return {
        "similar_recent_count_24h": count,
        "trend": trend,
        "comment": comment,
    }

