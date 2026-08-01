"""Model comparison, ranking, and plotting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from .analysis import AnalysisResult
except ImportError:  # pragma: no cover - direct script context
    from analysis import AnalysisResult


DEFAULT_WEIGHTS: dict[str, float] = {
    "cv_rmse": 0.40,
    "bic": 0.25,
    "train_rmse": 0.20,
    "cv_accuracy": 0.15,
}


@dataclass
class RankingResult:
    """Container for ranking table and best-model details."""

    ranking_table: pd.DataFrame
    best_model_id: str
    best_prediction: float


def _min_max_utility_cost(values: pd.Series) -> pd.Series:
    """Normalize a cost metric so lower values become higher utility."""
    vmin = float(values.min())
    vmax = float(values.max())
    if np.isclose(vmax, vmin):
        return pd.Series(np.ones(len(values)), index=values.index)
    return (vmax - values) / (vmax - vmin)


def _min_max_utility_benefit(values: pd.Series) -> pd.Series:
    """Normalize a benefit metric so higher values become higher utility."""
    vmin = float(values.min())
    vmax = float(values.max())
    if np.isclose(vmax, vmin):
        return pd.Series(np.ones(len(values)), index=values.index)
    return (values - vmin) / (vmax - vmin)


def _validate_weights(weights: dict[str, float]) -> dict[str, float]:
    """Validate and normalize weights to sum to one."""
    required = {"cv_rmse", "bic", "train_rmse", "cv_accuracy"}
    if set(weights.keys()) != required:
        missing = required - set(weights.keys())
        extra = set(weights.keys()) - required
        raise ValueError(
            f"Weights must include exactly {sorted(required)}. Missing={sorted(missing)} Extra={sorted(extra)}"
        )

    for key, value in weights.items():
        if value < 0:
            raise ValueError(f"Weight for {key} must be non-negative.")

    total = float(sum(weights.values()))
    if total <= 0:
        raise ValueError("At least one weight must be > 0.")

    return {k: float(v / total) for k, v in weights.items()}


def rank_models(
    analysis_result: AnalysisResult,
    weights: Optional[dict[str, float]] = None,
) -> RankingResult:
    """Rank fitted models using weighted fit and prediction metrics.

    Parameters
    ----------
    analysis_result : AnalysisResult
        Output from run_regression_analysis.
    weights : dict[str, float], optional
        Optional weight override for metrics. Keys:
        cv_rmse, bic, train_rmse, cv_accuracy.

    Returns
    -------
    RankingResult
        Ranking table and best-model summary.
    """
    use_weights = _validate_weights(weights or DEFAULT_WEIGHTS)

    records = []
    for model_id, result in analysis_result.model_results.items():
        records.append(
            {
                "model_id": model_id,
                "train_rmse": result.train_rmse,
                "bic": result.bic,
                "cv_rmse": result.cv_rmse_mean,
                "cv_accuracy": result.cv_accuracy_mean,
                "prediction_at_target": result.prediction_at_target,
            }
        )

    table = pd.DataFrame(records)

    table["u_train_rmse"] = _min_max_utility_cost(table["train_rmse"])
    table["u_bic"] = _min_max_utility_cost(table["bic"])
    table["u_cv_rmse"] = _min_max_utility_cost(table["cv_rmse"])
    table["u_cv_accuracy"] = _min_max_utility_benefit(table["cv_accuracy"])

    table["weighted_score"] = (
        use_weights["train_rmse"] * table["u_train_rmse"]
        + use_weights["bic"] * table["u_bic"]
        + use_weights["cv_rmse"] * table["u_cv_rmse"]
        + use_weights["cv_accuracy"] * table["u_cv_accuracy"]
    )

    # Use deterministic metric-based tie-breakers after weighted score.
    table = table.sort_values(
        by=[
            "weighted_score",
            "cv_rmse",
            "bic",
            "train_rmse",
            "cv_accuracy",
            "model_id",
        ],
        ascending=[False, True, True, True, False, True],
    ).reset_index(drop=True)

    best_model = str(table.loc[0, "model_id"])
    best_pred = float(table.loc[0, "prediction_at_target"])

    return RankingResult(
        ranking_table=table,
        best_model_id=best_model,
        best_prediction=best_pred,
    )


def print_ranking_summary(ranking: RankingResult, top_n: int = 8) -> None:
    """Print a compact console summary of ranked models."""
    preview = ranking.ranking_table.head(top_n).copy()
    keep = [
        "model_id",
        "weighted_score",
        "cv_rmse",
        "cv_accuracy",
        "bic",
        "train_rmse",
        "prediction_at_target",
    ]
    print("\nModel ranking (best first):")
    print(preview[keep].to_string(index=False, float_format=lambda x: f"{x:0.5f}"))


def plot_model_fits(
    data: pd.DataFrame,
    analysis_result: AnalysisResult,
    ranking: RankingResult,
    top_n: int = 3,
) -> None:
    """Plot observed data and fitted curves for top-ranked models."""
    predictor = analysis_result.predictor_col
    target = analysis_result.target_col

    x = data[predictor].to_numpy(dtype=float)
    y = data[target].to_numpy(dtype=float)

    x_line = np.linspace(float(np.min(x)), float(np.max(x)), 200)
    x_line_2d = x_line.reshape(-1, 1)

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=28, alpha=0.65, label="Observed")

    top_ids = ranking.ranking_table["model_id"].head(top_n).tolist()
    for model_id in top_ids:
        estimator = analysis_result.model_results[model_id].estimator
        y_hat = estimator.predict(x_line_2d)
        plt.plot(x_line, y_hat, linewidth=2, label=model_id)

    plt.title("Observed Data and Top Model Fits")
    plt.xlabel(predictor)
    plt.ylabel(target)
    plt.legend()
    plt.tight_layout()


def plot_metric_comparison(ranking: RankingResult, top_n: int = 8) -> None:
    """Plot weighted scores for top-ranked models."""
    preview = ranking.ranking_table.head(top_n)

    plt.figure(figsize=(10, 6))
    plt.bar(preview["model_id"], preview["weighted_score"])
    plt.title("Weighted Model Score Comparison")
    plt.xlabel("Model")
    plt.ylabel("Weighted Score")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
