from app.models.findings import Decision, Severity


class PolicyEngine:
    """Apply security policy to a calculated risk severity."""

    def __init__(
        self,
        high_action: Decision = Decision.BLOCK,
        critical_action: Decision = Decision.BLOCK,
    ) -> None:
        self.high_action = high_action
        self.critical_action = critical_action

    def decide(self, severity: Severity) -> Decision:
        """Return the action associated with the supplied severity."""

        if severity == Severity.CRITICAL:
            return self.critical_action

        if severity == Severity.HIGH:
            return self.high_action

        if severity in {Severity.MEDIUM, Severity.LOW}:
            return Decision.WARN if severity == Severity.MEDIUM else Decision.ALLOW

        return Decision.ALLOW
