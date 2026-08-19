from app.data.loader import load_training_data
from app.ml.baseline import train_model, save_model


def main():
    print("Loading training data...")

    dataset = load_training_data(
        include_hlyn=True,
        include_neuralchemy=True,
        include_nemotron=True,
    )

    texts = dataset["text"]
    labels = dataset["label"]

    print(f"Training samples: {len(texts)}")

    model = train_model(texts, labels)

    save_model(model)

    print("Training complete.")
    print("Model saved to: models/aegisai_tfidf.joblib")


if __name__ == "__main__":
    main()
