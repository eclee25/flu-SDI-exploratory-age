
## Name: Elizabeth Lee
## Date: 7/19/15
## Function: develop mild, moderate, and severe benchmark thresholds based on quantiles; compare to CDC descriptions
## Filenames: 
## Data Source: 
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

setwd('/home/elee/R/source_functions')
source("dfsumm.R")

classifySeverity <- function(beta, quantileValues){
  mildThresh <- quantileValues[1]
  sevThresh <- quantileValues[2]
  classification <- rep(0, length(beta))
  classification[which(beta<mildThresh)] <- -1
  classification[which(beta>sevThresh)] <- 1
  # mild = -1, moderate = 0, severe = 1
  return(classification)
}

setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Exploration/output')
ixData <- read.csv("longBeta_ixT_avg_noILI.csv", header=T) %>% select(season, contains("ix")) %>% mutate(ixRank = min_rank(ixT_avg_noILI))
# 10% thresholds
thresh10 <- quantile(ixData$ixT_avg_noILI, probs = c(0.1, 0.9))
# 20% thresholds
thresh20 <- quantile(ixData$ixT_avg_noILI, probs = c(0.2, 0.8)) 
# 25% thresholds
thresh25 <- quantile(ixData$ixT_avg_noILI, probs = c(0.25, 0.75))
# identify classifications for 10% and 20% thresholds
ixData2 <- ixData %>% mutate(classif10 = classifySeverity(ixT_avg_noILI, thresh10)) %>% mutate(classif20 = classifySeverity(ixT_avg_noILI, thresh20)) %>% mutate(classif25 = classifySeverity(ixT_avg_noILI, thresh25))

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(ixData2, 'benchmark_ixT_avg_quantileThresh.csv', row.names=F) # 7/20/15 5:30 pm
