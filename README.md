# Metadata‑Driven Data Quality Scoring System

This repository provides a lightweight, metadata‑driven data quality scoring engine written in Python. It evaluates datasets (CSV/JSON) against configurable rules (completeness, uniqueness, allowed values, regex patterns) and produces a quantitative score (0‑100) useful for regulated industries.

## Features
- **Rule‑based scoring** – Define per‑column rules in a simple Python dictionary or external JSON file.
- **Multiple data sources** – Load CSV or JSON files directly.
- **Extensible** – Add new rule types by extending `QualityScorer`.
- **CLI** – Run the scorer from the command line.
- **Test suite** – Unit tests with `pytest`.

## Quick Start
```bash
# Clone the repo
git clone https://github.com/youruser/metadata-quality-scoring.git
cd metadata-quality-scoring

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the scorer on a sample CSV
python -m src.main --input data/sample.csv
```

You can also supply a custom rule file:
```bash
python -m src.main --input data/sample.csv --config config/custom_rules.json
```

## Development
### Running tests
```bash
pip install -r requirements.txt
pytest
```

### Adding new rules
Edit `src/config.py` or provide a JSON file with the same structure. Each column can contain any of the following keys:
- `required`: `true`/`false` – column must be present.
- `completeness_weight`: numeric (default 1).
- `uniqueness_weight`: numeric (default 1).
- `allowed_values`: list of permissible values.
- `regex`: regular expression pattern that values must match.

The scorer combines the weighted results into a column score and averages them for an overall dataset score.

## License
MIT License
