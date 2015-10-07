
## Name: Elizabeth Lee
## Date: 7/19/15
## Function: develop mild, moderate, and severe benchmark thresholds based on quantiles; compare to CDC descriptions
## Filenames: 
## Data Source: 
## Notes: 
# 7/22/15: Use qualitative analysis (See "CDC_Source/CDC_severity_descriptions.ods") to set thresholds. Assumes that rank order with beta is true. Add column "classifq" for completeness (not actually used in subsequent analyses).
# 10/5/15: use updated quantile thresholds to output new data file, update paths, add non-iterative CDC qualitatively coded categories as reference for comparison
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

require(dplyr)
setwd(dirname(sys.frame(1)$ofile)) # only works if you source the program


classifySeverity <- function(beta, quantileValues){
  mildThresh <- quantileValues[1]
  sevThresh <- quantileValues[2]
  classification <- rep(NA, length(beta))
  classification[which(beta<mildThresh)] <- -1
  classification[which(beta>sevThresh)] <- 1
  classification[which(beta>=mildThresh & beta <=sevThresh)] <- 0
  # mild = -1, moderate = 0, severe = 1
  return(classification)
}

# cdc codes from CDC_severity_descriptions (NA for 97-98 and 98-99)
CDCcodes <- c(NA, NA, 0, -1, 0, -1, 1, 0,-1, -0.5, 0, 0, 0, -1, 1, 0) 
RRorig <- c(NA, NA, NA, NA, 0, -1, 1, 1, -1, -1, 1, -1, NA, NA, NA, NA)
RRorig.sh <- RRorig[!is.na(RRorig)]
CDCcodes.sh <- CDCcodes[!is.na(RRorig)]

# quantiles
q.25 <- c(0.25, 0.75)
qorig <- c(0.3, 0.75)
q0 <- c(0.32, 0.86) # 4.5 mild seasons
q1 <- c(0.36, 0.86) # 5 mild seasons
q2 <- c(0.33, 0.86) # 4 mild seasons


setwd('../../../R_export')
ixData <- read.csv("longBeta_ixT_avg_noILI.csv", header=T) %>% select(season, contains("ix")) %>% mutate(ixRank = min_rank(ixT_avg_noILI)) %>% mutate(training = ifelse(season %in% 2:9, 0, 1))
# 25% thresholds
thresh25 <- quantile(ixData$ixT_avg_noILI, probs = q.25)
# initial classifq threshold # 7/22/15
threshq.orig <- quantile(ixData$ixT_avg_noILI, probs = qorig)
# classifq threshold # 10/6/15 based on qualitative classifications
threshq0 <- quantile(ixData$ixT_avg_noILI, probs = q0)
threshq1 <- quantile(ixData$ixT_avg_noILI, probs = q1) 
threshq2 <- quantile(ixData$ixT_avg_noILI, probs = q2)

# identify classifications for 25% and CDC-based thresholds
ixData2 <- ixData %>% mutate(classif25 = classifySeverity(ixT_avg_noILI, thresh25)) %>% mutate(classifqOrig = classifySeverity(ixT_avg_noILI, threshq.orig)) %>% mutate(classifq0 = classifySeverity(ixT_avg_noILI, threshq0)) %>% mutate(classifq1 = classifySeverity(ixT_avg_noILI, threshq1)) %>% mutate(classifq2 = classifySeverity(ixT_avg_noILI, threshq2)) %>% mutate(cdcQual = CDCcodes) %>% mutate(RRorig = RRorig)

# # 10/6/15: fix quantile thresholds for training dataset, apply to test dataset
# # doesn't seem to be necessary to have training/test data since we're using an external source to get at the distribution of severity
# thresh.train25 <- quantile(ixData %>% filter(training==1) %>% select(ixT_avg_noILI) %>% unlist, probs=q.25)
# thresh.trainq0 <- quantile(ixData %>% filter(training==1) %>% select(ixT_avg_noILI) %>% unlist, probs=q0)
# thresh.trainq1 <- quantile(ixData %>% filter(training==1) %>% select(ixT_avg_noILI) %>% unlist, probs=q1)
# thresh.trainq2 <- quantile(ixData %>% filter(training==1) %>% select(ixT_avg_noILI) %>% unlist, probs=q2)
# ixData3 <- ixData %>% mutate(classif.train25 = classifySeverity(ixT_avg_noILI, thresh.train25)) %>% mutate(classif.trainq0 = classifySeverity(ixT_avg_noILI, thresh.trainq0)) %>% mutate(classif.trainq1 = classifySeverity(ixT_avg_noILI, thresh.trainq1)) %>% mutate(classif.trainq2 = classifySeverity(ixT_avg_noILI, thresh.trainq2)) %>% mutate(cdcQual = CDCcodes) %>% mutate(RRorig = RRorig)

write.csv(ixData2, 'benchmark_ixT_avg_quantileThresh.csv', row.names=F) # 10/6/15, 17:56
