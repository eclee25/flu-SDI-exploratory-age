# 5/20/13
# Draw a histogram of the popstat variable where popstat represents the population of all ages of a zipcode prefix.
#
# Data: popstat_by_zip3_2010.csv

pop <- read.csv('popstat_by_zip3_2010.csv', header = F)
pop2 <- pop[1:919,] # drop last row because the last row is the total across all zipcodes

hist(pop2[,3], breaks= 25, main='Popstat histogram', xlab = "Popstat", prob=T) # saved as popstat_by_zip3_2010_v5-16-13.png
quantile(pop2[,3])

## 6/4/13 Break down popstat more
hist(pop2[,3], breaks= 200, main='Popstat histogram', xlab = "Popstat", prob=T) # 6/4/10 draw hist with greater number of breaks to see if the distr is bimodal
# each bar represents a popstat of ~15,000

hist(pop2[,3], breaks= 500, main='Popstat histogram', xlab = "Popstat", prob=T) # 6/4/10 draw hist with greater number of breaks to see if the distr is bimodal
# each bar represents a popstat of ~6000

# perform checks on the histogram -- why is there such a high density in the zero bin? (the 35 zero values were not removed)
zeros<- pop2[pop2$V3==0,]
lessthan15000 <- pop2[pop2$V3<15000,3]
sd<-setdiff(pop2[,3], lessthan15000)
bw15and30000 <- sd[sd<30000]

# draw histogram again where 0 values are removed
pop_no0 <- pop2[pop2$V3!=0,]
hist(pop_no0[,3], breaks= 200, main='Popstat histogram', xlab = "Popstat", prob=T)
hist(pop_no0[,3], breaks= 500, main='Popstat histogram', xlab = "Popstat", prob=T) # saved as popstat_by_zip3_2010_n0.png

# 0%: 0.0
# 25%: 105,774.5
# 50%: 202,375
# 75%: 432,941.5
# 100%: 3,003,916