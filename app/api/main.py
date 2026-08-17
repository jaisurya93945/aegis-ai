from fastapi import FastAPI

from app.api.schemas import AnalyzeRequest, AnalyzeResponse, FindingResponse
from app.core.service import AegisService


app = FastAPI(
    title="AegisAI",
    description="AI security gateway for LLM, RAG, and agentic AI applications.",
    version="0.1.0",
)

service = AegisService()


@app.get("/health")
def health() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok"}


@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze an AI-related input for security threats."""
    analysis = service.analyze(request.text)

    return AnalyzeResponse(
        risk_score=analysis.risk_score,
        severity=analysis.severity.value,
        decision=analysis.decision.value,
        findings=[
            FindingResponse(
                type=finding.type.value,
                severity=finding.severity.value,
                description=finding.description,
                evidence=finding.evidence,
            )
            for finding in analysis.findings
        ],
    )
