
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
set.seed(10)

#### permutations ################################
permTest <- function(vec1, vec2){
  n.perms <- 1000
  dummycor <- rep(NA, n.perms)
  R <- cor(vec1, vec2)
  for (i in 1:n.perms){
    vec1.perm <- sample(vec1, length(vec1))
    dummycor[i] <- cor(vec1.perm, vec2)
  }
  # p-value in a permutation test is the proportion of permute-calculated R values larger than R of the original samples
  # two-sided test
  pval <- length(dummycor[abs(dummycor) > abs(R)])/n.perms
  return(list(R, pval))
}

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
mdata2 <- left_join(mdata1, natData, by = "season") %>% select(-mn_early_nat, -valid_normweeks) %>% filter(!is.na(mn_early_st))
incl.analysis <- mdata2 %>% group_by(state) %>% count(state) %>% filter(n == 8) %>% select(state) %>% ungroup %>% unlist

#### process correlation coefficients ################################
corrData.sentinel <- mdata2 %>% filter(state %in% incl.analysis) %>% group_by(State) %>% summarise(R = permTest(mn_early_st, mn_retro_nat)[[1]], pval = permTest(mn_early_st, mn_retro_nat)[[2]]) %>% mutate(signif = ifelse(pval < 0.05, 1, 0))

corrData.retro <- mdata2 %>% filter(state %in% incl.analysis) %>% group_by(State) %>% summarise(R = permTest(mn_retro_st, mn_retro_nat)[[1]], pval = permTest(mn_retro_st, mn_retro_nat)[[2]]) %>% mutate(signif = ifelse(pval < 0.05, 1, 0))

#### write to file ################################
setwd('../SDI_Data/explore/R_export')
write.csv(corrData.sentinel, file = 'sentinelStateCorrelation_signif.csv', row.names=F)
write.csv(corrData.retro, file = 'retroStateCorrelation_signif.csv', row.names=F)
# saved 10/15/15

#### plot formmating ################################
w <- 5; h <- 3
mar <- c(0,0,0,0)
setwd('../../../Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/MainFigures')

#### plot index data as scatterplot ################################
ixplot <- ggplot(mdata2 %>% filter(state %in% incl.analysis), aes(x = mn_early_st, y = mn_retro_nat, group = State)) +
  geom_point() +
  theme(text = element_text(size = 18)) +
  facet_wrap(~State, scales = 'free')
x11()
print(ixplot)

#### plot map of correlation coefficients ################################
mapplot <- ggplot(corrData.sentinel, aes(map_id = State)) +
  geom_map(aes(fill = R), map = statesMap, color = "black") +
  scale_fill_gradientn(name = "Pearson's R", colours = brewer.pal(8, "PRGn"), guide = 'legend', breaks = seq(-1, 1, by = 0.25)) +
  expand_limits(x = statesMap$long, y = statesMap$lat) +
  theme_minimal(base_size = 16, base_family = "") +
  theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank(), plot.margin = unit(mar, "mm")) +
  labs(x=NULL, y=NULL)
ggsave(mapplot, file="earlySt_retroNat_corrCoef_stlvl.png", width=w, height=h)

setwd('../AddlFigures')
mapplot2 <- ggplot(corrData.retro, aes(map_id = State)) +
  geom_map(aes(fill = R), map = statesMap, color = "black") +
  scale_fill_gradientn(name = "Pearson's R", colours = brewer.pal(8, "PRGn"), guide = 'legend', breaks = seq(-1, 1, by = 0.25)) +
  expand_limits(x = statesMap$long, y = statesMap$lat) +
  theme_minimal(base_size = 16, base_family = "") +
  theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank(), plot.margin = unit(mar, "mm")) +
  labs(x=NULL, y=NULL)
ggsave(mapplot2, file="retroSt_retroNat_corrCoef_stlvl.png", width=w, height=h)
#10/15/15
