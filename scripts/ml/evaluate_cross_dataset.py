from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from app.data.registry import load_dataset
from app.ml.baseline import DEFAULT_THRESHOLD, load_model


def evaluate(name, dataset, model, threshold):
    texts = dataset["text"]
    labels = dataset["label"]

    probabilities = model.predict_proba(texts)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    unique_labels = sorted(set(labels))

    print(f"\n=== {name} ===")
    print(f"Samples:   {len(labels)}")
    print(f"Threshold: {threshold:.2f}")
    print(f"Labels:    {unique_labels}")

    if unique_labels == [1]:
        detected = int(predictions.sum())
        missed = len(labels) - detected
        detection_rate = detected / len(labels)

        print("Dataset type: ATTACK-ONLY")
        print(f"Detected attacks: {detected}")
        print(f"Missed attacks:   {missed}")
        print(f"Detection rate:   {detection_rate:.4f}")
        print(f"Detection rate:   {detection_rate * 100:.2f}%")

        return

    if unique_labels == [0]:
        benign_detected_as_attack = int(predictions.sum())
        false_positive_rate = (
            benign_detected_as_attack / len(labels)
        )

        print("Dataset type: BENIGN-ONLY")
        print(
            f"Benign samples classified as attack: "
            f"{benign_detected_as_attack}"
        )
        print(
            f"False positive rate: "
            f"{false_positive_rate:.4f}"
        )
        print(
            f"False positive rate: "
            f"{false_positive_rate * 100:.2f}%"
        )

        return

    tn, fp, fn, tp = confusion_matrix(
        labels,
        predictions,
        labels=[0, 1],
    ).ravel()

    accuracy = accuracy_score(labels, predictions)
    precision = precision_score(labels, predictions)
    recall = recall_score(labels, predictions)
    f1 = f1_score(labels, predictions)

    false_positive_rate = fp / (fp + tn)
    false_negative_rate = fn / (fn + tp)

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1:        {f1:.4f}")
    print(f"FPR:       {false_positive_rate:.4f}")
    print(f"FNR:       {false_negative_rate:.4f}")

    print("Confusion Matrix:")
    print([
        [int(tn), int(fp)],
        [int(fn), int(tp)],
    ])


def main():
    print("Loading model...")
    model = load_model()

    print("Loading datasets...")

    hlyn = load_dataset("hlyn")["train"]
    nemotron = load_dataset("nemotron")["train"]

    evaluate(
        "HLYN",
        hlyn,
        model,
        DEFAULT_THRESHOLD,
    )

    evaluate(
        "NEMOTRON",
        nemotron,
        model,
        DEFAULT_THRESHOLD,
    )


if __name__ == "__main__":
    main()
