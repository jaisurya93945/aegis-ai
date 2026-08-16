from app.detectors.base import Detector
from app.detectors.prompt_injection import PromptInjectionDetector


def get_default_detectors() -> list[Detector]:
    """Return the detectors enabled by default."""
    return [
        PromptInjectionDetector(),
    ]
