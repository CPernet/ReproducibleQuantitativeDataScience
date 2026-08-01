"""Model fitting and cross-validation for ice cream regression."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer


def mae_to_accuracy(mae_value: float) -> float:
    """Convert MAE into a bounded accuracy score in (0, 1]."""
    return 1.0 / (1.0 + float(mae_value))


@dataclass
class ModelResult:
    """Per-model regression and validation output.

    Attributes
    ----------
    model_id : str
        Stable identifier for the fitted model.
    estimator : Any
        Fitted estimator object used for inference.
    train_rmse : float
        Root-mean-squared error on full cleaned data.
    bic : float
        Bayesian Information Criterion on full cleaned data.
    cv_rmse_mean : float
        Mean RMSE across held-out CV folds.
    cv_rmse_std : float
        Standard deviation of held-out RMSE across folds.
    cv_accuracy_mean : float
        Mean MAE-based accuracy across held-out CV folds.
    cv_accuracy_std : float
        Standard deviation of MAE-based accuracy across folds.
    prediction_at_target : float
        Predicted target value at the requested temperature.
    n_parameters : int
        Effective number of linear parameters in the model.
    fold_rmse : list[float]
        RMSE values, one per CV fold.
    fold_accuracy : list[float]
        MAE-based accuracy values, one per CV fold.
    """

    model_id: str
    estimator: Any
    train_rmse: float
    bic: float
    cv_rmse_mean: float
    cv_rmse_std: float
    cv_accuracy_mean: float
    cv_accuracy_std: float
    prediction_at_target: float
    n_parameters: int
    fold_rmse: list[float]
    fold_accuracy: list[float]


@dataclass
class AnalysisResult:
    """Full analysis output covering all selected models."""

    predictor_col: str
    target_col: str
    prediction_temperature: float
    cv_folds: int
    random_state: int
    selected_models: list[str]
    model_results: dict[str, ModelResult]


ModelBuilder = Callable[[], Any]


def _build_poly_model(degree: int, fit_intercept: bool) -> Pipeline:
    """Create a polynomial regression pipeline."""
    return Pipeline(
        steps=[
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("model", LinearRegression(fit_intercept=fit_intercept)),
        ]
    )


def _build_spline_model(fit_intercept: bool, n_knots: int) -> Pipeline:
    """Create a spline-basis regression pipeline with intercept control."""
    return Pipeline(
        steps=[
            (
                "spline",
                SplineTransformer(
                    n_knots=n_knots,
                    degree=3,
                    include_bias=False,
                ),
            ),
            ("model", LinearRegression(fit_intercept=fit_intercept)),
        ]
    )


def _count_parameters(estimator: Any) -> int:
    """Count model parameters for BIC (including intercept when fitted)."""
    if isinstance(estimator, Pipeline):
        lr = estimator.named_steps["model"]
    else:
        lr = estimator

    coef_count = int(np.size(lr.coef_))
    intercept_count = 1 if np.size(lr.intercept_) > 0 and lr.fit_intercept else 0
    return coef_count + intercept_count


def _compute_bic(y_true: np.ndarray, y_pred: np.ndarray, n_params: int) -> float:
    """Compute BIC from residual sum of squares."""
    residuals = y_true - y_pred
    rss = float(np.sum(residuals**2))
    n_samples = y_true.shape[0]
    rss = max(rss, 1e-12)
    return float(n_samples * np.log(rss / n_samples) + n_params * np.log(n_samples))


def supported_model_builders(spline_knots: int = 5) -> dict[str, ModelBuilder]:
    """Return all supported model builders keyed by stable IDs."""
    return {
        "poly1_intercept": lambda: _build_poly_model(1, True),
        "poly1_no_intercept": lambda: _build_poly_model(1, False),
        "poly2_intercept": lambda: _build_poly_model(2, True),
        "poly2_no_intercept": lambda: _build_poly_model(2, False),
        "poly3_intercept": lambda: _build_poly_model(3, True),
        "poly3_no_intercept": lambda: _build_poly_model(3, False),
        "spline_intercept": lambda: _build_spline_model(True, spline_knots),
        "spline_no_intercept": lambda: _build_spline_model(False, spline_knots),
    }


def _resolve_selected_models(
    requested_models: Optional[list[str]],
    available: dict[str, ModelBuilder],
) -> list[str]:
    """Validate and resolve selected model IDs."""
    if requested_models is None or len(requested_models) == 0:
        return list(available.keys())

    unsupported = sorted(set(requested_models) - set(available.keys()))
    if unsupported:
        available_text = ", ".join(sorted(available.keys()))
        bad_text = ", ".join(unsupported)
        raise ValueError(
            f"Unsupported model(s): {bad_text}. Supported models are: {available_text}."
        )

    return requested_models


def run_regression_analysis(
    data: pd.DataFrame,
    predictor_col: str,
    target_col: str,
    models: Optional[list[str]] = None,
    prediction_temperature: float = 40.0,
    cv_folds: int = 5,
    random_state: int = 42,
    spline_knots: int = 5,
) -> AnalysisResult:
    """Fit selected regression models and compute fit/CV metrics.

    Parameters
    ----------
    data : pandas.DataFrame
        Cleaned input data.
    predictor_col : str
        Predictor column name.
    target_col : str
        Target column name.
    models : list[str], optional
        Model IDs to fit. If omitted, all supported models are used.
    prediction_temperature : float, default=40.0
        Temperature value used for non-observed prediction.
    cv_folds : int, default=5
        Number of KFold splits.
    random_state : int, default=42
        Seed used when shuffling KFold splits.
    spline_knots : int, default=5
        Number of knots used by spline models.

    Returns
    -------
    AnalysisResult
        Structured model outputs for ranking and reporting.
    """
    if cv_folds < 2:
        raise ValueError("cv_folds must be at least 2.")
    if len(data) < cv_folds:
        raise ValueError("Number of rows must be >= cv_folds for cross-validation.")

    available = supported_model_builders(spline_knots=spline_knots)
    selected_models = _resolve_selected_models(models, available)

    X = data[[predictor_col]].to_numpy(dtype=float)
    y = data[target_col].to_numpy(dtype=float)

    cv = KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)

    results: dict[str, ModelResult] = {}

    for model_id in selected_models:
        estimator = available[model_id]()
        estimator.fit(X, y)

        train_pred = estimator.predict(X)
        train_rmse = float(np.sqrt(mean_squared_error(y, train_pred)))
        n_params = _count_parameters(estimator)
        bic = _compute_bic(y, train_pred, n_params)

        fold_rmse: list[float] = []
        fold_accuracy: list[float] = []

        for train_idx, test_idx in cv.split(X):
            fold_estimator = clone(estimator)
            fold_estimator.fit(X[train_idx], y[train_idx])
            fold_pred = fold_estimator.predict(X[test_idx])

            rmse = float(np.sqrt(mean_squared_error(y[test_idx], fold_pred)))
            mae = float(mean_absolute_error(y[test_idx], fold_pred))
            accuracy = mae_to_accuracy(mae)

            fold_rmse.append(rmse)
            fold_accuracy.append(accuracy)

        pred_temp = float(
            estimator.predict(np.array([[prediction_temperature]], dtype=float))[0]
        )

        results[model_id] = ModelResult(
            model_id=model_id,
            estimator=estimator,
            train_rmse=train_rmse,
            bic=bic,
            cv_rmse_mean=float(np.mean(fold_rmse)),
            cv_rmse_std=float(np.std(fold_rmse, ddof=0)),
            cv_accuracy_mean=float(np.mean(fold_accuracy)),
            cv_accuracy_std=float(np.std(fold_accuracy, ddof=0)),
            prediction_at_target=pred_temp,
            n_parameters=n_params,
            fold_rmse=fold_rmse,
            fold_accuracy=fold_accuracy,
        )

    return AnalysisResult(
        predictor_col=predictor_col,
        target_col=target_col,
        prediction_temperature=float(prediction_temperature),
        cv_folds=cv_folds,
        random_state=random_state,
        selected_models=selected_models,
        model_results=results,
    )
