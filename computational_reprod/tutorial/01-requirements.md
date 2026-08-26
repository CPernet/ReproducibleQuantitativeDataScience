# Stage 1 — venv plus `requirements.txt`

Open `stage-01-requirements` as the VS Code folder. Optionally copy it and initialize Git so every later agent change is inspectable.

## 1. Create the intended environment

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

MacOS/Linux:

```bash
 python3 -m venv .venv
 source .venv/bin/activate
 python3 -m pip install --upgrade pip
 python3 -m pip install -r requirements.txt
 ```


In VS Code, run **Python: Select Interpreter** and choose `.venv`.

## 2. Test and run

Windows PowerShell:

```powershell
python -m pytest -q
python run_analysis.py --input data/data.csv --output outputs --predict-temperature 40
```

MacOS/Linux:

```bash
python3 -m pytest -q
python run_analysis.py --input data/data.csv --output outputs --predict-temperature 40
```

The original console-only entry point still works:

```powershell
python src/IceCreamRegression.py data/data.csv
```

Inspect all four files in `outputs/`. The VS Code tasks run the same commands.

## 4. Audit the contract

- Where is Python 3.11 declared?
- Does this file record every transitive dependency?
- Does creating a venv install anything?
- What does activation change in the shell?
- Would another student know the official run command from `requirements.txt` alone?

Save the output artifacts outside this folder for comparison with stage 2.
