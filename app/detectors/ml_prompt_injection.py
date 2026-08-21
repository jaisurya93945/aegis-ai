from pathlib import Path

from app.detectors.base import Detector
from app.ml.baseline import (
    DEFAULT_THRESHOLD,
    load_model,
    predict_with_threshold,
)
from app.models.findings import (
    FindingType,
    FindingSource,
    SecurityFinding,
    Severity,
)
from app.models.results import DetectorResult


V2_MODEL_PATH = Path("models/aegisai_tfidf_v2.joblib")


class MLPromptInjectionDetector(Detector):
    """Detect prompt injection using the trained AegisAI ML model."""

    name = "ml_prompt_injection"

    def __init__(
        self,
        threshold: float = DEFAULT_THRESHOLD,
        model_path: Path = V2_MODEL_PATH,
    ) -> None:
        self.threshold = threshold
        self.model_path = model_path
        self.model = load_model(model_path)

    def detect(self, text: str) -> DetectorResult:
        """Analyze text using the trained ML classifier."""

        predictions, probabilities = predict_with_threshold(
            self.model,
            [text],
            threshold=self.threshold,
        )

        prediction = int(predictions[0])
        probability = float(probabilities[0])

        findings: list[SecurityFinding] = []

        if prediction == 1:
            if probability >= 0.90:
                severity = Severity.HIGH
            elif probability >= 0.70:
                severity = Severity.MEDIUM
            else:
                severity = Severity.LOW

            findings.append(
                SecurityFinding(
                    type=FindingType.PROMPT_INJECTION,
                    severity=severity,
                    source=FindingSource.ML,
                    description=(
                        "ML detector identified the input as a likely "
                        "prompt injection."
                    ),
                    evidence=f"ml_probability={probability:.4f}",
                )
            )

        return DetectorResult(
            detector=self.name,
            findings=findings,
        )
