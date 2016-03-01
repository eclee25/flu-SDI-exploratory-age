
## Name: Elizabeth Lee
## Date: 10/22/15
## Function: severity ms bar chart: x-axis = retrospective severity, y-axis = national operational indicators (hospitalization rate, P&I mortality percentage, excess mortality rate w/ state deviation as SE)
## Filenames: CDC_Source/Import_Data/cdc_severity_measures_hospMort_nat.csv; Py_export/SDI_nat_classif_covCareAdj_v5_7.csv; Py_export/SDI_state_classif_covCareAdj_v5_7st.csv

## Data Source: 
## Notes: include states with early seasons because they are still peaking prior to the national epidemic
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

#### header #################################
rm(list = ls())
# .Rprofile sets wd 'Dropbox (Bansal Lab)/code' and sources "GeneralTools.R" in .myenv
require(dplyr)
require(ggplot2)
require(tidyr)
require(readr)
require(grid)
setwd(dirname(sys.frame(1)$ofile)) # only works if you source the program

#### plot formatting ################################
mar <- c(0.5, 0.5, 0.5, 0.5)
w <- 8; h <- 5.75; dp <- 300

#### import data ################################
setwd('../../Py_export') 
natIX <- read_csv('SDI_nat_classif_covCareAdj_v5_7.csv')
stIX <- read_csv('SDI_state_classif_covCareAdj_v5_7st.csv', col_types = "icddi") %>% rename(Abbreviation = state) 


setwd('../../../Census')
abbrData <- read.csv('state_abbreviations.csv', header = T, colClasses = list('Abbreviation' = 'character'))
abbrData$State <- tolower(abbrData$State)

setwd('../CDC_Source/Import_Data')
natIndic <- read_csv('cdc_severity_measures_hospMort_nat.csv')
setwd('../from_Cecile')
stIndic <- read_csv('ExcessPI_seasonal_statelvl.csv') %>% mutate(State = tolower(State))
names(stIndic) <- c('state_code', 'State', 'seasonString', 'excess_PImort_rate100K', 'detrend_excess_PImort_rate', 'pop')

#### clean nat data ################################
natD <- left_join(natIX, natIndic, by = 'season')

#### clean state data ################################
stDummy <- left_join(stIndic, abbrData, by = 'State') %>% filter(seasonString != 'S2009') %>% mutate(season = as.numeric(substr.Right(seasonString, 4)) - 2000)
popDummy <- stDummy %>% group_by(season) %>% summarise(natpop = sum(pop))
stDummy2 <- full_join(stDummy, popDummy, by = 'season') %>% select(-state_code, -detrend_excess_PImort_rate) %>% mutate(popWt = pop/natpop)

stD <- left_join(stIX, stDummy2, by = c('Abbreviation', 'season')) %>% select(-valid_normweeks) 
stExcPI <- stD %>% group_by()

#### merge nat & excess P&I mort data ################################
# calculate national level excess P&I mortality rates based on population weighted average
natExcPI <- stD %>% group_by(season) %>% summarise(ex_PImort_rate100K = weighted.mean(excess_PImort_rate100K, popWt), ex_PImort_SD = sd(excess_PImort_rate100K))
fullD <- left_join(natD, natExcPI, by = 'season') %>% select(season, mn_retro, hosp_tot, pk_ili_prop, ex_PImort_rate100K, ex_PImort_SD) %>% mutate(pk_ili_perc = pk_ili_prop*100)

#### linear model bw mn_retro ################################
modHosp <- lm(hosp_tot ~ mn_retro, data = fullD)
modPkILI <- lm(pk_ili_perc ~ mn_retro, data = fullD)
modExPI <- lm(ex_PImort_rate100K ~ mn_retro, data = fullD)
modStExPI <- lm(excess_PImort_rate100K ~ mn_retro, data = stD)

#### exploratory ################################
plot(fullD$mn_retro, fullD$hosp_tot, col = 'yellow', xlim = c(-15, 15), ylim = c(0, 45))
abline(modHosp, col = 'yellow')
points(fullD$mn_retro, fullD$pk_ili_perc, col = 'blue')
abline(modPkILI, col = 'blue')
points(fullD$mn_retro, fullD$ex_PImort_rate100K, col = 'purple')
abline(modExPI, col = 'purple')

plot(stD$mn_retro, stD$excess_PImort_rate100K)
abline(modStExPI)

#### generate bar chart data ################################
# evenly spaced retro values
retroVal <- data.frame(mn_retro = seq(-14, 14, by = 7))
barDNat <- data.frame(mn_retro = retroVal$mn_retro, hosp = predict(modHosp, retroVal), pkILI = predict(modPkILI, retroVal), exPI = predict(modExPI, retroVal)) %>% gather("metric", "value", 2:4)
barDSt <- data.frame(mn_retro = retroVal$mn_retro, exPI = predict(modStExPI, retroVal)) %>% gather("metric", "value", 2)

# unevenly spaced retro values
barDNat2 <- fullD %>% filter(season %in% c(9, 6, 5, 8)) %>% select(-ex_PImort_SD, -pk_ili_prop) %>% gather("metric", "value", 3:5) %>% mutate(mn_retro_fac = signif(mn_retro, 2)) %>% filter(metric != 'pk_ili_prop') %>% left_join(fullD %>% select(season, ex_PImort_SD), by = 'season') %>% mutate(SD = ifelse(metric == 'ex_PImort_rate100K', ex_PImort_SD, NA)) %>% select(-ex_PImort_SD)

#### draw bar chart ################################
setwd('../../Manuscripts/Age_Severity/Submission_Materials/BMCInfectiousDiseases/MainFigures/subfigs')

