import json
from collections import Counter
from pathlib import Path


REPORT_PATH = Path(
    "dataset/reports/neuralchemy_near_duplicates.json"
)


def main() -> None:
    with REPORT_PATH.open("r", encoding="utf-8") as file:
        report = json.load(file)

    matches = report["matches"]

    print("AegisAI Near-Duplicate Analysis")
    print("===============================")

    print(f"Total potential matches: {len(matches)}")

    split_pairs = Counter(
        f"{match['split_a']} -> {match['split_b']}"
        for match in matches
    )

    print("\nMatches by split pair")
    print("---------------------")

    for pair, count in split_pairs.items():
        print(f"{pair}: {count}")

    similarity_buckets = Counter()

    for match in matches:
        score = match["similarity"]

        if score >= 99:
            bucket = "99-100"
        elif score >= 98:
            bucket = "98-98.99"
        elif score >= 97:
            bucket = "97-97.99"
        elif score >= 96:
            bucket = "96-96.99"
        else:
            bucket = "95-95.99"

        similarity_buckets[bucket] += 1

    print("\nSimilarity distribution")
    print("-----------------------")

    for bucket in [
        "99-100",
        "98-98.99",
        "97-97.99",
        "96-96.99",
        "95-95.99",
    ]:
        print(f"{bucket}: {similarity_buckets[bucket]}")

    print("\nTop 10 strongest matches")
    print("------------------------")

    strongest = sorted(
        matches,
        key=lambda match: match["similarity"],
        reverse=True,
    )

    for match in strongest[:10]:
        print(
            f"\nSimilarity: {match['similarity']}"
        )
        print(
            f"{match['split_a']}[{match['index_a']}]: "
            f"{match['text_a']}"
        )
        print(
            f"{match['split_b']}[{match['index_b']}]: "
            f"{match['text_b']}"
        )


if __name__ == "__main__":
    main()
