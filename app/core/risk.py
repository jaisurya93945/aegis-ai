from app.models.findings import (
    Decision,
    SecurityFinding,
    Severity,
)


class RiskEngine:
    """Calculate a transparent baseline risk score from security findings."""

    _SEVERITY_SCORES = {
        Severity.LOW: 20,
        Severity.MEDIUM: 40,
        Severity.HIGH: 70,
        Severity.CRITICAL: 95,
    }

    def calculate_score(self, findings: list[SecurityFinding]) -> int:
        """Return the highest severity score among the findings."""

        if not findings:
            return 0

        return max(
            self._SEVERITY_SCORES[finding.severity]
            for finding in findings
        )

    def calculate_severity(self, findings: list[SecurityFinding]) -> Severity:
        """Return the highest severity represented by the findings."""

        if not findings:
            return Severity.LOW

        severity_order = {
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 3,
            Severity.CRITICAL: 4,
        }

        return max(
            findings,
            key=lambda finding: severity_order[finding.severity],
        ).severity

    def calculate_decision(self, findings: list[SecurityFinding]) -> Decision:
        """Return a baseline security decision."""

        if not findings:
            return Decision.ALLOW

        severity = self.calculate_severity(findings)

        if severity in {Severity.HIGH, Severity.CRITICAL}:
            return Decision.BLOCK

        return Decision.WARN
