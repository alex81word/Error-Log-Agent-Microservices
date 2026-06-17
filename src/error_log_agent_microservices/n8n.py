from __future__ import annotations

from .models import ActionableLogEvent


def build_n8n_payload(event: ActionableLogEvent) -> dict[str, object]:
    """Shape an actionable event for downstream N8N workflows."""

    return {
        "event_type": event.category.value,
        "severity": event.severity.value,
        "retryable": event.retryable,
        "summary": event.summary,
        "raw_log": event.raw_log,
        "recommended_actions": event.recommended_actions,
        "tags": event.tags,
    }
