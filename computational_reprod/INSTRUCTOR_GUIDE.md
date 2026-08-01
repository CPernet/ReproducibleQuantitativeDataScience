# Instructor guide

## Suggested 75–90 minute session

| Time | Activity | Teaching point |
| ---: | --- | --- |
| 10 min | Inspect the inherited repository and run the original CLI | Reproducibility concerns an entire computation, not only source code |
| 15 min | Diagnose and repair stage 1 | A venv isolates packages; `requirements.txt` does not select Python |
| 20 min | Agent-assisted migration to uv | A good migration prompt constrains scope and requires evidence |
| 10 min | Compare stage-1 and stage-2 artifacts | The environment changed; data, code, parameters, and results did not |
| 20 min | Build and run the container | The public interface becomes input + parameters → outputs |
| 10 min | Provenance discussion | Neither a lock nor a container identifies a complete scientific run |

## Preparation

Install VS Code, Git, Python 3.11, uv, and Docker Desktop. On Windows, use the same PowerShell terminal throughout. Pre-build the image if classroom bandwidth is limited.

## Intended stage-1 friction

The inherited `requirements.txt` pins a Python-3.11-era numerical stack. Installation under Python 3.12–3.14 may fail because compatible wheels are unavailable. Allow roughly five minutes for diagnosis:

```powershell
python --version
python -m pip install -r requirements.txt
```

Then expose the missing contract: the file never states which Python to use. Recover with `py -3.11 -m venv .venv`. Do not let this become a compiler exercise.

## Demonstration checkpoints

At all three stages, use the supplied `data/data.csv` and prediction temperature 40. Compare:

- the eight rows and ordering in `model_ranking.csv`;
- the best model and prediction in `summary.json`;
- the two plots;
- the unchanged SHA-256 of `data/data.csv`.

The source archive had 46 original tests. The tutorial adds one integration test for the export boundary, so each stage should report 47 passing tests.

For the Docker demonstration, remove or rename the host `.venv` before running the image. Only Docker, the mounted CSV, the parameters, and an output directory are needed.

## Discussion prompts

1. Does `uv.lock` guarantee bitwise-identical floating-point output on every architecture?
2. What remains mutable when the Dockerfile uses `python:3.11-slim` instead of an image digest?
3. Why is the dataset mounted instead of baked into the image?
4. What is gained—and lost—when users interact only through the container entry point?
5. Which identifiers are needed to cite one exact run?
