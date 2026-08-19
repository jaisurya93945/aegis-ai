from app.data.splits import load_evaluation_data
from app.ml.baseline import load_model

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def evaluate(name, dataset, model):
    texts = dataset["text"]
    labels = dataset["label"]

    predictions = model.predict(texts)

    print(f"\n=== {name.upper()} ===")
    print(f"Samples: {len(labels):,}")
    print(f"Accuracy:  {accuracy_score(labels, predictions):.4f}")
    print(f"Precision: {precision_score(labels, predictions, zero_division=0):.4f}")
    print(f"Recall:    {recall_score(labels, predictions, zero_division=0):.4f}")
    print(f"F1:        {f1_score(labels, predictions, zero_division=0):.4f}")

    print("\nConfusion Matrix:")
    print(confusion_matrix(labels, predictions))

    print("\nClassification Report:")
    print(classification_report(labels, predictions, zero_division=0))


def main():
    print("Loading model...")
    model = load_model()

    print("Loading evaluation datasets...")
    dataset = load_evaluation_data()

    evaluate("validation", dataset["validation"], model)
    evaluate("test", dataset["test"], model)


if __name__ == "__main__":
    main()
