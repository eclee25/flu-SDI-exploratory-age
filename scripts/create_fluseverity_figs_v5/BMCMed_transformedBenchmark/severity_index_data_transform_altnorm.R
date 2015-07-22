
## Name: Elizabeth Lee
## Date: 7/15/15
## Function: 
## Filenames: 
## Data Source: 
## Notes: 
### 7/22/15: try alternative normalization schemes -- do they change beta rank order significantly?

## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

require(dplyr)
require(ggplot2)
require(tidyr)

setwd('/home/elee/R/source_functions')
source("dfsumm.R")

logit_func <- function(p, percents){
  if(percents==T){
    p <- p/100
  }
  return(log(p)-log(1-p))
}

setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Exploration')
# short data: seasons 2 to 9, long data: seasons -2 to 14
long <- read.csv('cdc_severity_data_long_cleaned.csv', header=T, na.strings="NA")

# perform log and logit transformations & assign normalization schemes years
long2 <- tbl_df(long) %>% filter(season!=10) %>% mutate(logit_perc_pos = logit_func(perc_pos, percents=T)) %>% mutate(logit_propPi = logit_func(prop_pi, percents=F)) %>% mutate(log_pedDeaths = log(ped_deaths)) %>% mutate(logit_iliProp = logit_func(ili_prop, percents=F)) %>% mutate(log_hosp5.17 = log(hosp_5.17)) %>% mutate(log_hosp18.49 = log(hosp_18.49)) %>% mutate(norm1 = c(rep(0, 12), rep(1, 4))) %>% mutate(norm2 = c(rep(0, 6), rep(1, 6), rep(2, 4)))

long3 <- long2 %>% select(season, norm1, norm2, contains("log"))
data_only <- long3 %>% select(contains("log"))
headers_only <- long3 %>% select(season, norm1, norm2)

###########################################
## Normalization Scheme 1 ##
# pre and post pandemic years
norm1_refs <- long3 %>% group_by(norm1) %>% summarise_each(funs(mean(., na.rm=T), sd(., na.rm=T)), -season, -norm2)
long3_norm1_combined <- left_join(long3, norm1_refs, by="norm1") %>% select(-norm2)
norm1_mn_mx <- long3_norm1_combined %>% select(contains("mean"))
norm1_sd_mx <- long3_norm1_combined %>% select(contains("_sd"))
norm1_std_noIDs <- (data_only - norm1_mn_mx)/norm1_sd_mx
norm1_std <- bind_cols(headers_only, norm1_std_noIDs) %>% select(-norm2)
names(norm1_std) <- c("season", "norm1", "stdLogit_perc_pos", "stdLogit_propPI", "stdLog_pedDeaths", "stdLogit_iliProp", "stdLog_hosp5.17", "stdLog_hosp18.49")

# exploratory plot: plot standardized data for log and logit values
norm1_std_gather <- gather(norm1_std, "metric", "value", 3:8)
norm1metric.ts <- ggplot(norm1_std_gather, aes(x=season, y=value, group=metric)) +
  geom_point(aes(color=as.factor(norm1))) + facet_wrap(~metric)
setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures')
ggsave("longBeta_norm1_stdMetrics.png", width=9, height=6) # 7/22/15 15:18

# rm ILI data for beta calculation
norm1_forbeta <- norm1_std_gather %>% mutate(metric=as.character(metric)) %>% filter(metric != "stdLogit_iliProp")
# create index: noILI, mean, log transformed data
norm1_ix <- norm1_forbeta %>% group_by(season) %>% summarise(ixTavg_norm1 = mean(value, na.rm=T))


