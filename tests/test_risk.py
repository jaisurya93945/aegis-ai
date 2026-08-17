from app.core.risk import RiskEngine
from app.models.findings import (
    FindingType,
    SecurityFinding,
    Severity,
)


def make_finding(severity: Severity) -> SecurityFinding:
    return SecurityFinding(
        type=FindingType.PROMPT_INJECTION,
        severity=severity,
        description="Test security finding.",
    )


def test_no_findings_have_zero_risk():
    engine = RiskEngine()

    assert engine.calculate_score([]) == 0
    assert engine.calculate_severity([]) == Severity.LOW


def test_high_severity_produces_high_risk():
    engine = RiskEngine()

    findings = [make_finding(Severity.HIGH)]

    assert engine.calculate_score(findings) == 70
    assert engine.calculate_severity(findings) == Severity.HIGH


def test_critical_severity_produces_critical_risk():
    engine = RiskEngine()

    findings = [make_finding(Severity.CRITICAL)]

    assert engine.calculate_score(findings) == 95
    assert engine.calculate_severity(findings) == Severity.CRITICAL


def test_highest_severity_wins():
    engine = RiskEngine()

    findings = [
        make_finding(Severity.LOW),
        make_finding(Severity.HIGH),
        make_finding(Severity.MEDIUM),
    ]

    assert engine.calculate_score(findings) == 70
    assert engine.calculate_severity(findings) == Severity.HIGH
