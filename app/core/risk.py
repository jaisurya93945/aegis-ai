from app.models.findings import FindingSource, SecurityFinding, Severity


class RiskEngine:
    """Calculate a transparent risk score from security findings."""

    _SEVERITY_SCORES = {
        Severity.LOW: 20,
        Severity.MEDIUM: 40,
        Severity.HIGH: 70,
        Severity.CRITICAL: 95,
    }

    # ML findings are intentionally capped below deterministic HIGH risk.
    _ML_SEVERITY_SCORES = {
        Severity.LOW: 10,
        Severity.MEDIUM: 25,
        Severity.HIGH: 50,
        Severity.CRITICAL: 70,
    }

    def calculate_score(self, findings: list[SecurityFinding]) -> int:
        """Return the highest risk score among security findings."""

        if not findings:
            return 0

        scores = []

        for finding in findings:
            if finding.source == FindingSource.ML:
                score = self._ML_SEVERITY_SCORES[finding.severity]
            else:
                score = self._SEVERITY_SCORES[finding.severity]

            scores.append(score)

        return max(scores)

    def calculate_severity(
        self,
        findings: list[SecurityFinding],
    ) -> Severity:
        """Return the effective security severity."""

        if not findings:
            return Severity.LOW

        severity_order = {
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 3,
            Severity.CRITICAL: 4,
        }

        # Deterministic findings retain their full severity authority.
        rule_findings = [
            finding
            for finding in findings
            if finding.source == FindingSource.RULE
        ]

        if rule_findings:
            return max(
                rule_findings,
                key=lambda finding: severity_order[finding.severity],
            ).severity

        # ML-only findings are mapped to a conservative effective severity.
        highest_ml = max(
            findings,
            key=lambda finding: severity_order[finding.severity],
        )

        if highest_ml.severity == Severity.HIGH:
            return Severity.MEDIUM

        return highest_ml.severity
