import argparse
import json
import pathlib
from typing import Any, Dict

import pandas as pd

from src.data_loader import load_data
from src.quality_scorer import QualityScorer
from src.config import DEFAULT_RULES


def load_rules(path: str) -> Dict[str, Any]:
    """Load rule definitions from a JSON file.

    The JSON format must match the structure of ``DEFAULT_RULES``.
    """
    rule_path = pathlib.Path(path)
    if not rule_path.is_file():
        raise FileNotFoundError(f"Rule file not found: {path}")
    with rule_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Score data quality based on metadata rules."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input data file (CSV or JSON).",
    )
    parser.add_argument(
        "--config",
        required=False,
        help="Path to a JSON file containing custom rules.",
    )
    args = parser.parse_args()

    # Load data
    df: pd.DataFrame = load_data(args.input)

    # Load or fallback to default rules
    if args.config:
        rules = load_rules(args.config)
    else:
        rules = DEFAULT_RULES

    scorer = QualityScorer(rules)
    result = scorer.score(df)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
