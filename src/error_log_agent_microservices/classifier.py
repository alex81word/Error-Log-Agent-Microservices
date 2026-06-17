from __future__ import annotations

from .models import ActionableLogEvent, FailureCategory, Severity
from .n8n import build_n8n_payload

_RULES: dict[FailureCategory, tuple[tuple[str, ...], Severity, bool, list[str]]] = {
    FailureCategory.timeout: (
        ("timeout", "timed out", "deadline exceeded"),
        Severity.high,
        True,
        ["check latency", "increase timeout budget", "inspect upstream service health"],
    ),
    FailureCategory.authentication: (
        ("unauthorized", "forbidden", "authentication failed", "invalid credentials", "jwt"),
        Severity.critical,
        False,
        ["verify credentials", "refresh tokens", "check auth provider status"],
    ),
    FailureCategory.database: (
        ("database", "sql", "postgres", "mysql", "deadlock", "connection pool"),
        Severity.high,
        True,
        ["inspect database availability", "review connection pool limits", "check query performance"],
    ),
    FailureCategory.network: (
        ("network", "dns", "connection reset", "connection refused", "econnreset", "ehostunreach"),
        Severity.high,
        True,
        ["check routing and dns", "validate service reachability", "inspect firewall or proxy"],
    ),
    FailureCategory.dependency_failure: (
        ("dependency", "module not found", "importerror", "package missing", "artifact"),
        Severity.medium,
        False,
        ["verify dependency installation", "rebuild the environment", "check package lock or image"],
    ),
}


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _with_n8n_payload(event: ActionableLogEvent) -> ActionableLogEvent:
    return event.model_copy(update={"n8n_payload": build_n8n_payload(event)})


def classify_log(log_text: str) -> ActionableLogEvent:
    normalized = _normalize(log_text)

    for category, (keywords, severity, retryable, recommendations) in _RULES.items():
        if any(keyword in normalized for keyword in keywords):
            return _with_n8n_payload(
                ActionableLogEvent(
                    raw_log=log_text,
                    summary=f"Detected {category.value.replace('_', ' ')} failure",
                    category=category,
                    severity=severity,
                    retryable=retryable,
                    recommended_actions=recommendations,
                    tags=[category.value, "actionable"],
                )
            )

    return _with_n8n_payload(
        ActionableLogEvent(
            raw_log=log_text,
            summary="Unclassified log event",
            category=FailureCategory.unknown,
            severity=Severity.low,
            retryable=False,
            recommended_actions=["capture more context", "route to manual triage"],
            tags=["unknown", "actionable"],
        )
    )
