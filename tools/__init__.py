"""
Tools package for the smart triage customer support project.

Exposes helper functions that agents can call, such as
keyword analysis and SLA rules lookup.
"""

from .keywords import analyze_keywords
from .sla import sla_rules_lookup
from .history import history_stats

__all__ = ["analyze_keywords", "sla_rules_lookup", "history_stats"]

