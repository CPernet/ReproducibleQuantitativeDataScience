"""Tests for data loading and cleaning."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose

from src.data_loader import load_and_clean_data


@pytest.mark.parametrize(
    "predictor_col,target_col",
    [
        ("temperature [Celsius]", "ice cream [# scoops]"),
        (None, None),
    ],
)
def test_load_and_clean_removes_missing_and_negative(tmp_path, predictor_col, target_col):
    """Loader should drop missing rows and negative targets."""
    frame = pd.DataFrame(
        {
            "temperature [Celsius]": [10.0, 12.0, np.nan, 15.0],
            "ice cream [# scoops]": [1.2, -0.2, 2.0, 3.4],
        }
    )
    csv_path = tmp_path / "sample.csv"
    frame.to_csv(csv_path, index=False)

    result = load_and_clean_data(
        csv_path=str(csv_path),
        predictor_col=predictor_col,
        target_col=target_col,
    )

    assert result.rows_in == 4
    assert result.rows_after_missing_drop == 3
    assert result.rows_out == 2
    assert result.removed_missing == 1
    assert result.removed_negative == 1

    assert_allclose(
        result.data[result.predictor_col].to_numpy(dtype=float),
        np.array([10.0, 15.0]),
    )
    assert_allclose(
        result.data[result.target_col].to_numpy(dtype=float),
        np.array([1.2, 3.4]),
    )


def test_loader_infers_numeric_columns_ignoring_unnamed(tmp_path):
    """Inference should ignore unnamed index-like columns."""
    frame = pd.DataFrame(
        {
            "Unnamed: 0": [0, 1, 2],
            "temp": [5.0, 10.0, 15.0],
            "scoops": [1.0, 2.0, 3.0],
        }
    )
    csv_path = tmp_path / "inferred.csv"
    frame.to_csv(csv_path, index=False)

    result = load_and_clean_data(str(csv_path))

    assert result.predictor_col == "temp"
    assert result.target_col == "scoops"


def test_loader_raises_when_no_valid_rows_left(tmp_path):
    """All-invalid rows should raise a validation error."""
    frame = pd.DataFrame(
        {
            "temp": [np.nan, 10.0],
            "scoops": [1.0, -2.0],
        }
    )
    csv_path = tmp_path / "invalid.csv"
    frame.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="No valid rows"):
        load_and_clean_data(str(csv_path))
