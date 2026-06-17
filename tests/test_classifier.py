from error_log_agent_microservices.classifier import classify_log
from error_log_agent_microservices.models import FailureCategory, Severity


def test_timeout_log_is_classified():
    result = classify_log("Request timeout after 30s while waiting for upstream API")
    assert result.category is FailureCategory.timeout
    assert result.severity is Severity.high
    assert result.retryable is True


def test_authentication_log_is_classified():
    result = classify_log("Authentication failed: unauthorized access for user token")
    assert result.category is FailureCategory.authentication
    assert result.severity is Severity.critical
    assert result.retryable is False


def test_database_log_is_classified():
    result = classify_log("Database connection pool exhausted for postgres primary")
    assert result.category is FailureCategory.database
    assert result.severity is Severity.high
    assert result.retryable is True


def test_network_log_is_classified():
    result = classify_log("Network error: connection refused to service endpoint")
    assert result.category is FailureCategory.network
    assert result.severity is Severity.high
    assert result.retryable is True


def test_dependency_failure_log_is_classified():
    result = classify_log("ImportError: module not found during dependency resolution")
    assert result.category is FailureCategory.dependency_failure
    assert result.severity is Severity.medium
    assert result.retryable is False

