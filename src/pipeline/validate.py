# src/pipeline/validate.py

"""
Stage 4: Data Validation.

Validates schema, missing values, data types, and feature ranges.
"""

import argparse
import logging

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("validate")


REQUIRED_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "species",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]


def validate_data(input_path: str) -> bool:
    df = pd.read_csv(input_path)

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        logger.error(
            "Validation FAILED: missing columns: %s",
            missing_columns
        )
        return False

    # Check for missing values
    if df[REQUIRED_COLUMNS].isnull().any().any():
        logger.error("Validation FAILED: missing values found")
        return False

    # Check numeric ranges
    range_rules = {
        "sepal length (cm)": (4.0, 8.0),
        "sepal width (cm)": (1.5, 5.0),
        "petal length (cm)": (1.0, 7.0),
        "petal width (cm)": (0.1, 3.0),
    }

    for column, (minimum, maximum) in range_rules.items():
        if not df[column].between(minimum, maximum).all():
            logger.error(
                "Validation FAILED: range check failed for '%s'",
                column
            )
            return False

    # Check target values
    valid_species = {"setosa", "versicolor", "virginica"}

    if not set(df["species"].unique()).issubset(valid_species):
        logger.error("Validation FAILED: invalid species values")
        return False

    logger.info(
        "Validation PASSED: %d rows, %d columns, all checks satisfied",
        len(df),
        len(df.columns)
    )

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="data/processed/iris_features.csv"
    )

    args = parser.parse_args()

    success = validate_data(args.input)

    if not success:
        raise SystemExit(1)