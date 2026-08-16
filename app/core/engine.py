from app.detectors.base import Detector
from app.models.findings import SecurityFinding


class AegisEngine:
    """Coordinates registered AegisAI security detectors."""

    def __init__(self, detectors: list[Detector]) -> None:
        self.detectors = detectors

    def analyze(self, text: str) -> list[SecurityFinding]:
        """Run every registered detector against the input."""
        findings: list[SecurityFinding] = []

        for detector in self.detectors:
            findings.extend(detector.detect(text))

        return findings
