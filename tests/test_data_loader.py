import pathlib
import pandas as pd
import tempfile
import json

from src.data_loader import load_data


def test_load_csv(tmp_path: pathlib.Path):
    csv_content = "id,name\n1,Alpha\n2,Beta\n"
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    df = load_data(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "name"]
    assert df.shape[0] == 2


def test_load_json_array(tmp_path: pathlib.Path):
    data = [{"id": 1, "value": "x"}, {"id": 2, "value": "y"}]
    json_file = tmp_path / "sample.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")
    df = load_data(str(json_file))
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["id", "value"]
    assert df.shape[0] == 2


def test_load_json_lines(tmp_path: pathlib.Path):
    lines = [json.dumps({"id": i, "val": chr(65 + i)}) for i in range(3)]
    jsonl_file = tmp_path / "sample.jsonl"
    jsonl_file.write_text("\n".join(lines), encoding="utf-8")
    df = load_data(str(jsonl_file))
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 3
    assert "val" in df.columns
