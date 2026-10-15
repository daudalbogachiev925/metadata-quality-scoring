"""Default metadata rules used by the quality scorer.

The structure is a dictionary where each key is a column name and the value
is another dictionary describing the validation rules for that column.
"""

DEFAULT_RULES = {
    "id": {
        "required": True,
        "completeness_weight": 2,
        "uniqueness_weight": 2,
    },
    "email": {
        "required": True,
        "regex": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$",
        "completeness_weight": 1.5,
    },
    "age": {
        "required": False,
        "allowed_values": list(range(0, 121)),  # 0‑120 years
        "completeness_weight": 1,
    },
    "country": {
        "required": True,
        "allowed_values": ["US", "CA", "GB", "DE", "FR"],
        "completeness_weight": 1,
    },
}
