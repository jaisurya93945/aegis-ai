from app.models.findings import FindingType, SecurityFinding, Severity
from app.models.results import DetectorResult


def test_detector_result_with_no_findings():
    result = DetectorResult(detector="prompt_injection")

    assert result.detector == "prompt_injection"
    assert result.findings == []


def test_detector_result_with_finding():
    finding = SecurityFinding(
        type=FindingType.PROMPT_INJECTION,
        severity=Severity.HIGH,
        description="Potential prompt injection indicator detected.",
        evidence="ignore previous instructions",
    )

    result = DetectorResult(
        detector="prompt_injection",
        findings=[finding],
    )

    assert result.detector == "prompt_injection"
    assert len(result.findings) == 1
    assert result.findings[0].type == FindingType.PROMPT_INJECTION
