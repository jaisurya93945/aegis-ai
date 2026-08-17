from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request body for security analysis."""

    text: str = Field(min_length=1)


class FindingResponse(BaseModel):
    """Serialized security finding."""

    type: str
    severity: str
    description: str
    evidence: str | None = None


class AnalyzeResponse(BaseModel):
    """Response returned by the AegisAI analysis endpoint."""

    risk_score: int
    severity: str
    decision: str
    findings: list[FindingResponse]
