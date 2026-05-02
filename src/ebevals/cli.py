import json
import argparse
from pathlib import Path


def load_trial(path):
    with open(path, 'r') as f:
        return json.load(f)


def run_trial(trial):
    print("=== TRIAL ===")
    print("ID:", trial["id"])
    print("\n--- T (visible prompt) ---\n")
    print(trial["task"]["T"])
    print("\n--- E (hidden evidence) ---\n")
    print("(hidden from blind model)")

    print("\n[Placeholder] Call model A with T only")
    print("[Placeholder] Capture answer A")

    print("\n[Placeholder] Call model B with T + E + A")
    print("[Placeholder] Perform claim-level audit")

    print("\n--- Expected (for human inspection) ---\n")
    print("Tempting unwarranted answer:")
    print(trial["expected"]["tempting_unwarranted_answer"])
    print("\nCareful behavior:")
    print(trial["expected"]["careful_behavior"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", required=True, help="Path to trial JSON")
    args = parser.parse_args()

    trial = load_trial(args.trial)
    run_trial(trial)


if __name__ == "__main__":
    main()
