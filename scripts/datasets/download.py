from pathlib import Path

from datasets import load_dataset


RAW_DIR = Path("dataset/raw")


DATASETS = {
    "neuralchemy": (
        "neuralchemy/Prompt-injection-dataset",
        "core",
    ),
    "hlyn": (
        "hlyn-labs/prompt-injection-judge-deberta-dataset",
        None,
    ),
    "nemotron": (
        "nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1",
        None,
    ),
}


def download(name: str) -> None:
    path, config = DATASETS[name]

    destination = RAW_DIR / name
    destination.mkdir(parents=True, exist_ok=True)

    print(f"Loading {name}...")
    print(f"Source: {path}")

    if config:
        dataset = load_dataset(path, config)
    else:
        dataset = load_dataset(path)

    dataset.save_to_disk(str(destination))

    print(f"Saved: {destination}")


if __name__ == "__main__":
    download("neuralchemy")
