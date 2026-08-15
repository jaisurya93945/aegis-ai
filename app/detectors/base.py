from abc import ABC, abstractmethod

from app.models.findings import SecurityFinding


class Detector(ABC):
    """Base interface for all AegisAI security detectors."""

    name: str = "base"

    @abstractmethod
    def detect(self, text: str) -> list[SecurityFinding]:
        """Analyze text and return security findings."""
        raise NotImplementedError
