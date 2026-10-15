import json
import pathlib
from typing import Any
import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """Load a CSV or JSON file into a pandas DataFrame.

    Parameters
    ----------
    file_path: str
        Path to the data file.

    Returns
    -------
    pd.DataFrame
        Loaded data.
    """
    path = pathlib.Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    elif path.suffix.lower() == ".json":
        # Assume newline‑delimited JSON objects or a list of objects
        with path.open("r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Fallback to line‑by‑line JSON objects
                f.seek(0)
                data = [json.loads(line) for line in f if line.strip()]
        df = pd.DataFrame(data)
    else:
        raise ValueError("Unsupported file type. Use .csv or .json")
    return df
