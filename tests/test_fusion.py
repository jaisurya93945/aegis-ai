from app.core.fusion import FindingFusion
from app.models.findings import (
    FindingSource,
    FindingType,
    SecurityFinding,
    Severity,
)


def make_finding(
    finding_type: FindingType,
    severity: Severity,
    evidence: str | None = None,
    source: FindingSource = FindingSource.RULE,
) -> SecurityFinding:
    return SecurityFinding(
        type=finding_type,
        severity=severity,
        source=source,
        description="Test security finding.",
        evidence=evidence,
    )


def test_empty_findings_return_empty_list():
    fusion = FindingFusion()

    assert fusion.fuse([]) == []


def test_distinct_findings_are_preserved():
    fusion = FindingFusion()

    findings = [
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.HIGH,
        ),
        make_finding(
            FindingType.SYSTEM_PROMPT_EXTRACTION,
            Severity.HIGH,
        ),
    ]

    fused = fusion.fuse(findings)

    assert len(fused) == 2
    assert {finding.type for finding in fused} == {
        FindingType.PROMPT_INJECTION,
        FindingType.SYSTEM_PROMPT_EXTRACTION,
    }


def test_exact_duplicate_findings_are_removed():
    fusion = FindingFusion()

    finding = make_finding(
        FindingType.PROMPT_INJECTION,
        Severity.HIGH,
        evidence="ignore previous instructions",
    )

    fused = fusion.fuse([finding, finding])

    assert len(fused) == 1


def test_same_type_and_evidence_are_deduplicated():
    fusion = FindingFusion()

    findings = [
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.HIGH,
            evidence="ignore previous instructions",
        ),
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.HIGH,
            evidence="ignore previous instructions",
            source=FindingSource.ML,
        ),
    ]

    fused = fusion.fuse(findings)

    assert len(fused) == 1


def test_same_type_with_different_evidence_is_preserved():
    fusion = FindingFusion()

    findings = [
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.HIGH,
            evidence="ignore previous instructions",
        ),
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.HIGH,
            evidence="disregard previous instructions",
        ),
    ]

    fused = fusion.fuse(findings)

    assert len(fused) == 2


def test_different_severity_is_not_deduplicated():
    fusion = FindingFusion()

    findings = [
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.MEDIUM,
            evidence="suspicious instruction",
        ),
        make_finding(
            FindingType.PROMPT_INJECTION,
            Severity.HIGH,
            evidence="suspicious instruction",
        ),
    ]

    fused = fusion.fuse(findings)

    assert len(fused) == 2


def test_fusion_preserves_original_finding_data():
    fusion = FindingFusion()

    finding = make_finding(
        FindingType.OBFUSCATION,
        Severity.HIGH,
        evidence="zero_width_characters=2",
        source=FindingSource.RULE,
    )

    fused = fusion.fuse([finding])

    assert fused[0].type == FindingType.OBFUSCATION
    assert fused[0].severity == Severity.HIGH
    assert fused[0].source == FindingSource.RULE
    assert fused[0].evidence == "zero_width_characters=2"
