from app.detectors.base import Detector
from app.ml.baseline import (
    DEFAULT_THRESHOLD,
    load_model,
    predict_with_threshold,
)
from app.models.findings import (
    FindingType,
    SecurityFinding,
    Severity,
)
from app.models.results import DetectorResult


class MLPromptInjectionDetector(Detector):
    """Detect prompt injection using the trained ML baseline."""

    name = "ml_prompt_injection"

    def __init__(self, threshold: float = DEFAULT_THRESHOLD) -> None:
        self.threshold = threshold
        self.model = load_model()

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
            findings.append(
                SecurityFinding(
                    type=FindingType.PROMPT_INJECTION,
                    severity=Severity.HIGH,
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
