
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

# read in beta zRR data
setwd('../../../R_export')
betaData <- read.csv('benchmark_ixT_avg_quantileThresh.csv', header=T) %>% select(classifq0) %>% unlist
betaData.sh <- betaData[!is.na(RRorig)]

# quantiles
q.25 <- c(0.25, 0.75)
qorig <- c(0.3, 0.75)
q0 <- c(0.32, 0.86) # 4.5 mild seasons
q1 <- c(0.36, 0.86) # 5 mild seasons
q2 <- c(0.33, 0.86) # 4 mild seasons


# import RR data
setwd('../Py_export')
RRdata <- read.csv("SDI_nat_classif_covCareAdj_v5_7.csv", header=T)
thresh25 <- quantile(RRdata$mn_retro, probs = q.25)
# assumes that RR index follows the same distribution as the qualitative classifications
threshq0 <- quantile(RRdata$mn_retro, probs = q0)
threshq1 <- quantile(RRdata$mn_retro, probs = q1)
threshq2 <- quantile(RRdata$mn_retro, probs = q2)
RRdata2 <- RRdata %>% mutate(classif25R = classifySeverity(mn_retro, thresh25)) %>% 
  mutate(classif25E = classifySeverity(mn_early, thresh25)) %>% 
  mutate(classifq0R = classifySeverity(mn_retro, threshq0)) %>% 
  mutate(classifq0E = classifySeverity(mn_early, threshq0)) %>% 
  mutate(classifq1R = classifySeverity(mn_retro, threshq1)) %>% 
  # mutate(classifq1E = classifySeverity(mn_early, threshq1)) %>% 
  mutate(classifq2R = classifySeverity(mn_retro, threshq2)) %>% 
  # mutate(classifq2E = classifySeverity(mn_early, threshq2)) %>% 
  mutate(cdcQual = CDCcodes.sh, RRorig = RRorig.sh, betaNew = betaData.sh)


# write.csv(RRdata2, 'benchmark_ixT_avg_quantileThresh.csv', row.names=F) # 10/6/15 
