import base64
import binascii
import re

from app.detectors.base import Detector
from app.models.findings import (
    FindingSource,
    FindingType,
    SecurityFinding,
    Severity,
)
from app.models.results import DetectorResult


class ObfuscationDetector(Detector):
    """Detect suspicious instruction-obfuscation techniques."""

    name = "obfuscation"

    _SUSPICIOUS_TERMS = (
        "ignore previous instructions",
        "ignore all previous instructions",
        "reveal the system prompt",
        "reveal hidden instructions",
        "follow these instructions",
        "disregard previous instructions",
        "bypass safety",
        "jailbreak",
    )

    _ZERO_WIDTH_RE = re.compile(
        r"[\u200b\u200c\u200d\u2060\ufeff]"
    )

    _CONTROL_CHAR_RE = re.compile(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"
    )

    _BASE64_RE = re.compile(
        r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{20,}={0,2}(?![A-Za-z0-9+/])"
    )

    def detect(self, text: str) -> DetectorResult:
        """Analyze text for suspicious obfuscation indicators."""

        findings: list[SecurityFinding] = []

        normalized = " ".join(text.lower().split())

        # ---------------------------------------------------------
        # Zero-width Unicode characters
        # ---------------------------------------------------------

        zero_width_matches = self._ZERO_WIDTH_RE.findall(text)

        if zero_width_matches:
            suspicious_context = any(
                term in normalized
                for term in self._SUSPICIOUS_TERMS
            )

            if suspicious_context:
                findings.append(
                    SecurityFinding(
                        type=FindingType.OBFUSCATION,
                        severity=Severity.HIGH,
                        source=FindingSource.RULE,
                        description=(
                            "Suspicious zero-width Unicode characters "
                            "were detected in an input containing "
                            "security-sensitive instructions."
                        ),
                        evidence=(
                            f"zero_width_characters="
                            f"{len(zero_width_matches)}"
                        ),
                    )
                )

        # ---------------------------------------------------------
        # Suspicious control characters
        # ---------------------------------------------------------

        control_matches = self._CONTROL_CHAR_RE.findall(text)

        if control_matches:
            suspicious_context = any(
                term in normalized
                for term in self._SUSPICIOUS_TERMS
            )

            if suspicious_context:
                findings.append(
                    SecurityFinding(
                        type=FindingType.OBFUSCATION,
                        severity=Severity.MEDIUM,
                        source=FindingSource.RULE,
                        description=(
                            "Suspicious control characters were "
                            "detected in a security-sensitive input."
                        ),
                        evidence=(
                            f"control_characters="
                            f"{len(control_matches)}"
                        ),
                    )
                )

        # ---------------------------------------------------------
        # Base64-looking payloads
        # ---------------------------------------------------------

        encoded_candidates = self._BASE64_RE.findall(text)

        for candidate in encoded_candidates:
            decoded = self._decode_base64(candidate)

            if decoded is None:
                continue

            decoded_normalized = " ".join(
                decoded.lower().split()
            )

            if any(
                term in decoded_normalized
                for term in self._SUSPICIOUS_TERMS
            ):
                findings.append(
                    SecurityFinding(
                        type=FindingType.OBFUSCATION,
                        severity=Severity.HIGH,
                        source=FindingSource.RULE,
                        description=(
                            "A Base64-encoded payload contains "
                            "security-sensitive instructions."
                        ),
                        evidence=(
                            f"base64_payload={candidate[:32]}..."
                        ),
                    )
                )

        # ---------------------------------------------------------
        # Excessive whitespace / instruction splitting
        # ---------------------------------------------------------

        if self._contains_suspicious_whitespace_pattern(text):
            findings.append(
                SecurityFinding(
                    type=FindingType.OBFUSCATION,
                    severity=Severity.MEDIUM,
                    source=FindingSource.RULE,
                    description=(
                        "Suspicious whitespace manipulation was "
                        "detected around security-sensitive "
                        "instructions."
                    ),
                    evidence="suspicious_whitespace_pattern",
                )
            )

        return DetectorResult(
            detector=self.name,
            findings=findings,
        )

    @staticmethod
    def _decode_base64(value: str) -> str | None:
        """Safely decode a Base64 candidate."""

        try:
            padding = "=" * (-len(value) % 4)

            decoded = base64.b64decode(
                value + padding,
                validate=True,
            )

            return decoded.decode(
                "utf-8",
                errors="strict",
            )

        except (
            ValueError,
            UnicodeDecodeError,
            binascii.Error,
        ):
            return None

    @staticmethod
    def _contains_suspicious_whitespace_pattern(
        text: str,
    ) -> bool:
        """
        Detect security-sensitive instructions separated by
        unusual whitespace patterns.
        """

        patterns = (
            r"ignore\s{4,}previous\s+instructions",
            r"ignore[\t\r\n]+previous\s+instructions",
            r"reveal\s{4,}the\s+system\s+prompt",
            r"disregard[\t\r\n]+previous\s+instructions",
        )

        normalized_source = text.lower()

        return any(
            re.search(pattern, normalized_source)
            for pattern in patterns
        )
