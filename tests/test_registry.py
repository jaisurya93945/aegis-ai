from app.core.registry import get_default_detectors
from app.detectors.extraction import SystemPromptExtractionDetector
from app.detectors.prompt_injection import PromptInjectionDetector


def test_default_detectors_are_registered():
    detectors = get_default_detectors()

    assert len(detectors) == 2
    assert isinstance(detectors[0], PromptInjectionDetector)
    assert isinstance(detectors[1], SystemPromptExtractionDetector)
