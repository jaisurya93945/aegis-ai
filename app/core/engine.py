from app.core.registry import get_default_detectors
from app.core.risk import RiskEngine
from app.detectors.base import Detector
from app.models.findings import SecurityAnalysis, SecurityFinding


class AegisEngine:
    """Coordinates detectors and calculates security risk."""

    def __init__(
        self,
        detectors: list[Detector] | None = None,
        risk_engine: RiskEngine | None = None,
    ) -> None:
        self.detectors = (
            detectors if detectors is not None else get_default_detectors()
        )
        self.risk_engine = risk_engine or RiskEngine()

    def analyze(self, text: str) -> SecurityAnalysis:
        """Run detectors and calculate the resulting security risk."""
        findings: list[SecurityFinding] = []

        for detector in self.detectors:
            result = detector.detect(text)
            findings.extend(result.findings)

        risk_score = self.risk_engine.calculate_score(findings)
        severity = self.risk_engine.calculate_severity(findings)
        decision = self.risk_engine.calculate_decision(findings)

        return SecurityAnalysis(
            risk_score=risk_score,
            severity=severity,
            decision=decision,
            findings=findings,
        )
