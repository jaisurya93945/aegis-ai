from collections import defaultdict
from statistics import mean, median

from app.data.splits import load_evaluation_data
from app.ml.baseline import load_model


def analyze_split(name, dataset, model):
    texts = dataset["text"]
    labels = dataset["label"]

    probabilities = model.predict_proba(texts)[:, 1]

    stats = defaultdict(list)

    for label, probability in zip(labels, probabilities):
        stats[int(label)].append(float(probability))

    print(f"\n=== {name} ===")
    print(f"Samples: {len(texts)}")

    for label in sorted(stats):
        values = stats[label]

        print(f"\nLabel {label}")
        print(f"Count:   {len(values)}")
        print(f"Mean:    {mean(values):.4f}")
        print(f"Median:  {median(values):.4f}")
        print(f"Min:     {min(values):.4f}")
        print(f"Max:     {max(values):.4f}")

        for threshold in (0.30, 0.50, 0.70, 0.90):
            percentage = (
                sum(p >= threshold for p in values)
                / len(values)
                * 100
            )

            print(
                f">={threshold:.2f}: "
                f"{percentage:.2f}%"
            )


def main():
    print("Loading model...")
    model = load_model()

    print("Loading evaluation datasets...")
    evaluation = load_evaluation_data()

    analyze_split(
        "VALIDATION",
        evaluation["validation"],
        model,
    )

    analyze_split(
        "TEST",
        evaluation["test"],
        model,
    )


if __name__ == "__main__":
    main()

