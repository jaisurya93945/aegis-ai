from app.core.engine import AegisEngine
from app.models.findings import SecurityAnalysis


class AegisService:
    """Public application service for AegisAI security analysis."""

    def __init__(self, engine: AegisEngine | None = None) -> None:
        self.engine = engine or AegisEngine()

    def analyze(self, text: str) -> SecurityAnalysis:
        """Analyze AI-related text through the AegisAI security pipeline."""
        return self.engine.analyze(text)
