
## Name: Elizabeth Lee
## Date: 10/13/15
## Function: Pearson's R correlation coefficients between state early warning and national retrospective
## Filenames: 
## Data Source: 
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

#### header #################################
rm(list = ls())
require(tidyr)
require(ggplot2)
require(Hmisc)
require(dplyr)
require(RColorBrewer)

# .Rprofile sets wd 'Dropbox (Bansal Lab)/code' and sources "GeneralTools.R" in .myenv
setwd(dirname(sys.frame(1)$ofile)) # only works if you source the program

#### import data ################################
setwd('../../Py_export') 
stateData <- read.csv('SDI_state_classif_covCareAdj_v5_7st.csv', header = T, colClasses = list('state' = 'character'))
natData <- read.csv('SDI_nat_classif_covCareAdj_v5_7.csv', header = T) %>% rename(mn_retro_nat = mn_retro, mn_early_nat = mn_early)
setwd('../../../Census')
abbrData <- read.csv('state_abbreviations.csv', header = T, colClasses = list('Abbreviation' = 'character'))
abbrData$State <- tolower(abbrData$State)

statesMap <- map_data("state")

#### clean data ################################
mdata1 <- left_join(tbl_df(stateData), tbl_df(abbrData), by = c("state" = "Abbreviation")) %>% rename(mn_retro_st = mn_retro, mn_early_st = mn_early)
mdata2 <- left_join(mdata1, natData, by = "season") %>% select(-mn_retro_st, -mn_early_nat, -valid_normweeks) %>% filter(!is.na(mn_early_st))
incl.analysis <- mdata2 %>% group_by(state) %>% count(state) %>% filter(n == 8) %>% select(state) %>% ungroup %>% unlist

#### process correlation coefficients ################################
corrData <- mdata2 %>% filter(state %in% incl.analysis) %>% group_by(State) %>% summarise(R = rcorr(mn_early_st, mn_retro_nat)[[1]][2], pval = rcorr(mn_early_st, mn_retro_nat)[[3]][2])

#### plot formmating ################################
w <- 5; h <- 3
mar <- c(0,0,0,0)
setwd('../Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/MainFigures')

#### plot index data as scatterplot ################################
ixplot <- ggplot(mdata2 %>% filter(state %in% incl.analysis), aes(x = mn_early_st, y = mn_retro_nat, group = State)) +
  geom_point() +
  theme(text = element_text(size = 18)) +
  facet_wrap(~State, scales = 'free')
x11()
print(ixplot)

#### plot map of correlation coefficients ################################
mapplot <- ggplot(corrData, aes(map_id = State)) +
  geom_map(aes(fill = R), map = statesMap, color = "black") +
  scale_fill_gradientn(name = "Pearson's R", colours = brewer.pal(8, "PRGn"), guide = 'legend', breaks = seq(-1, 1, by = 0.25)) +
  expand_limits(x = statesMap$long, y = statesMap$lat) +
  theme_minimal(base_size = 16, base_family = "") +
  theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank(), plot.margin = unit(mar, "mm")) +
  labs(x=NULL, y=NULL)
ggsave(mapplot, file="earlySt_retroNat_corrCoef_stlvl.png", width=w, height=h)
