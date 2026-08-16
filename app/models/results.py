from pydantic import BaseModel, Field

from app.models.findings import SecurityFinding


class DetectorResult(BaseModel):
    """Result returned by an AegisAI detector."""

    detector: str = Field(min_length=1)
    findings: list[SecurityFinding] = Field(default_factory=list)
