from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FailureCategory(str, Enum):
    timeout = "timeout"
    authentication = "authentication"
    database = "database"
    network = "network"
    dependency_failure = "dependency_failure"
    unknown = "unknown"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ActionableLogEvent(BaseModel):
    raw_log: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    category: FailureCategory
    severity: Severity = Severity.medium
    retryable: bool = False
    recommended_actions: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    n8n_payload: dict[str, Any] = Field(default_factory=dict)

