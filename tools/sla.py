"""
Simple SLA / priority rules helper.
Encodes heuristic mapping from category + signals to priority and impact.
"""

from typing import Dict, List, Any


def sla_rules_lookup(
    category: str, urgency_signals: List[str], impact_bucket: str
) -> Dict[str, Any]:
    """
    Decide a suggested priority and SLA target based on category and signals.

    Returns:
      {
        "priority_level": str,
        "impact_scope": str,
        "sla_target": str,
        "reason": str,
      }
    """
    category = (category or "general_inquiry").lower()
    impact_bucket = impact_bucket or "unknown"
    has_urgency = bool(urgency_signals)

    # Defaults
    level = "P3_normal"
    scope = "single_user"
    sla = "Respond within 1 business day"
    reason_parts = []

    if impact_bucket == "system_wide":
        scope = "system_wide"
        level = "P1_critical"
        sla = "Respond within 1 hour, resolve within 4 hours"
        reason_parts.append("Signals of system-wide impact")
    elif impact_bucket == "multiple_users":
        scope = "multiple_users"
        level = "P2_high"
        sla = "Respond within 4 hours, resolve within 1 business day"
        reason_parts.append("Signals of multiple users affected")

    if has_urgency and level == "P3_normal":
        # Escalate one step if only urgency but not wide impact
        level = "P2_high"
        sla = "Respond within 4 hours, resolve within 1 business day"
        reason_parts.append("Urgent language in the ticket")

    # Category-specific soft adjustments
    if category == "feature_request":
        if not has_urgency and impact_bucket == "unknown":
            level = "P4_low"
            scope = "unknown"
            sla = "Respond within 2–3 business days"
            reason_parts.append("Feature request with no clear urgency")

    if not reason_parts:
        reason_parts.append("Default priority based on single-user impact")

    reason = "; ".join(reason_parts)

    return {
        "priority_level": level,
        "impact_scope": scope,
        "sla_target": sla,
        "reason": reason,
    }

