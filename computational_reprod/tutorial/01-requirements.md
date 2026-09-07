# Preparation

Whatever the names of your output folder or files of the agnetic-coding exercise were, rename them manually to "*_original*" or copy them in a separate folder with that name.

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

# for python3.12 use other requirements:

```bash
 python3 -m venv .venv
 source .venv/bin/activate
 python3 -m pip install --upgrade pip
 python3 -m pip install -r requirements_py312.txt
```


In VS Code, press Ctrl+Shift+P, run **Python: Select Interpreter** and choose `.venv`.

## 2. Test and run

Note you might need to modify the call to the "IceCreamRegression.py" file depending on where your earlier decisions have located it and how it should be called. Below there is just some examples:

Windows PowerShell:

```powershell
python -m pytest -q
python src/IceCreamRegression.py MelsIceCreamHabits.csv
python src/IceCreamRegression.py data/data.csv --models poly1_intercept --prediction-temperature 40
python run_analysis.py --input data/data.csv --output /outputs --predict-temperature 40
```

MacOS/Linux:

```bash
python3 -m pytest -q
python src/IceCreamRegression.py data/data.csv
python src/IceCreamRegression.py data/data.csv --models poly1_intercept --prediction-temperature 40
python run_analysis.py --input data/data.csv --output outputs --predict-temperature 40
```

The original console-only running of the code should also still work:

```powershell
python src/IceCreamRegression.py MelsIceCreamHabits.csv
```

Inspect all four files output files, the original ones and the recent ones. 

## 4. Audit the contract

- Where is Python declared?
- Does this file record every transitive dependency?
- Does creating a venv install anything?
- What does activation change in the shell?
- Would another student know the official run command from `requirements.txt` alone?

Rename all new outputs to "*_requirements*" or save the outputs in a separate folder for comparison with stage 2.
