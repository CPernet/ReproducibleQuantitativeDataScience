"""Data loading and cleaning utilities for the ice cream workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class DataLoadResult:
    """Container for cleaned data and audit metadata.

    Attributes
    ----------
    data : pandas.DataFrame
        Cleaned dataframe containing only predictor and target columns.
    predictor_col : str
        Name of the predictor column (temperature).
    target_col : str
        Name of the target column (ice cream count).
    rows_in : int
        Number of rows before cleaning.
    rows_after_missing_drop : int
        Number of rows after removing missing values.
    rows_out : int
        Number of rows after all cleaning steps.
    removed_missing : int
        Number of rows removed because of missing values.
    removed_negative : int
        Number of rows removed because target value was negative.
    """

    data: pd.DataFrame
    predictor_col: str
    target_col: str
    rows_in: int
    rows_after_missing_drop: int
    rows_out: int
    removed_missing: int
    removed_negative: int


def _candidate_numeric_columns(frame: pd.DataFrame) -> list[str]:
    """Return column names that can be interpreted as numeric."""
    candidates: list[str] = []
    for col in frame.columns:
        # Skip typical unnamed index columns produced by CSV exports.
        if str(col).lower().startswith("unnamed"):
            continue
        converted = pd.to_numeric(frame[col], errors="coerce")
        if converted.notna().any():
            candidates.append(col)
    return candidates


def _resolve_columns(
    frame: pd.DataFrame,
    predictor_col: Optional[str],
    target_col: Optional[str],
) -> tuple[str, str]:
    """Resolve predictor and target column names."""
    if predictor_col is not None and predictor_col not in frame.columns:
        raise ValueError(f"Predictor column '{predictor_col}' was not found in the CSV.")
    if target_col is not None and target_col not in frame.columns:
        raise ValueError(f"Target column '{target_col}' was not found in the CSV.")

    if predictor_col and target_col:
        if predictor_col == target_col:
            raise ValueError("Predictor and target columns must be different.")
        return predictor_col, target_col

    candidates = _candidate_numeric_columns(frame)
    if len(candidates) < 2:
        raise ValueError(
            "Unable to infer predictor/target columns: CSV needs at least two numeric columns."
        )

    resolved_predictor = predictor_col or candidates[0]
    resolved_target = target_col or next((c for c in candidates if c != resolved_predictor), None)

    if resolved_target is None:
        raise ValueError("Could not resolve a distinct target column.")

    return resolved_predictor, resolved_target


def load_and_clean_data(
    csv_path: str,
    predictor_col: Optional[str] = None,
    target_col: Optional[str] = None,
) -> DataLoadResult:
    """Load and clean ice cream data from CSV.

    Parameters
    ----------
    csv_path : str
        Path to the input CSV file.
    predictor_col : str, optional
        Predictor column name. If omitted, the first numeric column is used.
    target_col : str, optional
        Target column name. If omitted, the next numeric column is used.

    Returns
    -------
    DataLoadResult
        Cleaned data and row-removal audit metadata.

    Raises
    ------
    FileNotFoundError
        If the CSV path does not exist.
    ValueError
        If columns cannot be resolved or no valid rows remain after cleaning.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file was not found: {csv_path}")

    raw_frame = pd.read_csv(path)
    predictor, target = _resolve_columns(raw_frame, predictor_col, target_col)

    # Work on a detached copy so source data loaded from disk is never mutated in-place.
    selected = raw_frame[[predictor, target]].copy(deep=True)
    selected[predictor] = pd.to_numeric(selected[predictor], errors="coerce")
    selected[target] = pd.to_numeric(selected[target], errors="coerce")

    rows_in = int(len(selected))

    selected_non_missing = selected.dropna(subset=[predictor, target]).copy(deep=True)
    rows_after_missing_drop = int(len(selected_non_missing))

    selected_non_negative = selected_non_missing[selected_non_missing[target] >= 0].copy(deep=True)
    rows_out = int(len(selected_non_negative))

    removed_missing = rows_in - rows_after_missing_drop
    removed_negative = rows_after_missing_drop - rows_out

    if rows_out == 0:
        raise ValueError("No valid rows left after removing missing and negative target values.")

    return DataLoadResult(
        data=selected_non_negative,
        predictor_col=predictor,
        target_col=target,
        rows_in=rows_in,
        rows_after_missing_drop=rows_after_missing_drop,
        rows_out=rows_out,
        removed_missing=removed_missing,
        removed_negative=removed_negative,
    )
