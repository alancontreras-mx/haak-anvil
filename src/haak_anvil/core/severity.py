"""Risk scoring and severity normalization."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Severity(str, Enum):
    """Normalized severity scale used across all parsers and renderers."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def numeric(self) -> int:
        return {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}[self.value]

    @property
    def label_es(self) -> str:
        return {
            "info": "Informativo",
            "low": "Baja",
            "medium": "Media",
            "high": "Alta",
            "critical": "Crítica",
        }[self.value]


class CVSS(BaseModel):
    """CVSS v3.1 base score with optional vector."""

    score: float = Field(ge=0.0, le=10.0)
    vector: str | None = None
    version: str = "3.1"

    @field_validator("vector")
    @classmethod
    def vector_must_start_with_cvss(cls, v: str | None) -> str | None:
        if v is not None and not v.upper().startswith("CVSS:"):
            raise ValueError("CVSS vector must begin with 'CVSS:'")
        return v


def severity_from_cvss(score: float) -> Severity:
    """Map CVSS v3.1 base score to normalized severity per NVD/FIRST guidance.

    https://nvd.nist.gov/vuln-metrics/cvss
    """
    if score >= 9.0:
        return Severity.CRITICAL
    if score >= 7.0:
        return Severity.HIGH
    if score >= 4.0:
        return Severity.MEDIUM
    if score > 0.0:
        return Severity.LOW
    return Severity.INFO


def severity_from_nessus(risk_factor: str) -> Severity:
    """Map Nessus risk_factor field to normalized Severity."""
    return {
        "Critical": Severity.CRITICAL,
        "High": Severity.HIGH,
        "Medium": Severity.MEDIUM,
        "Low": Severity.LOW,
        "None": Severity.INFO,
    }.get(risk_factor, Severity.INFO)
