from abc import ABC, abstractmethod

from app.models.results import DetectorResult


class Detector(ABC):
    """Base interface for all AegisAI security detectors."""

    name: str = "base"

    @abstractmethod
    def detect(self, text: str) -> DetectorResult:
        """Analyze text and return a structured detector result."""
        raise NotImplementedError
