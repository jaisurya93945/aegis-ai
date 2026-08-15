from app.detectors.base import Detector
from app.models.findings import (
    FindingType,
    SecurityFinding,
    Severity,
)


class PromptInjectionDetector(Detector):
    """Baseline detector for common prompt injection indicators."""

    name = "prompt_injection"

    _INDICATORS = (
        "ignore previous instructions",
        "ignore all previous instructions",
        "disregard previous instructions",
        "disregard all previous instructions",
        "forget previous instructions",
        "override previous instructions",
    )

    def detect(self, text: str) -> list[SecurityFinding]:
        normalized = text.casefold()

        matches = [
            indicator
            for indicator in self._INDICATORS
            if indicator in normalized
        ]

        if not matches:
            return []

        return [
            SecurityFinding(
                type=FindingType.PROMPT_INJECTION,
                severity=Severity.HIGH,
                description="Potential prompt injection indicator detected.",
                evidence=matches[0],
            )
        ]
