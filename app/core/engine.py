from app.core.fusion import FindingFusion
from app.core.policy import PolicyEngine
from app.core.registry import get_default_detectors
from app.core.risk import RiskEngine
from app.detectors.base import Detector
from app.models.findings import SecurityAnalysis, SecurityFinding


class AegisEngine:
    """Coordinates detection, finding fusion, risk analysis, and policy."""

    def __init__(
        self,
        detectors: list[Detector] | None = None,
        risk_engine: RiskEngine | None = None,
        policy_engine: PolicyEngine | None = None,
        fusion: FindingFusion | None = None,
    ) -> None:
        self.detectors = (
            detectors if detectors is not None else get_default_detectors()
        )
        self.risk_engine = risk_engine or RiskEngine()
        self.policy_engine = policy_engine or PolicyEngine()
        self.fusion = fusion or FindingFusion()

    def analyze(self, text: str) -> SecurityAnalysis:
        """Run detectors, fuse findings, calculate risk, and apply policy."""

        findings: list[SecurityFinding] = []

        for detector in self.detectors:
            result = detector.detect(text)
            findings.extend(result.findings)

        findings = self.fusion.fuse(findings)

        risk_score = self.risk_engine.calculate_score(findings)
        severity = self.risk_engine.calculate_severity(findings)
        decision = self.policy_engine.decide(severity)

        return SecurityAnalysis(
            risk_score=risk_score,
            severity=severity,
            decision=decision,
            findings=findings,
        )
