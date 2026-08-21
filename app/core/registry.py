from app.detectors.base import Detector
from app.detectors.extraction import SystemPromptExtractionDetector
from app.detectors.jailbreak import JailbreakDetector
from app.detectors.ml_prompt_injection import MLPromptInjectionDetector
from app.detectors.obfuscation import ObfuscationDetector
from app.detectors.prompt_injection import PromptInjectionDetector


def get_default_detectors() -> list[Detector]:
    """Return the detectors enabled by default."""

    return [
        PromptInjectionDetector(),
        SystemPromptExtractionDetector(),
        MLPromptInjectionDetector(),
        JailbreakDetector(),
        ObfuscationDetector(),
    ]
