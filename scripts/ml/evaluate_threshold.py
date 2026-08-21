from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from app.data.splits import load_evaluation_data
from app.ml.baseline import DEFAULT_THRESHOLD, load_model


def evaluate(name, dataset, model, threshold):
    texts = dataset["text"]
    labels = dataset["label"]

    probabilities = model.predict_proba(texts)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        labels,
        predictions,
    ).ravel()

    accuracy = accuracy_score(labels, predictions)
    precision = precision_score(labels, predictions)
    recall = recall_score(labels, predictions)
    f1 = f1_score(labels, predictions)

    false_positive_rate = fp / (fp + tn)
    false_negative_rate = fn / (fn + tp)

    print(f"\n=== {name} ===")
    print(f"Threshold:          {threshold:.2f}")
    print(f"Samples:            {len(labels)}")
    print(f"Accuracy:           {accuracy:.4f}")
    print(f"Precision:          {precision:.4f}")
    print(f"Recall:             {recall:.4f}")
    print(f"F1:                 {f1:.4f}")
    print(f"False Positive Rate:{false_positive_rate:.4f}")
    print(f"False Negative Rate:{false_negative_rate:.4f}")

    print("\nConfusion Matrix:")
    print([[tn, fp], [fn, tp]])


def main():
    print("Loading model...")
    model = load_model()

    print("Loading evaluation datasets...")
    datasets = load_evaluation_data()

    evaluate(
        "VALIDATION",
        datasets["validation"],
        model,
        DEFAULT_THRESHOLD,
    )

    evaluate(
        "TEST",
        datasets["test"],
        model,
        DEFAULT_THRESHOLD,
    )


if __name__ == "__main__":
    main()
