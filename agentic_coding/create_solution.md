# 1. Create a folder and always version control it (it will help following what the agent is doing)

```Shell
mkdir /c/Users/adm-cyril/Downloads/MelsIceCream
cd /c/Users/adm-cyril/Downloads/MelsIceCream
git init
```

*Note*: the instructions and prompt below are a possible solution, there are no solution per se.

# 2. Create your context files for the agent

## Specification

The specification file is for both the agents and humans, describing what the program should do.

```Shell
touch SPEC.md  
cat >> SPEC.md <<'EOF'
# Overview
This repository is hosting a python code for regresion analyses and prediction based on those models. The workflow uses 3 separate modules; a data loader, a compute part with several regression models, and the export part to comparing and rank models, allowing user to decide which model is best.  

# Workflow

## Input
A csv file with ice cream count and temperatures

## Data loader module
load the data, check for missing value, removes negative ice cream count (impossible), output a data frame

## Analysis module
Take the data loader data frame as imput, along with options for which regression models to compute. Supported models are linear regressions (polynomials order 1,2,3), splines, and in each case with/witout intercepts. Compute models and use cross validation for prediction. Returns an object with regression results.

## Output module
Takes the regression results object as imput, and compares and ranks models, also does plots.
Model comparisons rely on average RMSE and BIC (model fit), but also average RMSE and prediction accuracy of held out sample during the cross-validation.
A file with prefix as the input file name + suffix _results.tsv should be generated, reporting all models and ranks. 

# Required behaviour
- The original input must not be modified.
- Missing values must be excluded.
- Negative ice cream count values must be removed.
- Output must inlude both model goodness and prediction accuracy.
EOF
cp /c/Users/adm-cyril/Downloads/ReproducibleQuantitativeDataScience/provenance/MelsIceCreamHabits.csv /c/Users/adm-cyril/Downloads/MelsIceCream/data.csv
```

## Agent instructions

The agent file gives instructions on how to structure the program on disk.

```Shell
touch AGENT.md  
cat >> AGENT.md <<'EOF'
# Agent instructions

## Repository structure

- Source code is under `src/`.
- Tests are under `tests/`.
- Instructions (README) is at the root`.

## Testing

- Use `pytest`.
- Name test files `test_<module>.py`.
- Prefer parametrized tests for related cases.
- Use `numpy.testing.assert_allclose` for numerical arrays.
- Every bug fix must include a regression test.
EOF
```

# 3. Next, make a plan

Use the plan mode and the model you want (you can choose in the chat box among 'agent', 'chat', 'plan').

We are using Melanies' ice cream count to fit different regression models.

1. add SPEC.md and AGENT.md to the context
2. prompt to make a plan
   ```Plain
   Make an analysis workflow to analyse the MelsIceCreamHabits.csv - let's call it IceCreamRegression.py. The workflow must follow the SPEC.md description. The design must follow the AGENT.md description. The data loader should take any file as input (but assuming column headers is ok). I need to also be able to predict non observed values, by default 40 degrees. Similalry, the default is to use all models, but this can be specified as an option. Write clean code with concise numpy-style docstrings. Comment trough the code. Use litterate programming with a header for IceCreamRegression.py. For each part of the workflow explain what is happening. Write a readme file to doucument the code and usage. Git commit once finished.
   ```
3. Answer questions, add things that 'may' be needed to good programing and coding.
4. Execute the plan and git add/commit.
5. Add testing and git add/commit. The diff can help checking what has changed.
   ```Plain
   Generate unit tests for IceCreamRegression.py we just completed. Derive expected behaviour from the original requirements (SPEC.md), not merely from the current implementation. Include nominal cases, boundary conditions, malformed inputs, and regression cases. Use the pytest testing framework. Git commit once finished.
   ```

# 4. Add independent testing

**Start a new chat** (remove in context learning). **Should you use a different model?**
New prompt:

```Plain
Act as an independent test engineer. Read SPEC.md and inspect the implementation, but do not assume the implementation is correct. Identify missing behaviours, boundary cases, invalid inputs, and assumptions not currently tested. Add tests that would reveal plausible implementation defects. Generate tests for all methods using made up data to match each regression model expectation and test if it works. Do not change the tests simply to make them run, unless there is a clear problem with the test itself. Generate a report on test results and make a plan for solution to implement (do not execute yet). Git commit once finished.
```
