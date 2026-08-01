"""Tests for the thin artifact-export boundary used by all three stages."""

from pathlib import Path

import pandas as pd

from run_analysis import export_analysis


def test_export_analysis_writes_expected_artifacts(tmp_path: Path):
    input_path = Path(__file__).parents[1] / "data" / "data.csv"

    results = export_analysis(str(input_path), str(tmp_path), 40.0)

    assert results["cleaning"]["rows_in"] == 50
    assert results["cleaning"]["removed_negative"] == 1
    expected = {
        "model_ranking.csv",
        "summary.json",
        "model_fits.png",
        "model_scores.png",
    }
    assert {path.name for path in tmp_path.iterdir()} == expected
    ranking = pd.read_csv(tmp_path / "model_ranking.csv")
    assert len(ranking) == 8
    assert ranking.loc[0, "model_id"] == results["best_model"]
