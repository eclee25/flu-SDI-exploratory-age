
## Name: Elizabeth Lee
## Date: 7/15/15
## Function: export cleaned data to create reformed benchmark
# 10/4/15: export to R_export
## Filenames: 
## Data Source: 
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

require(dplyr)
require(ggplot2)
require(tidyr)
setwd(dirname(sys.frame(1)$ofile)) # only works if you source the program


logit_func <- function(p, percents){
  if(percents==T){
    p <- p/100
  }
  return(log(p)-log(1-p))
}

setwd('../../../../../CDC_Source/Import_Data')
# short data: seasons 2 to 9, long data: seasons -2 to 14
long <- read.csv('cdc_severity_data_long_cleaned.csv', header=T, na.strings="NA")

# perform log and logit transformations
long2 <- tbl_df(long) %>% filter(season!=10) %>% mutate(logit_perc_pos = logit_func(perc_pos, percents=T)) %>% mutate(logit_propPi = logit_func(prop_pi, percents=F)) %>% mutate(log_pedDeaths = log(ped_deaths)) %>% mutate(logit_iliProp = logit_func(ili_prop, percents=F)) %>% mutate(log_hosp5.17 = log(hosp_5.17)) %>% mutate(log_hosp18.49 = log(hosp_18.49))

# find means and sd for each dataset in prep for standardization
long.means <- apply(long2, 2, mean, na.rm=T)
long.means[1] <- 0
long.mn.mx <- t(long.means %*% t(rep(1, dim(long2)[1])))
long.sd <- apply(long2, 2, sd, na.rm=T)
long.sd[1] <- 1
long.sd.mx <- t(long.sd %*% t(rep(1, dim(long2)[1])))

# perform standardization for benchmark
long2.std <- (long2 - long.mn.mx)/long.sd.mx
long2.std <- tbl_df(long2.std)

# exploratory plot: plot standardized data for log and logit values
long2.std.logs <- select(long2.std, season, contains("log"))
names(long2.std.logs) <- c("season", "stdLogit_perc_pos", "stdLogit_propPI", "stdLog_pedDeaths", "stdLogit_iliProp", "stdLog_hosp5.17", "stdLog_hosp18.49")
p.long <- gather(long2.std.logs, "metric", "value", 2:7)
metric.ts <- ggplot(p.long, aes(x=season, y=value, group=metric)) +
    geom_point(aes(color=metric)) + facet_wrap(~metric)
setwd(dirname(sys.frame(1)$ofile))
setwd('../../../../../Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Exploration/output')
ggsave("longBeta_stdMetrics.png", width=9, height=6) # 7/19/15 8:05 pm

# gather data for calculation of mean transformed index
long2std.gather <- gather(long2.std.logs, "metric", "value", 2:7) %>% mutate(metric=as.character(metric))
long3 <- long2std.gather %>% filter(metric != "stdLogit_iliProp")

# create multiple possible indexes from standardized data
# 1) noILI, mean, log transformed data
long4 <- long3 %>% group_by(season) %>% summarise(ixT_avg_noILI = mean(value, na.rm=T))

# join index to original data
long5 <- long2 %>% left_join(long2.std.logs, by="season") %>% left_join(long4, by="season") %>% select(-ili_prop, -logit_iliProp, -stdLogit_iliProp)

# view index values
long5 %>% select(season, contains("ix"))

# compare to original benchmark values
setwd(dirname(sys.frame(1)$ofile))
setwd('../../../../../CDC_Source/Import_Data')


longIX <- read.csv('cdc_severity_index_long.csv', header=T, na.strings="NA")
longIX2 <- longIX %>% mutate(ix_mn = apply(longIX[,c(2:4, 6:7)], 1, mean, na.rm=T)) 
longIX2 %>% select(season, contains("ix"))

# generate tables that compare the three betas
# beta.orig - in ms; beta.mean - same data but mean instead of sum; beta.Tmean - log and logit transformed data with mean
long.compare <- data.frame(season=longIX2$season, beta.orig=longIX2$ix_noILI, beta.mean=longIX2$ix_mn, beta.Tmean=long5$ixT_avg_noILI)

# write data to file
setwd(dirname(sys.frame(1)$ofile))
setwd('../../../R_export')
write.csv(long.compare, "longBeta_comparisons.csv", row.names=F) # 10/6/15 12:51 pm
write.csv(long5, "longBeta_ixT_avg_noILI.csv", row.names=F) # 10/6/15 12:51 pm

