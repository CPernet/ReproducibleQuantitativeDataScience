# 1. Create a folder and always version control it (it will help following what the agent is doing)

```Shell
mkdir /c/Users/adm-cyril/Downloads/MelsIceCream
cd /c/Users/adm-cyril/Downloads/MelsIceCream
git init
```

# 2. Create your context file for the agent

```Shell
touch repo_context.md  
echo "This repository is hosting a python code for regresion analyses. It uses different functions to load data, compute and export the output." > repo_context.md  
cp /c/Users/adm-cyril/Downloads/ReproducibleQuantitativeDataScience/provenance/MelsIceCreamHabits.csv /c/Users/adm-cyril/Downloads/MelsIceCream/data.csv
```


# 3. Next we can make a plan

Using agent mode and the model you want to make a plan. (you can choose in the chat box among 'gent', 'chat', 'plan').  

We are using Melanies' ice cream count to fit different regression models.

1. add new to the context
2. prompt to make a plan
   "Create a plan to analysis data.csv ; I want to be able to choose between many different regression models, using different polynomials (1,2,3), splines, with/witout interscepts, and compare them using RMSE and BIC."
3. Answer quesitons, add thnigs that 'may' be needed to good programing and coding.
4. Execute the plan
