from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


MODEL_PATH = Path("models/aegisai_tfidf.joblib")

# Security-oriented default selected from threshold evaluation.
# Validation F1: 0.9519
# Test F1:       0.9544
DEFAULT_THRESHOLD = 0.30


def build_model() -> Pipeline:
    """Build the AegisAI TF-IDF + Logistic Regression baseline."""

    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    min_df=2,
                    max_df=0.98,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def train_model(texts, labels) -> Pipeline:
    """Train the baseline classifier."""

    model = build_model()
    model.fit(texts, labels)

    return model


def save_model(
    model: Pipeline,
    path: Path = MODEL_PATH,
) -> None:
    """Save the trained model."""

    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(
    path: Path = MODEL_PATH,
) -> Pipeline:
    """Load a previously trained model."""

    if not path.exists():
        raise FileNotFoundError(
            f"Model not found: {path}. "
            "Train the baseline model first."
        )

    return joblib.load(path)


def predict_with_threshold(
    model: Pipeline,
    texts,
    threshold: float = DEFAULT_THRESHOLD,
):
    """
    Predict attack/benign labels using a configurable threshold.

    Returns:
        predictions: 0 = benign, 1 = attack
        probabilities: probability assigned to the attack class
    """

    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0.0 and 1.0")

    probabilities = model.predict_proba(texts)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    return predictions, probabilities
