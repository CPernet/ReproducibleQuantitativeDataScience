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

# Required behaviour
- The original input must not be modified.
- Missing values must be excluded.
- Negative ice cream count values must be removed.
- Output must inlude both model goodness and prediction accuracy.
