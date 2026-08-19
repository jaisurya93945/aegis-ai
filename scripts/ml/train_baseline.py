from time import perf_counter

from app.data.loader import load_training_data
from app.ml.baseline import train_model, save_model


def main():
    print("Loading training data...", flush=True)

    start = perf_counter()

    dataset = load_training_data(
        include_hlyn=True,
        include_neuralchemy=True,
        include_nemotron=True,
    )

    print(
        f"Loaded {len(dataset):,} training samples "
        f"in {perf_counter() - start:.1f}s",
        flush=True,
    )

    texts = dataset["text"]
    labels = dataset["label"]

    print("Starting TF-IDF + Logistic Regression training...", flush=True)
    print("This can take a while on the Chromebook.", flush=True)

    start = perf_counter()

    model = train_model(texts, labels)

    print(
        f"Training finished in {perf_counter() - start:.1f}s",
        flush=True,
    )

    print("Saving model...", flush=True)

    save_model(model)

    print(
        "Model saved to: models/aegisai_tfidf.joblib",
        flush=True,
    )


if __name__ == "__main__":
    main()
