import json
from pathlib import Path

from app.detectors.prompt_injection import PromptInjectionDetector


DATASET_PATH = Path("dataset/evaluation/baseline.jsonl")


def load_dataset(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def main() -> None:
    detector = PromptInjectionDetector()
    samples = load_dataset(DATASET_PATH)

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for sample in samples:
        findings = detector.detect(sample["text"])
        predicted = "attack" if findings else "benign"
        expected = sample["expected"]

        if expected == "attack" and predicted == "attack":
            true_positive += 1
        elif expected == "benign" and predicted == "attack":
            false_positive += 1
        elif expected == "benign" and predicted == "benign":
            true_negative += 1
        elif expected == "attack" and predicted == "benign":
            false_negative += 1

        print(
            f'{sample["id"]}: '
            f"expected={expected} "
            f"predicted={predicted}"
        )

    total = len(samples)
    correct = true_positive + true_negative
    accuracy = correct / total if total else 0.0

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive
        else 0.0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative
        else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

    print()
    print("Confusion Matrix")
    print("-----------------")
    print(f"True positives:  {true_positive}")
    print(f"False positives: {false_positive}")
    print(f"True negatives:  {true_negative}")
    print(f"False negatives: {false_negative}")

    print()
    print("Metrics")
    print("-------")
    print(f"Accuracy:  {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall:    {recall:.2%}")
    print(f"F1 score:  {f1:.2%}")


if __name__ == "__main__":
    main()
