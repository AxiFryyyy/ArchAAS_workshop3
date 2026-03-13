"""
Keyword-based helper for ticket analysis.
This is intentionally simple and rule-based for transparency.
"""

from collections import Counter
from typing import Dict, List, Any


CATEGORY_KEYWORDS = {
    "billing": [
        "bill",
        "invoice",
        "charge",
        "charged",
        "refund",
        "payment",
        "credit card",
        "subscription",
        "auto-renew",
        "pricing",
    ],
    "technical_issue": [
        "bug",
        "error",
        "crash",
        "not working",
        "cannot",
        "can't",
        "failed",
        "timeout",
        "down",
        "broken",
        "loading",
        "lag",
    ],
    "account_access": [
        "login",
        "log in",
        "sign in",
        "password",
        "reset",
        "otp",
        "2fa",
        "verification",
        "locked",
        "suspend",
        "suspended",
        "ban",
        "banned",
        "access",
    ],
    "feature_request": [
        "feature",
        "request",
        "it would be great",
        "suggest",
        "improve",
        "improvement",
        "enhancement",
        "can you add",
        "i wish",
    ],
}

URGENCY_KEYWORDS = [
    "urgent",
    "asap",
    "immediately",
    "right now",
    "critical",
    "cannot use",
    "can't use",
    "blocked",
    "blocker",
]

IMPACT_KEYWORDS = {
    "system_wide": [
        "all users",
        "everyone",
        "entire company",
        "whole company",
        "production",
        "prod",
        "service down",
        "system down",
        "outage",
    ],
    "multiple_users": [
        "multiple users",
        "many users",
        "several users",
        "my team",
        "our team",
        "our customers",
    ],
}


def _find_matches(text: str, patterns: List[str]) -> List[str]:
    text_lower = text.lower()
    return [p for p in patterns if p in text_lower]


def analyze_keywords(ticket_text: str) -> Dict[str, Any]:
    """
    Analyze ticket text to extract simple keyword-based signals.

    Returns a dict with:
      - category_scores: Counter-like mapping category -> score (int)
      - urgency_signals: list of matched urgency phrases
      - impact_signals: list of matched impact phrases (raw)
      - impact_bucket: one of "system_wide" / "multiple_users" / "unknown"
      - raw_matches: per-category keyword hits
    """
    text = ticket_text or ""

    # Category scores
    category_scores: Counter = Counter()
    raw_matches: Dict[str, List[str]] = {}

    for category, patterns in CATEGORY_KEYWORDS.items():
        matches = _find_matches(text, patterns)
        if matches:
            category_scores[category] += len(matches)
            raw_matches[category] = matches

    # Urgency
    urgency_signals = _find_matches(text, URGENCY_KEYWORDS)

    # Impact
    impact_signals_raw: List[str] = []
    impact_bucket = "unknown"
    for bucket, patterns in IMPACT_KEYWORDS.items():
        matches = _find_matches(text, patterns)
        if matches:
            impact_signals_raw.extend(matches)
            # choose the first bucket that matches as primary
            if impact_bucket == "unknown":
                impact_bucket = bucket

    return {
        "category_scores": dict(category_scores),
        "urgency_signals": urgency_signals,
        "impact_signals": impact_signals_raw,
        "impact_bucket": impact_bucket,
        "raw_matches": raw_matches,
    }

