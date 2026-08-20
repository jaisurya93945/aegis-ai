import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.data.splits import load_evaluation_data
from app.ml.baseline import load_model

from sklearn.metrics import precision_score, recall_score, f1_score

def main():
    model = load_model()
    dataset = load_evaluation_data()

    thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]

    for split_name in ["validation", "test"]:
        split = dataset[split_name]

        texts = split["text"]
        labels = split["label"]

        probabilities = model.predict_proba(texts)[:, 1]

        print(f"\n=== {split_name.upper()} ===")
        print(
            f"{'Threshold':<10}"
            f"{'Precision':<12}"
            f"{'Recall':<10}"
            f"{'F1':<10}"
        )

        for threshold in thresholds:
            predictions = (probabilities >= threshold).astype(int)

            precision = precision_score(
                labels,
                predictions,
                zero_division=0,
            )

            recall = recall_score(
                labels,
                predictions,
                zero_division=0,
            )

            f1 = f1_score(
                labels,
                predictions,
                zero_division=0,
            )

            print(
                f"{threshold:<10.2f}"
                f"{precision:<12.4f}"
                f"{recall:<10.4f}"
                f"{f1:<10.4f}"
            )


if __name__ == "__main__":
    main()
