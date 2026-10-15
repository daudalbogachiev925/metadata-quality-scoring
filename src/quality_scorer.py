import re
from typing import Any, Dict, List, Tuple
import pandas as pd


class QualityScorer:
    """Score a DataFrame against metadata rules.

    The scorer evaluates four aspects per column (if configured):
    - completeness (non‑null ratio)
    - uniqueness (unique values ratio)
    - allowed values (percentage of values within an allowed set)
    - regex pattern match (percentage of values matching a regex)

    Each aspect can be weighted; the final column score is the weighted
    average of the applicable aspects. The overall dataset score is the mean
    of all column scores.
    """

    def __init__(self, rules: Dict[str, Dict[str, Any]]):
        self.rules = rules

    def _score_completeness(self, series: pd.Series) -> float:
        return series.notna().mean() * 100

    def _score_uniqueness(self, series: pd.Series) -> float:
        if series.dropna().empty:
            return 0.0
        return series.nunique() / series.notna().sum() * 100

    def _score_allowed_values(self, series: pd.Series, allowed: List[Any]) -> float:
        if not allowed:
            return 100.0
        mask = series.isin(allowed) | series.isna()
        return mask.mean() * 100

    def _score_regex(self, series: pd.Series, pattern: str) -> float:
        regex = re.compile(pattern)
        def matches(val):
            if pd.isna(val):
                return True
            return bool(regex.fullmatch(str(val)))
        return pd.Series(series.map(matches)).mean() * 100

    def _evaluate_column(self, col: str, series: pd.Series) -> Tuple[float, Dict[str, float]]:
        col_rules = self.rules.get(col, {})
        components: List[Tuple[float, float]] = []  # (weight, score)
        details: Dict[str, float] = {}

        # Completeness
        comp_weight = col_rules.get("completeness_weight", 1)
        comp_score = self._score_completeness(series)
        components.append((comp_weight, comp_score))
        details["completeness"] = comp_score

        # Uniqueness
        if col_rules.get("uniqueness_weight"):
            uniq_weight = col_rules["uniqueness_weight"]
            uniq_score = self._score_uniqueness(series)
            components.append((uniq_weight, uniq_score))
            details["uniqueness"] = uniq_score

        # Allowed values
        if "allowed_values" in col_rules:
            allowed = col_rules["allowed_values"]
            allowed_score = self._score_allowed_values(series, allowed)
            # default weight = 1 if not specified
            weight = col_rules.get("allowed_values_weight", 1)
            components.append((weight, allowed_score))
            details["allowed_values"] = allowed_score

        # Regex pattern
        if "regex" in col_rules:
            pattern = col_rules["regex"]
            regex_score = self._score_regex(series, pattern)
            weight = col_rules.get("regex_weight", 1)
            components.append((weight, regex_score))
            details["regex"] = regex_score

        # Weighted average for the column
        total_weight = sum(w for w, _ in components)
        if total_weight == 0:
            column_score = 0.0
        else:
            column_score = sum(w * s for w, s in components) / total_weight
        return column_score, details

    def score(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate scores for the entire DataFrame.

        Returns a dictionary with overall score, per‑column scores and detailed
        component breakdowns.
        """
        column_results: Dict[str, Any] = {}
        scores: List[float] = []
        for col in df.columns:
            col_score, details = self._evaluate_column(col, df[col])
            column_results[col] = {
                "score": round(col_score, 2),
                "details": {k: round(v, 2) for k, v in details.items()},
            }
            scores.append(col_score)
        overall = round(sum(scores) / len(scores), 2) if scores else 0.0
        return {
            "overall_score": overall,
            "column_scores": column_results,
        }
