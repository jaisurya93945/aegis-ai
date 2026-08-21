from app.core.registry import get_default_detectors
from app.detectors.jailbreak import JailbreakDetector
from app.detectors.obfuscation import ObfuscationDetector


def test_default_detectors_are_registered():
    detectors = get_default_detectors()

    assert len(detectors) == 5

    assert any(
        isinstance(detector, JailbreakDetector)
        for detector in detectors
    )

    assert any(
        isinstance(detector, ObfuscationDetector)
        for detector in detectors
    )
