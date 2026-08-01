"""Tests for regression analysis module."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose

from src.analysis import run_regression_analysis


def _build_sample_data(n: int = 60) -> pd.DataFrame:
    """Create deterministic synthetic data for model testing."""
    x = np.linspace(0, 30, n)
    noise = 0.05 * np.sin(x)
    y = 0.08 * x**2 + 0.4 * x + 1.2 + noise
    return pd.DataFrame({"temperature": x, "scoops": y})


def test_default_analysis_runs_all_models():
    """Default run should evaluate all supported models."""
    data = _build_sample_data()

    result = run_regression_analysis(
        data=data,
        predictor_col="temperature",
        target_col="scoops",
    )

    assert len(result.selected_models) == 8
    assert set(result.selected_models) == set(result.model_results.keys())


def test_model_subset_validation_error():
    """Unsupported model IDs should raise a clear error."""
    data = _build_sample_data()

    with pytest.raises(ValueError, match="Unsupported model"):
        run_regression_analysis(
            data=data,
            predictor_col="temperature",
            target_col="scoops",
            models=["poly1_intercept", "does_not_exist"],
        )


def test_prediction_default_temperature_is_applied():
    """Default non-observed prediction should be computed at 40 C."""
    data = _build_sample_data()

    result = run_regression_analysis(
        data=data,
        predictor_col="temperature",
        target_col="scoops",
    )

    assert result.prediction_temperature == 40.0
    for model_id in result.selected_models:
        pred = result.model_results[model_id].prediction_at_target
        assert np.isfinite(pred)


def test_cross_validation_is_deterministic_for_fixed_seed():
    """Cross-validation aggregates should be stable with fixed random state."""
    data = _build_sample_data()

    result_a = run_regression_analysis(
        data=data,
        predictor_col="temperature",
        target_col="scoops",
        random_state=7,
    )
    result_b = run_regression_analysis(
        data=data,
        predictor_col="temperature",
        target_col="scoops",
        random_state=7,
    )

    for model_id in result_a.selected_models:
        a = result_a.model_results[model_id]
        b = result_b.model_results[model_id]
        assert_allclose(a.cv_rmse_mean, b.cv_rmse_mean)
        assert_allclose(a.cv_accuracy_mean, b.cv_accuracy_mean)
