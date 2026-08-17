from app.core.registry import get_default_detectors
from app.detectors.base import Detector
from app.models.findings import (
    Decision,
    SecurityAnalysis,
    Severity,
    SecurityFinding,
)


class AegisEngine:
    """Coordinates registered AegisAI security detectors."""

    def __init__(self, detectors: list[Detector] | None = None) -> None:
        self.detectors = (
            detectors if detectors is not None else get_default_detectors()
        )

    def analyze(self, text: str) -> SecurityAnalysis:
        """Run every detector and return a structured analysis."""
        findings: list[SecurityFinding] = []

        for detector in self.detectors:
            result = detector.detect(text)
            findings.extend(result.findings)

        return SecurityAnalysis(
            risk_score=0,
            severity=Severity.LOW,
            decision=Decision.ALLOW,
            findings=findings,
        )
