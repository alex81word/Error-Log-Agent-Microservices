from error_log_agent_microservices.classifier import classify_log
from error_log_agent_microservices.n8n import build_n8n_payload


def test_n8n_payload_contains_actionable_fields():
    event = classify_log("DNS failure: connection refused to upstream")
    payload = build_n8n_payload(event)

    assert payload["event_type"] == "network"
    assert payload["retryable"] is True
    assert payload["summary"] == event.summary