###########################################
## Normalization Scheme 2 ##
# 1997-98 through 2002-03, 2003-04 through 2008-09, 2010-11 through 2013-14
norm2_refs <- long3 %>% group_by(norm2) %>% summarise_each(funs(mean(., na.rm=T), sd(., na.rm=T)), -season, -norm1)
long3_norm2_combined <- left_join(long3, norm2_refs, by="norm2") %>% select(-norm1)
norm2_mn_mx <- long3_norm2_combined %>% select(contains("mean"))
norm2_sd_mx <- long3_norm2_combined %>% select(contains("_sd"))
norm2_std_noIDs <- (data_only - norm2_mn_mx)/norm2_sd_mx
norm2_std <- bind_cols(headers_only, norm2_std_noIDs) %>% select(-norm1)
names(norm2_std) <- c("season", "norm2", "stdLogit_perc_pos", "stdLogit_propPI", "stdLog_pedDeaths", "stdLogit_iliProp", "stdLog_hosp5.17", "stdLog_hosp18.49")

# exploratory plot: plot standardized data for log and logit values
norm2_std_gather <- gather(norm2_std, "metric", "value", 3:8)
norm2metric.ts <- ggplot(norm2_std_gather, aes(x=season, y=value, group=metric)) +
    geom_point(aes(color=as.factor(norm2))) + facet_wrap(~metric)
setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures')
ggsave("longBeta_norm2_stdMetrics.png", width=9, height=6) # 7/22/15 15:17

# rm ILI data for beta calculation
norm2_forbeta <- norm2_std_gather %>% mutate(metric=as.character(metric)) %>% filter(metric != "stdLogit_iliProp")
# create index: noILI, mean, log transformed data
norm2_ix <- norm2_forbeta %>% group_by(season) %>% summarise(ixTavg_norm2 = mean(value, na.rm=T))

###########################################
# join indexes to original data
norm1_forexport <- norm1_std %>% select(-contains("iliProp")) %>% left_join(., norm1_ix, by="season")
norm2_forexport <- norm2_std %>% select(-contains("iliProp")) %>% left_join(., norm2_ix, by="season")

# compare to original "new" benchmark (normalization occurs over entire period)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
norm0 <- read.csv('benchmark_ixT_avg_quantileThresh.csv', header=T, na.strings="NA")

# generate tables that compare the three betas
# beta.orig - in ms; beta.mean - same data but mean instead of sum; beta.Tmean - log and logit transformed data with mean
compare <- data.frame(season=norm0$season, beta_norm0=norm0$ixT_avg_noILI, beta_norm1=norm1_forexport$ixTavg_norm1, beta_norm2=norm2_forexport$ixTavg_norm2) %>% mutate(norm0rank = min_rank(beta_norm0)) %>% mutate(norm1rank = min_rank(beta_norm1)) %>% mutate(norm2rank = min_rank(beta_norm2))

########################################################
# plot bars for data
# specific formatting
seasonlab <- c('97-98', '98-99', '99-00', '00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '10-11', '11-12', '12-13', '13-14')
# plot formatting
w = 464 
h = 464
ps = 14
margin = c(1, 3, 1, 4) + 0.1 # bottom, left, top, right
omargin = c(1, 0, 1, 1)
un = "px"

setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures')
par(mar=margin)
png(filename="benchmarkbars_norm1.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
mids <- barplot(compare$beta_norm1, xlab='', ylab=expression(paste('Benchmark, ', beta[s], sep=' ')), ylim=c(-1.5, 1.5), cex.lab=1.3, main="norm1")
abline(h = quantile(compare$beta_norm1, c(0.3, 0.75)), col="black")
axis(1, at=mids, seasonlab, las = 2)
mtext('Season', side=1, line=3.5)
dev.off()

setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures')
par(mar=margin)
png(filename="benchmarkbars_norm2.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
mids2 <- barplot(compare$beta_norm2, xlab='', ylab=expression(paste('Benchmark, ', beta[s], sep=' ')), ylim=c(-1.5, 1.5), cex.lab=1.3, main="norm2")
abline(h = quantile(compare$beta_norm2, c(0.30, 0.70)), col="black")
axis(1, at=mids2, seasonlab, las = 2)
mtext('Season', side=1, line=3.5)
dev.off()

########################################################
# write data to file
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(compare, "beta_altnorm_comparisons.csv", row.names=F) # 7/22/15 4:02 pm

