# Solution to provenance exercise
# Author: Carl-Emil Pless
# Date: 26-06-2023

rm(list = ls())

# Load packages
library(here)

# Load MelsIceCreamHabits.csv
data <- read.csv(here("provenance", "MelsIceCreamHabits.csv"))

# Rename columns to observation, celcius, and scopps
colnames(data) <- c("observation", "celcius", "scoops")

# Remove negative scoops
data <- data[data$scoops >= 0, ]

# Run linear regression
reg <- lm(scoops ~ celcius, data = data)

# Predict for 40 C
predict(reg, newdata = data.frame(celcius = 40))

# Remove intercept from initial regression
reg2 <- lm(scoops ~ celcius - 1, data = data)

# Predict for 40 C
predict(reg2, newdata = data.frame(celcius = 40))