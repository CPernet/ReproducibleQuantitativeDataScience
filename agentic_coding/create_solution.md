# 1. Create a folder and always version control it (it will help following what the agent is doing)

```Shell
mkdir /c/Users/adm-cyril/Downloads/MelsIceCream
cd /c/Users/adm-cyril/Downloads/MelsIceCream
git init
```

# 2. Create your context file for the agent

```Shell
touch spec.md  
echo "This repository is hosting a python code for regresion analyses and preduction based on those models. The workflow uses 3 separate instances; a data loader, a compute part taking the data frame from the loader and computing several regression models, and the export part taking the regression model outputs, to comparing and rank them, allowing user to decide which model is best." > spec.md  
cp /c/Users/adm-cyril/Downloads/ReproducibleQuantitativeDataScience/provenance/MelsIceCreamHabits.csv /c/Users/adm-cyril/Downloads/MelsIceCream/data.csv
```

# 3. Next, make a plan

Use the plan mode and the model you want (you can choose in the chat box among 'agent', 'chat', 'plan').

We are using Melanies' ice cream count to fit different regression models.

1. add spec.md to the context
2. prompt to make a plan
   ```Plain
   "Make an analysis workflow to analyse the MelsIceCreamHabits.csv - let's call it IceCreamRegression.py. The design must follow the sepc.md description. The data loader should take any file as input (but assuming column headers is ok). It should also clean the data, such as negative ice cream count is impossible. For the compute part, I want to be able to choose between many different regression models, using different polynomials (order 1,2,3), splines, with/witout interscepts, and compare them using RMSE and BIC. I need to also be able to predict non observed values, by default 40 degrees. Similalry, the default is to use all models, but this can be specified as an option. The output, part takes the regression values, compare and rank them, do plots of results and errors. Write clean code with concise numpy-style docstrings. Comment trough the code. Use litterate programming with a header for IceCreamRegression.py. For each major section explain what is happening. Write a readme file to doucument the code and usage"
   ```
3. Answer questions, add things that 'may' be needed to good programing and coding.
4. Execute the plan and git add/commit.
5. Add testing and git add/commit. The diff can help checking what has changed.
   ```Plain
   Generate unit tests for IceCreamRegression.py we just completed. Derive expected behaviour from the original requirements (spec.md), not merely from the current implementation. Include nominal cases, boundary conditions, malformed inputs, and regression cases. Use the pytest testing framework.
   ```

# 4. Add independent testing

Start a new chat. Add the context.
New prompt:

```Plain
Act as an independent test engineer. Read spec.md and inspect the implementation, but do not assume the implementation is correct. Identify missing behaviours, boundary cases, invalid inputs, and assumptions not currently tested. Add tests that would reveal plausible implementation defects. Generate tests for all methods using made up data to mach each regression model expectation and test if it works. Do not change the tests simply to make them run, unless there is a clear problem with the test itself. Generate a report on test results and make a plan for solution to implement (do not execute yet).
```
