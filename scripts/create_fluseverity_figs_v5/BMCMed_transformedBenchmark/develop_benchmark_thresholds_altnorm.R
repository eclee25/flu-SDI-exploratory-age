
## Name: Elizabeth Lee
## Date: 7/19/15
## Function: develop mild, moderate, and severe benchmark thresholds based on quantiles; compare to CDC descriptions
## Filenames: 
## Data Source: 
## Notes: 
# 7/22/15: Use qualitative analysis (See "CDC_Source/CDC_severity_descriptions.ods") to set thresholds. Assumes that rank order with beta is true. Add column "classifq" for completeness (not actually used in subsequent analyses).
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

setwd('/home/elee/R/source_functions')
source("dfsumm.R")
require(dplyr)

classifySeverity <- function(beta, quantileValues){
  mildThresh <- quantileValues[1]
  sevThresh <- quantileValues[2]
  classification <- rep(0, length(beta))
  classification[which(beta<mildThresh)] <- -1
  classification[which(beta>sevThresh)] <- 1
  # mild = -1, moderate = 0, severe = 1
  return(classification)
}

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
ix <- read.csv("beta_altnorm_comparisons.csv", header=T)
# jerryrig classifq threshold
b0_threshq <- quantile(ix$beta_norm0, probs = c(0.3, 0.75))
b1_threshq <- quantile(ix$beta_norm1, probs = c(0.3, 0.75))
b2_threshq <- quantile(ix$beta_norm2, probs = c(0.3, 0.70))
# identify classifications for 10% and 20% thresholds
ix2 <- ix %>% mutate(b0_classifq = classifySeverity(beta_norm0, b0_threshq)) %>% mutate(b1_classifq = classifySeverity(beta_norm1, b1_threshq)) %>% mutate(b2_classifq = classifySeverity(beta_norm2, b2_threshq))

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(ix2, 'benchmark_ixTavg_altnorm_comparisons.csv', row.names=F) 