natPlot <- ggplot(barDNat, aes(x = factor(mn_retro), y = value, ymax = 24)) +
  geom_bar(aes(alpha = metric, fill = factor(mn_retro)), colour = 'black', stat = 'identity', width = 0.75, position = "dodge") +
  scale_alpha_manual(limits = c("hosp", "pkILI", "exPI"), labels = c("Hosp. (rate)", "Peak ILI/Visits (%)", "Excess P&I Mort. (rate)"), values = c(0.5, 0.75, 1), name = 'Indicator') +
  scale_fill_manual(limits = c(-14, -7, 0, 7, 14), values = c("#2c7bb6", "#abd9e9", "#ffffbf", "#fdae61", "#d7191c"), labels = c("Mild", ".", ".", ".", "Severe")) +
  geom_text(aes(label = c("Mild", "", "", "", "Severe"), x = levels(factor(mn_retro)), y = rep(23.5, 5)), size = 4) +
  theme_bw(base_size = 14, base_family = "") +
  theme(panel.grid.minor = element_blank(), panel.grid.major = element_blank(), axis.ticks.x = element_blank(), plot.margin = unit(mar, "mm"), legend.position = 'bottom') +
  ylab("Cumulative Rate per 100K; Percent") +
  xlab(expression(paste('Retospective Severity, ', bar(rho["s,r"])))) +
  guides(fill = 'none')
# ggsave(natPlot, width = w, height = h, file = "zRR_translation_even.png")
print(natPlot)

limits.ls <- sort(unique(barDNat2$mn_retro_fac))
if(length(limits.ls) == 5){
  colorbar <- c("#2c7bb6", "#abd9e9", "#ffffbf", "#fdae61", "#d7191c")
} else{
  # colorbar <- c("#2c7bb6", "#abd9e9", "#ffffbf", "#d7191c")
  colorbar <- c("#313695", "#abd9e9", "#fee090", "#d7191c")
}

natPlotU <- ggplot(barDNat2, aes(x = mn_retro_fac, y = value)) +
  geom_bar(aes(alpha = factor(metric, levels = c("hosp_tot", "ex_PImort_rate100K", "pk_ili_perc")), fill = factor(mn_retro_fac)), colour = 'black', stat = 'identity', width = 2.5, position = "dodge") +
  geom_errorbar(aes(ymax = value + SD, ymin = ifelse((value - SD) >= 0, value - SD, 0)), position = "dodge", hjust = 1, width = .3) +
  scale_alpha_manual(limits = c("hosp_tot", "ex_PImort_rate100K", "pk_ili_perc"), labels = c("Hosp. (rate)", "Excess P&I Mort. (rate)", "Peak ILI/Visits (%)"), values = c(0.2, 0.6, 1), name = 'Indicator') +
  scale_fill_manual(limits = as.character(limits.ls), values = colorbar, labels = c("Mild", rep("", length(limits.ls)-2), "Severe")) +
  geom_text(aes(label = c("Mild", rep("", length(limits.ls)-2), "Severe"), x = limits.ls, y = rep(21, length(limits.ls))), size = 4) +
  theme_bw(base_size = 14, base_family = "") +
  theme(panel.grid.minor = element_blank(), panel.grid.major = element_blank(), plot.margin = unit(mar, "mm"), legend.position = 'bottom') +
  ylab("Cum. Rate per 100K; Percent") +
  xlab(expression(paste('Retospective Severity, ', bar(rho["s,r"])))) +
  scale_x_continuous(breaks = c(limits.ls), labels = as.character(limits.ls)) +
  guides(fill = 'none')
ggsave(natPlotU, width = w, height = h, dpi = dp, file = "zRR_translation_uneven.png")
print(natPlotU)

#### alternative bar charts ################################
natPlot2 <- ggplot(barDNat, aes(x = factor(mn_retro), y = value, ymax = 24)) +
  geom_bar(aes(fill = metric), colour = 'black', stat = 'identity', width = 0.75, position = "dodge") +
  # geom_text(aes(label = signif(value, digits = 2)), position = position_dodge(width = 1), vjust = -0.5) +
  scale_fill_manual(labels = c("Cum. Hosp. (rate)", "Peak ILI/Visits (%)", "Excess P&I Mort. (rate)"), limits = c("hosp", "pkILI", "exPI"), values = c('#1b9e77', '#d95f02', '#7570b3'), name = 'Indicator') +
  theme_bw(base_size = 18, base_family = "") +
  theme(panel.grid.minor = element_blank(), panel.grid.major = element_blank(), axis.ticks.x = element_blank(), plot.margin = unit(mar, "mm"), legend.position = 'bottom') +
  xlab(expression(paste('Retospective Severity, ', bar(rho["s,r"])))) +
  ylab("Rate per 100K; Percent")
# print(natPlot2)

 
stPlot <- ggplot(barDSt, aes(x = factor(mn_retro), y = value, ymax = 24)) +
  geom_bar(aes(fill = metric), colour = 'black', stat = 'identity', width = 0.25, position = "dodge") +
  # geom_text(aes(label = signif(value, digits = 2)), position = position_dodge(width = 1), vjust = -0.5) +
  scale_fill_manual(labels = c("Excess P&I Mort. (rate)"), limits = c("exPI"), values = c('#7570b3'), name = 'Indicator') +
  theme_bw(base_size = 18, base_family = "") +
  theme(panel.grid.minor = element_blank(), panel.grid.major = element_blank(), axis.ticks.x = element_blank(), plot.margin = unit(mar, "mm"), legend.position = 'bottom') +
  xlab(expression(paste('Retospective Severity, ', bar(rho["s,r"])))) +
  ylab("Rate per 100K")
# print(stPlot)
  