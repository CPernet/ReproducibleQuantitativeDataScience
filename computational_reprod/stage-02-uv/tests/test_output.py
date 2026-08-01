"""Tests for model ranking and output behavior."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose

from src.analysis import run_regression_analysis
from src.output import DEFAULT_WEIGHTS, rank_models


def _build_sample_data(n: int = 80) -> pd.DataFrame:
    """Create synthetic data with mild nonlinearity."""
    x = np.linspace(0, 30, n)
    y = 0.04 * x**2 + 0.6 * x + 0.7 + 0.15 * np.cos(x)
    return pd.DataFrame({"temperature": x, "scoops": y})


def test_ranking_returns_expected_columns_and_best_model():
    """Ranking should expose raw metrics and weighted score."""
    data = _build_sample_data()
    analysis = run_regression_analysis(data, "temperature", "scoops")

    ranking = rank_models(analysis)
    table = ranking.ranking_table

    expected_columns = {
        "model_id",
        "train_rmse",
        "bic",
        "cv_rmse",
        "cv_accuracy",
        "prediction_at_target",
        "weighted_score",
    }
    assert expected_columns.issubset(set(table.columns))
    assert ranking.best_model_id == table.loc[0, "model_id"]
    assert_allclose(ranking.best_prediction, table.loc[0, "prediction_at_target"])


def test_custom_weights_are_supported_and_normalized():
    """Custom weights should be accepted and produce finite scores."""
    data = _build_sample_data()
    analysis = run_regression_analysis(data, "temperature", "scoops")

    custom_weights = {
        "cv_rmse": 4.0,
        "bic": 2.0,
        "train_rmse": 1.0,
        "cv_accuracy": 3.0,
    }
    ranking = rank_models(analysis, weights=custom_weights)

    assert np.isfinite(ranking.ranking_table["weighted_score"]).all()


def test_invalid_weights_raise_error():
    """Missing weight keys should trigger a validation error."""
    data = _build_sample_data()
    analysis = run_regression_analysis(data, "temperature", "scoops")

    bad_weights = {
        "cv_rmse": 1.0,
        "bic": 1.0,
        "train_rmse": 1.0,
    }
    with pytest.raises(ValueError, match="Weights must include exactly"):
        rank_models(analysis, weights=bad_weights)


def test_default_weights_sum_to_one():
    """Default weights should already sum to one."""
    assert_allclose(sum(DEFAULT_WEIGHTS.values()), 1.0)
