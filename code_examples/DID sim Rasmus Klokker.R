#this function simulates data that conforms to a classical, in econometrics at least, "difference-in-difference" design.
#in the data one group of observations, the treatment group, is treated at one period in time while the remaining observation, 
#the untreated group, remains untreated. As such, we observe all observations at multiple time points. In pthe pre-treatment period(s)
#all observations are untreated, while in the post-treatment period the observations in the treatment group have received a treatment
#the idea behind the design is then to 1) compute the difference in the outcome variable before and after the treatment occurred for the
#treatment group and 2) Compute the same before-and-after difference for the untreated group and 3) compare these two differences to get 
#the estimated effect of the treatment


did_sim <- function(per, units, theta, theta_dyn, treat_per){
  
  #number of periods
  
  per <- per
  
  #how many units
  
  units <- units
  
  #make baseline y
  
  did_dat <- data.frame(y=rnorm(units*per))
  
  #make "unit" id variable
  did_dat$unit <- rep(paste("unit", 1:units), each=per)
  
  
  #make "period" indicator variable
  did_dat$per <- rep(1:per, units)
  
  #sample who should be treated
  
  treated <- sample(paste("unit", 1:units), .20*units)
  
  
  #make "dynamic" treatment indicator
  did_dat$treated <- ifelse(did_dat$unit %in% treated&did_dat$per>=treat_per, "treated", "not treated")
  
  #make "static" treatment indicator
  
  did_dat$treated_stat <- ifelse(did_dat$unit %in% treated, "treated", "not treated")
  
  #make DGP
  
  did_dat$y <- ifelse(did_dat$treated=="treated", did_dat$y+theta+theta_dyn*did_dat$per,did_dat$y)
  
  return(did_dat)
  
}


did_dat <- did_sim(per=2, units=500, theta=1, theta_dyn = 0, treat_per=2)

#plot the data

library(ggplot2)

p <- ggplot(did_dat, aes(per, y, color=treated_stat))
p <- p+stat_summary(fun=mean, geom="line")
p

# Estimate treatment effect via OLS - Interaction specification

lm_int <- lm(y~treated_stat+as.factor(per)+treated_stat*as.factor(per), data=did_dat)

summary(lm_int)