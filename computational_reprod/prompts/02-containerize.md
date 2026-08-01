# Agent prompt: containerize the uv project

```text
Containerize this verified uv-based scientific analysis. Inspect the repository and state a short plan before editing.

Treat the image as an application with this default contract:
- read /data/input/data.csv;
- write only to /data/output;
- accept the existing CLI overrides for input, output, and prediction temperature;
- expect the input directory to be mounted read-only.

Constraints:
- Preserve data, scientific modules, tests, seed, model logic, CLI options, and these outputs: model_ranking.csv, summary.json, model_fits.png, model_scores.png.
- Install from the existing pyproject.toml and uv.lock using --frozen.
- Use Python 3.11, a multi-stage build, and a non-root runtime user.
- Keep uv, compilers, tests, teaching data, and development dependencies out of the final image.
- Add .dockerignore.
- Use ENTRYPOINT for run_analysis.py and CMD only for default arguments.
- Document PowerShell and Bash commands with separate input/output bind mounts.

Verification:
1. uv run python -m pytest -q still passes
2. docker build succeeds
3. docker run --rm IMAGE --help works
4. a mounted run creates all four files on the host
5. the input SHA-256 is unchanged
6. compare the container ranking/summary with stage 2
7. report image size and remaining limitations such as mutable base tags, architecture, and floating-point libraries

Do not weaken tests or copy the dataset into the image.
```
