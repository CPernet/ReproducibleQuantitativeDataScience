# 1. Create a folder and always version control it (it will help following what the agent is doing)

```Shell
mkdir /c/Users/adm-cyril/Downloads/MelsIceCream
cd /c/Users/adm-cyril/Downloads/MelsIceCream
git init
```

# 2. Create your context file for the agent

```Shell
touch spec.md  
echo "This repository is hosting a python code for regresion analyses and preduction based on those models. It uses different functions to load data, to compute each regression and to export the output, allowing user to decide which model is best." > spec.md  
cp /c/Users/adm-cyril/Downloads/ReproducibleQuantitativeDataScience/provenance/MelsIceCreamHabits.csv /c/Users/adm-cyril/Downloads/MelsIceCream/data.csv
```

# 3. Next we can make a plan

Using agent mode and the model you want to make a plan. (you can choose in the chat box among 'gent', 'chat', 'plan').

We are using Melanies' ice cream count to fit different regression models.

1. add spec.md to the context
2. prompt to make a plan
   ```Plain
   "Make an analysis workflow to analyse the MelsIceCreamHabits.csv - let's call it IceCreamRegression.py. I want to be able to choose between many different regression models, using different polynomials (1,2,3), splines, with/witout interscepts, and compare them using RMSE and BIC. I need to also be able to predict non observed values, by default 40 degrees. Similalry, the default is to use all models, but this can be specified as an option. Write clean code with concise numpy-style docstrings"
   ```
3. Answer questions, add things that 'may' be needed to good programing and coding.
4. Execute the plan and git add/commit.
5. Add testing.
   ```Plain
   Generate unit tests for IceCreamRegression.py we just completed. Derive expected behaviour from the original requirements, not merely from the current implementation. Include nominal cases, boundary conditions, malformed inputs, and regression cases. Use the pytest testing framework.
   ```

# 4. Add independent testing

Start a new chat. Add the context.
New prompt:

```Plain
Act as an independent test engineer. Read spec.md and inspect the implementation, but do not assume the implementation is correct. Identify missing behaviours, boundary cases, invalid inputs, and assumptions not currently tested. Add tests that would reveal plausible implementation defects. Generate tests for all methods using made up data to mach each regression model expectation and test if it works. Do not change the tests simply to make them run, unless there is a clear problem with the test itself. Generate a report on test results.
```
