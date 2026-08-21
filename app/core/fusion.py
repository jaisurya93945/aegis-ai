from app.models.findings import SecurityFinding


class FindingFusion:
    """Deduplicate overlapping security findings deterministically."""

    def fuse(
        self,
        findings: list[SecurityFinding],
    ) -> list[SecurityFinding]:
        """
        Return a deduplicated collection of security findings.

        Findings are considered duplicates when their type, severity,
        and evidence are identical. The original finding objects are
        preserved so their source, description, and evidence remain
        available for auditing.
        """

        fused: list[SecurityFinding] = []
        seen: set[tuple] = set()

        for finding in findings:
            key = (
                finding.type,
                finding.severity,
                finding.evidence,
            )

            if key in seen:
                continue

            seen.add(key)
            fused.append(finding)

        return fused
