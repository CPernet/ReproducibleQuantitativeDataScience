# Agent prompt: migrate the inherited project to uv

```text
Migrate this tested scientific Python repository from a manually managed venv plus requirements.txt to uv.

First inspect SPEC.md, AGENT.md, README.md, requirements.txt, run_analysis.py, src/, tests/, and the VS Code tasks. State a short plan before editing.

Constraints:
- Preserve data/data.csv byte-for-byte.
- Preserve the current src/ layout, scientific code, cleaning rules, eight model definitions, seed, CV procedure, CLI arguments, and four output filenames.
- Do not redesign or package the analysis merely to make the migration look larger.
- Declare Python 3.11 in both project metadata and .python-version.
- Create pyproject.toml with direct runtime dependencies and a separate development dependency group.
- Generate uv.lock with uv; never hand-write it.
- Update README and VS Code tasks to use uv sync, uv run, and uv lock --check.
- Remove requirements.txt only after every direct dependency is represented.
- Never commit .venv, caches, or generated outputs.

Verification:
1. uv sync
2. uv run python -m pytest -q
3. uv run python run_analysis.py --input data/data.csv --output outputs --predict-temperature 40
4. uv lock --check
5. compare model_ranking.csv and summary.json with the pre-migration artifacts
6. report changed files, commands, and any numerical differences

If anything fails, diagnose it rather than weakening tests or changing the analysis.
```
