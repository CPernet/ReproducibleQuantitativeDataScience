# Mel's Ice Cream: from `requirements.txt` to uv to Docker

This VS Code tutorial holds one scientific analysis constant while progressively strengthening its execution environment. It uses the original project  generated in the previous lecture (agentic coding): the real 50-row dataset, four source modules, specification, and full test suite.

| Stage                     | Environment contract                                            | Main student task                                                              |
| ------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `stage-01-requirements` | A manually created venv plus old pinned packages                | Discover that`requirements.txt` does not specify Python or the run procedure |
| `stage-02-uv`           | Declared Python, project metadata, exact lock, uniform commands | Ask an agent to migrate the project and verify unchanged results               |
| `stage-03-docker`       | OS image, Python, locked dependencies, code, entry point        | Build an application used through mounted inputs and outputs                   |

## Start

1. Open this repository in VS Code.
2. Read [`tutorial/00-overview.md`](tutorial/00-overview.md).
3. Complete stages 1–3 in order.
4. Use the prompts in `prompts/` only when instructed.

Each stage uses the same command-line contract and produces four artifacts:

- `model_ranking.csv`
- `summary.json`
- `model_fits.png`
- `model_scores.png`

The original scientific modules remain under `src/`. `run_analysis.py` is a thin, headless export boundary around the original `run_workflow()` API; it does not redefine the models.

## Learning objectives

Students should be able to explain why:

- venv isolation is useful but is not a reproducibility record;
- pins in `requirements.txt` still leave the interpreter and transitive resolution procedure implicit;
- `uv.lock`, `.python-version`, and `uv run` make local reproduction less ambiguous;
- Docker packages a runnable application, not merely a Python environment;
- code, data, parameters, environment, platform, and outputs all belong in scientific provenance.

## Repository map

- `tutorial/`: student instructions and questions
- `prompts/`: constrained coding-agent prompts
- `stage-01-requirements/`: inherited project with deliberately old dependencies
- `stage-02-uv/`: reference uv migration
- `stage-03-docker/`: reference container application
- `INSTRUCTOR_GUIDE.md`: timing, expected friction, and demonstrations
