"""Specification-driven tests for the top-level workflow orchestrator."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_allclose

from src import IceCreamRegression as icr


def _write_nominal_csv(path: Path) -> None:
    """Write a dataset containing nominal, missing, and negative rows."""
    frame = pd.DataFrame(
        {
            "temperature [Celsius]": [
                5.0,
                7.5,
                10.0,
                12.5,
                15.0,
                17.5,
                20.0,
                22.5,
                25.0,
                27.5,
                np.nan,
                30.0,
            ],
            "ice cream [# scoops]": [
                0.8,
                1.0,
                1.3,
                1.6,
                1.9,
                2.2,
                2.6,
                3.0,
                3.3,
                3.8,
                4.0,
                -0.2,
            ],
        }
    )
    frame.to_csv(path, index=False)


def _write_small_csv(path: Path) -> None:
    """Write a dataset that becomes too small for default 5-fold CV."""
    frame = pd.DataFrame(
        {
            "temp": [5.0, 8.0, 11.0, 14.0, np.nan, 18.0],
            "scoops": [0.8, 1.1, 1.5, 1.9, 2.3, -0.1],
        }
    )
    frame.to_csv(path, index=False)


def test_run_workflow_nominal_includes_required_outputs(tmp_path):
    """Workflow should output both fit quality and predictive quality metrics."""
    csv_path = tmp_path / "nominal.csv"
    _write_nominal_csv(csv_path)

    result = icr.run_workflow(
        csv_path=str(csv_path),
        predictor_col="temperature [Celsius]",
        target_col="ice cream [# scoops]",
    )

    assert {"config", "cleaning", "analysis", "ranking", "best_model", "prediction_at_target"}.issubset(
        set(result.keys())
    )

    cleaning = result["cleaning"]
    assert cleaning["rows_in"] == 12
    assert cleaning["removed_missing"] == 1
    assert cleaning["removed_negative"] == 1
    assert cleaning["rows_out"] == 10

    assert result["config"]["prediction_temperature"] == 40.0
    assert len(result["config"]["selected_models"]) == 8

    ranking_table = result["ranking"].ranking_table
    expected_metric_columns = {
        "train_rmse",
        "bic",
        "cv_rmse",
        "cv_accuracy",
        "weighted_score",
    }
    assert expected_metric_columns.issubset(set(ranking_table.columns))

    for model_result in result["analysis"].model_results.values():
        assert np.isfinite(model_result.train_rmse)
        assert np.isfinite(model_result.bic)
        assert np.isfinite(model_result.cv_rmse_mean)
        assert np.isfinite(model_result.cv_accuracy_mean)


def test_run_workflow_allows_model_subset_and_custom_prediction_temperature(tmp_path):
    """User-specified model subset and temperature should be honored."""
    csv_path = tmp_path / "subset.csv"
    _write_nominal_csv(csv_path)

    selected = ["poly1_intercept", "spline_intercept"]
    result = icr.run_workflow(
        csv_path=str(csv_path),
        predictor_col="temperature [Celsius]",
        target_col="ice cream [# scoops]",
        models=selected,
        prediction_temperature=33.3,
    )

    assert result["config"]["selected_models"] == selected
    assert_allclose(result["config"]["prediction_temperature"], 33.3)

    ranked_models = set(result["ranking"].ranking_table["model_id"].tolist())
    assert ranked_models == set(selected)


def test_workflow_rejects_missing_csv_path():
    """Missing input file should fail with FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        icr.run_workflow("this_file_does_not_exist.csv")


def test_workflow_rejects_unknown_column_names(tmp_path):
    """Unknown predictor or target columns should produce a clear failure."""
    csv_path = tmp_path / "unknown_cols.csv"
    _write_nominal_csv(csv_path)

    with pytest.raises(ValueError, match="Predictor column"):
        icr.run_workflow(
            csv_path=str(csv_path),
            predictor_col="not_a_column",
            target_col="ice cream [# scoops]",
        )


def test_workflow_fails_when_cleaned_data_too_small_for_default_cv(tmp_path):
    """Boundary condition: rows remaining after cleaning must support 5-fold CV."""
    csv_path = tmp_path / "too_small.csv"
    _write_small_csv(csv_path)

    with pytest.raises(ValueError, match="cv_folds"):
        icr.run_workflow(csv_path=str(csv_path), predictor_col="temp", target_col="scoops")


def test_workflow_rejects_unsupported_model_identifier(tmp_path):
    """Malformed model choices should fail validation."""
    csv_path = tmp_path / "bad_model.csv"
    _write_nominal_csv(csv_path)

    with pytest.raises(ValueError, match="Unsupported model"):
        icr.run_workflow(
            csv_path=str(csv_path),
            predictor_col="temperature [Celsius]",
            target_col="ice cream [# scoops]",
            models=["poly1_intercept", "bad_model_id"],
        )


def test_original_input_file_is_not_modified(tmp_path):
    """Regression guard: running analysis must not mutate source input."""
    csv_path = tmp_path / "immutable.csv"
    _write_nominal_csv(csv_path)

    before = csv_path.read_text(encoding="utf-8")

    _ = icr.run_workflow(
        csv_path=str(csv_path),
        predictor_col="temperature [Celsius]",
        target_col="ice cream [# scoops]",
    )

    after = csv_path.read_text(encoding="utf-8")
    assert before == after


def test_make_plots_invokes_plotting_calls_when_enabled(tmp_path, monkeypatch):
    """Plot option should trigger plotting functions and show call."""
    csv_path = tmp_path / "plot.csv"
    _write_nominal_csv(csv_path)

    calls = {"fit": 0, "metric": 0, "show": 0}

    def _fit(*args, **kwargs):
        calls["fit"] += 1

    def _metric(*args, **kwargs):
        calls["metric"] += 1

    def _show(*args, **kwargs):
        calls["show"] += 1

    monkeypatch.setattr(icr, "plot_model_fits", _fit)
    monkeypatch.setattr(icr, "plot_metric_comparison", _metric)
    monkeypatch.setattr(icr.plt, "show", _show)

    icr.run_workflow(
        csv_path=str(csv_path),
        predictor_col="temperature [Celsius]",
        target_col="ice cream [# scoops]",
        make_plots=True,
    )

    assert calls == {"fit": 1, "metric": 1, "show": 1}


@pytest.mark.parametrize(
    "text,expected",
    [
        (None, None),
        ("", None),
        ("  ", None),
        ("poly1_intercept", ["poly1_intercept"]),
        (
            " poly1_intercept , spline_intercept ,, poly2_no_intercept ",
            ["poly1_intercept", "spline_intercept", "poly2_no_intercept"],
        ),
    ],
)
def test_parse_model_list(text, expected):
    """Model list parser should normalize valid comma-separated input."""
    assert icr._parse_model_list(text) == expected
