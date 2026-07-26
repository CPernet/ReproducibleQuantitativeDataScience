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

# 3. Next we can make a plan

Using agent mode and the model you want to make a plan. (you can choose in the chat box among 'gent', 'chat', 'plan').

We are using Melanies' ice cream count to fit different regression models.

1. add spec.md to the context
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
Act as an independent test engineer. Read spec.md and inspect the implementation, but do not assume the implementation is correct. Identify missing behaviours, boundary cases, invalid inputs, and assumptions not currently tested. Add tests that would reveal plausible implementation defects. [...].
```
