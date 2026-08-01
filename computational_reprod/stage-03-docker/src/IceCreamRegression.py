"""IceCreamRegression: End-to-end regression workflow for Mel's ice cream habits.

Literate Header
---------------
This script orchestrates a complete analysis pipeline with three explicit stages:

1. Data Loader
   Reads CSV data, resolves predictor/target columns, excludes missing values, and
   removes impossible negative ice cream counts.

2. Analysis
   Fits a family of regression models (polynomial and spline, with/without
   intercept), computes fit metrics (RMSE, BIC), and estimates held-out
   prediction performance via cross-validation.

3. Output
   Compares models with a weighted score built from fit and predictive metrics,
   reports the best model, and optionally creates diagnostic plots.

Design goals:
- Preserve source data integrity by operating on copied data.
- Keep model selection configurable while defaulting to all supported models.
- Predict non-observed values with a default temperature of 40 Celsius.
- Provide both importable API and command-line usage.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt

try:
    from .analysis import run_regression_analysis
    from .data_loader import load_and_clean_data
    from .output import (
        DEFAULT_WEIGHTS,
        plot_metric_comparison,
        plot_model_fits,
        print_ranking_summary,
        rank_models,
    )
except ImportError:  # pragma: no cover - direct script context
    from analysis import run_regression_analysis
    from data_loader import load_and_clean_data
    from output import (
        DEFAULT_WEIGHTS,
        plot_metric_comparison,
        plot_model_fits,
        print_ranking_summary,
        rank_models,
    )


def run_workflow(
    csv_path: str,
    predictor_col: Optional[str] = None,
    target_col: Optional[str] = None,
    models: Optional[list[str]] = None,
    prediction_temperature: float = 40.0,
    cv_folds: int = 5,
    random_state: int = 42,
    spline_knots: int = 5,
    ranking_weights: Optional[dict[str, float]] = None,
    make_plots: bool = False,
) -> dict[str, Any]:
    """Run the complete ice cream regression workflow.

    Parameters
    ----------
    csv_path : str
        Path to input CSV file.
    predictor_col : str, optional
        Predictor column to use. Inferred if omitted.
    target_col : str, optional
        Target column to use. Inferred if omitted.
    models : list[str], optional
        Specific model IDs to fit. If omitted, all models are used.
    prediction_temperature : float, default=40.0
        Temperature for non-observed prediction.
    cv_folds : int, default=5
        Number of folds for KFold cross-validation.
    random_state : int, default=42
        Reproducibility seed for CV splits.
    spline_knots : int, default=5
        Number of knots used in spline basis construction.
    ranking_weights : dict[str, float], optional
        Optional custom ranking weights.
    make_plots : bool, default=False
        If True, generate model fit and score comparison plots.

    Returns
    -------
    dict[str, Any]
        Structured workflow outputs including cleaned data metadata,
        per-model metrics, ranking table, and best-model prediction.
    """
    # Stage 1: Load and clean the raw dataset.
    load_result = load_and_clean_data(
        csv_path=csv_path,
        predictor_col=predictor_col,
        target_col=target_col,
    )

    # Stage 2: Fit all selected models and compute validation metrics.
    analysis = run_regression_analysis(
        data=load_result.data,
        predictor_col=load_result.predictor_col,
        target_col=load_result.target_col,
        models=models,
        prediction_temperature=prediction_temperature,
        cv_folds=cv_folds,
        random_state=random_state,
        spline_knots=spline_knots,
    )

    # Stage 3: Rank models using weighted fit and predictive performance.
    ranking = rank_models(
        analysis_result=analysis,
        weights=ranking_weights,
    )

    if make_plots:
        plot_model_fits(load_result.data, analysis, ranking, top_n=3)
        plot_metric_comparison(ranking, top_n=min(8, len(ranking.ranking_table)))
        plt.show()

    return {
        "config": {
            "csv_path": str(Path(csv_path)),
            "predictor_col": load_result.predictor_col,
            "target_col": load_result.target_col,
            "prediction_temperature": float(prediction_temperature),
            "cv_folds": int(cv_folds),
            "random_state": int(random_state),
            "spline_knots": int(spline_knots),
            "ranking_weights": ranking_weights or DEFAULT_WEIGHTS,
            "selected_models": analysis.selected_models,
        },
        "cleaning": {
            "rows_in": load_result.rows_in,
            "rows_after_missing_drop": load_result.rows_after_missing_drop,
            "rows_out": load_result.rows_out,
            "removed_missing": load_result.removed_missing,
            "removed_negative": load_result.removed_negative,
        },
        "analysis": analysis,
        "ranking": ranking,
        "best_model": ranking.best_model_id,
        "prediction_at_target": ranking.best_prediction,
    }


def _parse_model_list(model_text: Optional[str]) -> Optional[list[str]]:
    """Parse a comma-separated model list into normalized IDs."""
    if model_text is None or model_text.strip() == "":
        return None
    return [item.strip() for item in model_text.split(",") if item.strip()]


def _build_parser() -> argparse.ArgumentParser:
    """Create CLI parser for workflow execution."""
    parser = argparse.ArgumentParser(description="Run the Mel's Ice Cream regression workflow.")
    parser.add_argument("csv_path", help="Path to input CSV file.")
    parser.add_argument(
        "--predictor-col",
        default=None,
        help="Predictor column name. If omitted, inferred from numeric columns.",
    )
    parser.add_argument(
        "--target-col",
        default=None,
        help="Target column name. If omitted, inferred from numeric columns.",
    )
    parser.add_argument(
        "--models",
        default=None,
        help=(
            "Comma-separated model IDs. If omitted, all supported models are used. "
            "Example: poly1_intercept,spline_intercept"
        ),
    )
    parser.add_argument(
        "--prediction-temperature",
        type=float,
        default=40.0,
        help="Temperature to predict at (default: 40).",
    )
    parser.add_argument("--cv-folds", type=int, default=5, help="Number of KFold splits.")
    parser.add_argument(
        "--random-state", type=int, default=42, help="Random state for shuffled KFold."
    )
    parser.add_argument(
        "--spline-knots", type=int, default=5, help="Number of spline knots."
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="If set, create model fit and weighted score plots.",
    )
    return parser


def main() -> None:
    """Entry point for command-line usage."""
    parser = _build_parser()
    args = parser.parse_args()

    results = run_workflow(
        csv_path=args.csv_path,
        predictor_col=args.predictor_col,
        target_col=args.target_col,
        models=_parse_model_list(args.models),
        prediction_temperature=args.prediction_temperature,
        cv_folds=args.cv_folds,
        random_state=args.random_state,
        spline_knots=args.spline_knots,
        make_plots=args.plot,
    )

    ranking = results["ranking"]
    print_ranking_summary(ranking)

    print("\nData cleaning summary:")
    cleaning = results["cleaning"]
    print(
        f"Rows in: {cleaning['rows_in']}, after missing-drop: {cleaning['rows_after_missing_drop']}, "
        f"final rows: {cleaning['rows_out']} (removed missing={cleaning['removed_missing']}, "
        f"removed negative={cleaning['removed_negative']})"
    )

    print("\nBest model result:")
    print(f"Best model: {results['best_model']}")
    print(
        f"Prediction at {results['config']['prediction_temperature']} C: "
        f"{results['prediction_at_target']:.5f}"
    )


if __name__ == "__main__":
    main()
