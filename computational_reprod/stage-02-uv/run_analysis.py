"""Run the original Mel's Ice Cream workflow and export reproducible artifacts."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "mels-matplotlib")
)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.IceCreamRegression import run_workflow
from src.data_loader import load_and_clean_data
from src.output import plot_metric_comparison, plot_model_fits, print_ranking_summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Mel's ice-cream regression and export results."
    )
    parser.add_argument("--input", required=True, help="Input CSV path.")
    parser.add_argument("--output", required=True, help="Directory for generated artifacts.")
    parser.add_argument(
        "--predict-temperature",
        type=float,
        default=40.0,
        help="Temperature at which to predict ice-cream consumption (default: 40).",
    )
    parser.add_argument("--predictor-col", default=None)
    parser.add_argument("--target-col", default=None)
    return parser


def export_analysis(
    input_path: str,
    output_dir: str,
    prediction_temperature: float = 40.0,
    predictor_col: str | None = None,
    target_col: str | None = None,
) -> dict[str, Any]:
    """Run the unchanged scientific workflow and write its public outputs."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    results = run_workflow(
        csv_path=input_path,
        predictor_col=predictor_col,
        target_col=target_col,
        prediction_temperature=prediction_temperature,
    )
    ranking = results["ranking"]
    analysis = results["analysis"]

    ranking.ranking_table.to_csv(output / "model_ranking.csv", index=False)

    summary = {
        "input": str(input_path),
        "predictor_col": results["config"]["predictor_col"],
        "target_col": results["config"]["target_col"],
        "prediction_temperature": results["config"]["prediction_temperature"],
        "best_model": results["best_model"],
        "prediction_at_target": results["prediction_at_target"],
        "cleaning": results["cleaning"],
    }
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    cleaned = load_and_clean_data(input_path, predictor_col, target_col)
    plot_model_fits(cleaned.data, analysis, ranking, top_n=3)
    plt.savefig(output / "model_fits.png", dpi=150)
    plt.close()

    plot_metric_comparison(ranking, top_n=8)
    plt.savefig(output / "model_scores.png", dpi=150)
    plt.close()

    return results


def main() -> None:
    args = _build_parser().parse_args()
    results = export_analysis(
        input_path=args.input,
        output_dir=args.output,
        prediction_temperature=args.predict_temperature,
        predictor_col=args.predictor_col,
        target_col=args.target_col,
    )
    print_ranking_summary(results["ranking"])
    print(f"\nBest model: {results['best_model']}")
    print(f"Artifacts written to: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
