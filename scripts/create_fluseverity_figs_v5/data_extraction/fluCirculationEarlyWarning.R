
## Name: Elizabeth Lee
## Date: 10/23/15
## Function: Export table of percent positive laboratory confirmed samples during early warning weeks
## Filenames: CDC_Source/Import_Data/all_cdc_source_data.csv
## Data Source: CDC 
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

#### header #################################
rm(list = ls())
require(dplyr)
require(tidyr)
require(readr)
setwd(dirname(sys.frame(1)$ofile)) # only works if you source the program

#### import Data ################################
setwd('../../../../../CDC_Source/Import_Data') 
cdcDat <- read_csv('all_cdc_source_data.csv', col_types = paste0("cii_d", paste(rep("_", 7), collapse = ''), "i", paste(rep("_", 25), collapse = ''))) 

#### early warning data ################################
ewDat <- data.frame(season = c(-2:9, 11:15), ewStart = c(50, rep(49, 4), rep(50, 2), rep(49, 4), 50, rep(49, 3), rep(50, 2))) %>% mutate(ewEnd = ewStart + 1)
ewDat2 <- ewDat %>% mutate(ewEnd = ewStart + 1) #%>% gather("type", "wknum", 2:3)
fullD <- left_join(cdcDat, ewDat, by = "season") %>% mutate(ew = ifelse(wk == ewStart, T, ifelse(wk == ewEnd, T, F))) %>% mutate(Season = paste(as.character(season + 1999), as.character(season + 2000), sep = '-'))

#### process perc Pos data ################################
percD <- fullD %>% filter(ew) %>% group_by(Season) %>% summarise(Percent = signif(mean(perc_pos), 3))

#### export table ################################
setwd('../../Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures')
write.csv(percD, "early_warning_percPos.csv", row.names = F)
