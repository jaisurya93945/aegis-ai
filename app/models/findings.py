from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    """Severity assigned to a security finding."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision(str, Enum):
    """Security action selected by the policy layer."""

    ALLOW = "allow"
    WARN = "warn"
    SANITIZE = "sanitize"
    BLOCK = "block"


class FindingType(str, Enum):
    """Security threat categories recognized by AegisAI."""

    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    SYSTEM_PROMPT_EXTRACTION = "system_prompt_extraction"
    OBFUSCATION = "obfuscation"


class SecurityFinding(BaseModel):
    """A single security finding produced by a detector."""

    type: FindingType
    severity: Severity
    description: str = Field(min_length=1)
    evidence: str | None = None


class SecurityAnalysis(BaseModel):
    """Complete security analysis of an AI-related input."""

    risk_score: int = Field(ge=0, le=100)
    severity: Severity
    decision: Decision
    findings: list[SecurityFinding] = Field(default_factory=list)
