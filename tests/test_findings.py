from app.models.findings import (
    Decision,
    FindingType,
    SecurityAnalysis,
    SecurityFinding,
    Severity,
)


def test_empty_security_analysis():
    analysis = SecurityAnalysis(
        risk_score=0,
        severity=Severity.LOW,
        decision=Decision.ALLOW,
    )

    assert analysis.risk_score == 0
    assert analysis.severity == Severity.LOW
    assert analysis.decision == Decision.ALLOW
    assert analysis.findings == []


def test_security_finding():
    finding = SecurityFinding(
        type=FindingType.PROMPT_INJECTION,
        severity=Severity.HIGH,
        description="Potential instruction override detected.",
        evidence="Ignore previous instructions",
    )

    assert finding.type == FindingType.PROMPT_INJECTION
    assert finding.severity == Severity.HIGH
    assert finding.evidence == "Ignore previous instructions"


def test_risk_score_bounds():
    analysis = SecurityAnalysis(
        risk_score=100,
        severity=Severity.CRITICAL,
        decision=Decision.BLOCK,
    )

    assert analysis.risk_score == 100
