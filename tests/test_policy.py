from app.core.policy import PolicyEngine
from app.models.findings import Decision, Severity


def test_low_severity_allows_request():
    policy = PolicyEngine()

    assert policy.decide(Severity.LOW) == Decision.ALLOW


def test_medium_severity_warns():
    policy = PolicyEngine()

    assert policy.decide(Severity.MEDIUM) == Decision.WARN


def test_high_severity_blocks_request():
    policy = PolicyEngine()

    assert policy.decide(Severity.HIGH) == Decision.BLOCK


def test_critical_severity_blocks_request():
    policy = PolicyEngine()

    assert policy.decide(Severity.CRITICAL) == Decision.BLOCK


def test_high_severity_policy_can_be_customized():
    policy = PolicyEngine(high_action=Decision.WARN)

    assert policy.decide(Severity.HIGH) == Decision.WARN
