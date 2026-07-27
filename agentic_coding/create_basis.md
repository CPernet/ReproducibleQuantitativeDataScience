# 1. Create a folder and always version control it (it will help following what the agent is doing)

```Shell
mkdir /c/Users/adm-cyril/Downloads/MelsIceCream
cd /c/Users/adm-cyril/Downloads/MelsIceCream
git init
```

*Note*: below are snippets of instructions and prompts - complete them replacing [...] by something meaningful given the IceCream dataset we previously analyzed.

# 2. Create your context files for the agent

## Specification

The specification file is for both the agents and humans, describing what the program should do.

```Shell
touch SPEC.md  
cat >> SPEC.md <<'EOF'
# Overview
This repository is hosting a python code for regresion analyses and prediction based on those models. The workflow [...].  

# Workflow

## Input
A csv file with ice cream count and temperatures

[...]

# Required behaviour
- The original input must not be modified.
- Missing values must be excluded.
[...]

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
   "Make an analysis workflow to analyse the MelsIceCreamHabits.csv - let's call it IceCreamRegression.py. I want [...]"
   ```
3. Answer questions, add things that 'may' be needed to good programing and coding.
4. Execute the plan and git add/commit.
5. Add testing.
   ```Plain
   Generate unit tests for IceCreamRegression.py we just completed. [...]. Use the pytest testing framework.
   ```

# 4. Add independent testing

Start a new chat. Add the context.
New prompt:

```Plain
Act as an independent test engineer. Read SPEC.md and inspect the implementation, but do not assume the implementation is correct. Identify missing behaviours, boundary cases, invalid inputs, and assumptions not currently tested. Add tests that would reveal plausible implementation defects. [...].
```
