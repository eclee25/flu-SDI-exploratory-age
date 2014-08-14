## Name: Elizabeth Lee
## Date: 8/6/14
## Function: clean data for nation level regression with benchmark index (normalization: 1997-8 through 2013-4, no 2009-10): season, H3 proportion among total subtypable isolates in region, ILINet toddler AR, ILINet child AR, ILINet adult AR, ILINet elderly AR, temperature, precipitation/humidity, antigenic novelty = weighted average of antigenic cluster match to immediately preceding year * proportion of type each season
### clean data for region level regression with retrospective severity index: season, region, H3 proportion among total subtypable isolates in region, SDI toddler AR, SDI child AR, SDI adult AR, SDI elderly AR, temperature by region, precipitation/humidity by region, antigenic novelty?
## Filenames: Py_export/
## Data Source: 
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")


dfsumm<-function(x) {
  if(!class(x)[1]%in%c("data.frame","matrix"))
    stop("You can't use dfsumm on ",class(x)," objects!")
  cat("\n",nrow(x),"rows and",ncol(x),"columns")
  cat("\n",nrow(unique(x)),"unique rows\n")
  s<-matrix(NA,nrow=6,ncol=ncol(x))
  for(i in 1:ncol(x)) {
    iclass<-class(x[,i])[1]
    s[1,i]<-paste(class(x[,i]),collapse=" ")
    y<-x[,i]
    yc<-na.omit(y)
    if(iclass%in%c("factor","ordered"))
      s[2:3,i]<-levels(yc)[c(1,length(levels(yc)))] else
        if(iclass=="numeric")
          s[2:3,i]<-as.character(signif(c(min(yc),max(yc)),3)) else
            if(iclass=="logical")
              s[2:3,i]<-as.logical(c(min(yc),max(yc))) else
                s[2:3,i]<-as.character(c(min(yc),max(yc)))
    s[4,i]<-length(unique(yc))
    s[5,i]<-sum(is.na(y))
    s[6,i]<-!is.unsorted(yc)
  }
  s<-as.data.frame(s)
  rownames(s)<-c("Class","Minimum","Maximum","Unique (excld. NA)","Missing values","Sorted")
  colnames(s)<-colnames(x)
  print(s)
} 
require(MASS)
require(leaps)

##################################################################################
## nation level analysis, 1997-2014 ## 
###################################
## outcome: benchmark index long ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
bench <- read.csv('cdc_severity_index_long_norm2.csv', colClasses='numeric', header=T, na.strings="NA")
# bench&ix_noILI

###################################
## H3 proportion among total isolates national ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/My_Work/Clean_Data_for_Import')
H3 <- read.csv('NREVSS_Isolates_Season_improved.csv', colClasses = 'numeric', header=T)
names(H3) <- c('syear', 'tot_spec', 'a_H1', 'a_unable', 'a_H3', 'a_09H1N1', 'b', 'H3N2v')
H3$season <- H3$syear - 2000
H3$tot_iso <- H3$a_H1 + H3$a_H3 + H3$a_09H1N1 + H3$b + H3$H3N2v
H3$a_H3_prop <- (H3$a_H3+H3$H3N2v)/H3$tot_iso
# H3$a_H3_prop

###################################
## ILI AR ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
ili <- read.csv('all_cdc_source_data.csv', colClasses = c(rep('character', 3), rep('numeric', 35)), header = TRUE, na.string='NA')
ilisub <- ili[as.numeric(ili$wk) > 39 | as.numeric(ili$wk) < 18,] # CDC does not collect data for weeks after 17 in certain seasons. for consistency, do not include weeks 18-20 as "flu season" in the index

# aggregate data to season level
ili_seas <- aggregate(cbind(ili_0.4, ili_5.24, ili_25.64, ili_65., patients) ~ season, data = ilisub, sum)
ili_seas$prop_0.4 <- ili_seas$ili_0.4/ili_seas$patients
ili_seas$prop_5.24 <- ili_seas$ili_5.24/ili_seas$patients
ili_seas$prop_25.64 <- ili_seas$ili_25.64/ili_seas$patients
ili_seas$prop_65. <- ili_seas$ili_65./ili_seas$patients
ili_seas$ili_tot <- ili_seas$ili_0.4 + ili_seas$ili_5.24 + ili_seas$ili_25.64 + ili_seas$ili_65.
ili_seas$prop_tot <- ili_seas$ili_tot/ili_seas$patients

## 8/13/14 OR, based on flu season AR ##
# function to calculate OR
calculateOR <- function(numeratorAR, denominatorAR){
  numeratorOdds <- numeratorAR/(1-numeratorAR)
  denominatorOdds <- denominatorAR/(1-denominatorAR)
  OR <- numeratorOdds/denominatorOdds
  return (OR)
}

ili_seas$OR_ca <- calculateOR(ili_seas$prop_5.24, ili_seas$prop_25.64)
ili_seas$OR_ce <- calculateOR(ili_seas$prop_5.24, ili_seas$prop_65.)
ili_seas$OR_ct <- calculateOR(ili_seas$prop_5.24, ili_seas$prop_0.4)

# prop_0.4, prop_5.24, prop_25.64, prop_65.
# OR_ca, OR_ce, OR_ct
###################################
## temperature, precipitation - national ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/NCDC_Source/Climate_Indices/Import_Data')
natclimate <- read.csv('nat_seas_pcp_tmp.csv', header=T, colClasses='numeric')

# mn_pcp, mn_tavg
###################################
## antigenic novelty ##
## http://elifesciences.org/content/3/e01914/F5


###################################
## merge nation level data ##
dum <- merge(bench, H3, by='season')
dum3 <- merge(dum, ili_seas, by='season')
dum2 <- merge(dum3, natclimate, by='season')
nat <- data.frame(season=dum2$season, ix_noILI=dum2$ix_noILI, H3_prop=dum2$a_H3_prop, ili_t=dum2$prop_0.4, ili_c=dum2$prop_5.24, ili_a=dum2$prop_25.64, ili_e=dum2$prop_65., precip=dum2$mn_pcp, temp=dum2$mn_tavg, ili_tot=dum2$prop_tot, OR_ca=dum2$OR_ca, OR_ce=dum2$OR_ce, OR_ct=dum2$OR_ct)

###################################
## is the benchmark normally distributed? ##
qqnorm(nat$ix_noILI, ylab='benchmark index'); qqline(nat$ix_noILI, col=2)

###################################
## nation level linear models ## 
# leaps example
leaps1 <- regsubsets(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp + ili_a + ili_c + ili_t + ili_e, data=nat, offset = ili_tot, nbest=10)
summary(leaps1)
plot(leaps1, scale='r2')

# for steps adjacent to "best" model (lowest AIC model)
# calculate delta AIC
calculateDeltaAIC <- function(AICtable){
  minAIC <- min(AICtable$AIC)
  AICtable$deltaAIC <- AICtable$AIC - minAIC
  return (AICtable)
}
# calculate Akaike weights (okay for nested models)
calculateAkaikeWts <- function(AICtable){
  if ('deltaAIC' %in% names(AICtable)){
    numerators <- exp(-AICtable$deltaAIC/2)
    denom <- sum(numerators)
    AICtable$AkaikeWts <- numerators/denom
  }
  else {
    AICtable <- calculateDeltaAIC(AICtable)
    numerators <- exp(-AICtable$deltaAIC/2)
    denom <- sum(numerators)
    AICtable$AkaikeWts <- numerators/denom
  }
  return (AICtable)
}

Mnat1 <- lm(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp + ili_a + ili_c + ili_t + ili_e, data=nat, offset = ili_tot)
summary(Mnat1)
step1 <- stepAIC(Mnat1, direction='both')
step1$anova
Mnat1f <- lm(ix_noILI ~ H3_prop + temp + ili_a, data=nat, offset = ili_tot)
summary(Mnat1f)
# data frame for age-specific ILI and OR AIC results
Mnat1_stepchanges <- c('none', '+OR_ce', '+ili_c', '+OR_ca', '+ili_t', '+ili_e', '+OR_ct', '+precip', '-temp', '-ili_a', '-H3_prop')
Mnat1_AIC <- c(19.526, 20.319, 20.711, 20.728, 21.132, 21.276, 21.494, 21.520, 24.389, 24.771, 26.992)
Mnat1_AICtab <- data.frame(steps = Mnat1_stepchanges, AIC = Mnat1_AIC)
Mnat1_AICtab_wts <- calculateAkaikeWts(Mnat1_AICtab)
  
Mnat2 <- lm(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp, data=nat, offset = ili_tot)
summary(Mnat2)
step2 <- stepAIC(Mnat2, direction='both')
step2$anova
Mnat2f <- lm(ix_noILI ~ H3_prop + OR_ca + temp, data=nat, offset = ili_tot)
summary(Mnat2f)
# data frame for OR AIC results
Mnat2_stepchanges <- c('none', '-OR_ca', '+OR_ce', '+OR_ct', '+precip', '-H3_prop', '-temp')
Mnat2_AIC <- c(24.285, 24.771, 24.871, 25.673, 26.235, 34.199, 34.439)
Mnat2_AICtab <- data.frame(steps = Mnat2_stepchanges, AIC = Mnat2_AIC)
Mnat2_AICtab_wts <- calculateAkaikeWts(Mnat2_AICtab)

Mnat3 <- lm(ix_noILI ~ H3_prop + precip + temp +  ili_a + ili_c + ili_t + ili_e, data=nat, offset = ili_tot)
summary(Mnat3)
step3 <- stepAIC(Mnat3, direction='both')
step3$anova
Mnat3f <- lm(ix_noILI ~ H3_prop + temp + ili_a, data=nat, offset = ili_tot)
summary(Mnat3f)
# dataframe for age-specific ILI AIC results
Mnat3_stepchanges <- c('none', '+ili_c', '+ili_t', '+ili_e', '+precip', '-temp', '-ili_a', '-H3_prop')
Mnat3_AIC <- c(19.526, 20.711, 21.132, 21.276, 21.520, 24.389, 24.771, 26.992)
Mnat3_AICtab <- data.frame(steps = Mnat3_stepchanges, AIC = Mnat3_AIC)
Mnat3_AICtab_wts <- calculateAkaikeWts(Mnat3_AICtab)



##################################################################################
## region level analysis, 2001-9 ## 
###################################

## zOR, region, season ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/')
zOR <- read.csv('SDI_regional_classifications.csv', colClasses = c('character', 'character', 'numeric', 'numeric'), header=T)
# add leading zero to region number
zOR[which(as.numeric(zOR$region) %in% 1:9),]$region <- paste('0', zOR[which(as.numeric(zOR$region) %in% 1:9),]$region, sep = '')
# season, region uqid
zOR$uqidSR <- paste('S', zOR$season, 'R', zOR$region, sep='')

# zOR$mn_retro
###################################
## H3 proportion among A isolates regional ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
H3r <- read.csv('all_cdc_source_data_HHSRegion.csv', colClasses = c(rep('character', 4), rep('numeric', 9), 'character', rep('numeric', 12)), header = TRUE, na.string='NA')

# drop all seasons except 2 through 9, keep isolate related columns only
H3r_sub <- H3r[(H3r$season %in% 2:9), 1:15]
H3r_sub$tot_iso <- H3r_sub$a_H1 + H3r_sub$a_H3 + H3r_sub$a_2009H1N1 + H3r_sub$b + H3r_sub$a_H3N2
# season, region uqid
H3r_sub$uqidSR <- paste('S', H3r_sub$season, 'R', H3r_sub$reg, sep='')

# aggregate data to season level
H3rs <- aggregate(cbind(a_H3, a_H3N2, tot_iso) ~ uqidSR, data=H3r_sub, sum)
H3rs$a_H3_prop <- (H3rs$a_H3 + H3rs$a_H3N2)/H3rs$tot_iso

# H3rs$a_H3_prop
###################################
## ILI AR ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
ilir <- read.csv('all_cdc_source_data_HHSRegion.csv', colClasses = c(rep('character', 4), rep('numeric', 9), 'character', rep('numeric', 12)), header = TRUE, na.string='NA')

# drop non-fluweeks
ilirsub <- ilir[as.numeric(ilir$wk) > 39 | as.numeric(ilir$wk) < 18,] # CDC does not collect data for weeks after 17 in certain seasons. for consistency, do not include weeks 18-20 as "flu season" in the index
# drop all seasons except 2 through 9, keep ILI related columns only
ilir2 <- ilirsub[(ilirsub$season %in% 2:9), c(1:4,14:23,26)]
# season, region uqid
ilir2$uqidSR <- paste('S', ilir2$season, 'R', ilir2$reg, sep='')

ilirs <- aggregate(cbind(ili_0.4, ili_5.24, ili_25.64, ili_65., patients) ~ uqidSR, data = ilir2, sum)
ilirs$prop_0.4 <- ilirs$ili_0.4/ilirs$patients
ilirs$prop_5.24 <- ilirs$ili_5.24/ilirs$patients
ilirs$prop_25.64 <- ilirs$ili_25.64/ilirs$patients
ilirs$prop_65. <- ilirs$ili_65./ilirs$patients

# prop_0.4, prop_5.24, prop_25.64, prop_65.
###################################
## temperature, precipitation - region ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/NCDC_Source/Climate_Indices/Import_Data')
climate <- read.csv('reg_seas_pcp_tmp.csv', header=T, colClasses = 'numeric')

# drop all seasons except 2 through 9
climate2 <- climate[(climate$season %in% 2:9),]
# add leading zero for region
climate2[which(as.numeric(climate2$region) %in% 1:9),]$region <- paste('0', climate2[which(as.numeric(climate2$region) %in% 1:9),]$region, sep='')
# season, region uqid
climate2$uqidSR <- paste('S', climate2$season, 'R', climate2$region, sep='')


###################################
## antigenic novelty (national only) ##
## http://elifesciences.org/content/3/e01914/F5
#?

###################################
## merge region level data ##
dumr <- merge(zOR, H3rs, by='uqidSR')
dumr3 <- merge(dumr, ilirs, by='uqidSR')
dumr2 <- merge(dumr3, climate2, by='uqidSR')
reg <- data.frame(uqidSR=dumr2$uqidSR, season=dumr2$season.x, region=dumr2$region.x, retrozOR=dumr2$mn_retro, H3_prop=dumr2$a_H3_prop, ili_t=dumr2$prop_0.4, ili_c=dumr2$prop_5.24, ili_a=dumr2$prop_25.64, ili_e=dumr2$prop_65., precip=dumr2$mn_pcp, temp=dumr2$mn_tavg)

###################################
## region level linear models ## 
Mreg <- lm(retrozOR ~ region + H3_prop + ili_t + ili_c + ili_a + ili_e + precip + temp, data=reg) # H3_prop then ili_a most explanatory
summary(Mreg)
Mreg2 <- lm(retrozOR ~ H3_prop, data=reg) # H3_prop most explanatory
summary(Mreg2)
Mreg3 <- lm(retrozOR ~ ili_a, data=reg) # ili_a significant
summary(Mreg3)
Mreg4 <- lm(retrozOR ~ ili_t, data=reg) 
summary(Mreg4)
Mreg5 <- lm(retrozOR ~ ili_c, data=reg) 
summary(Mreg5)
Mreg6 <- lm(retrozOR ~ ili_e, data=reg) 
summary(Mreg6)
Mreg7 <- lm(retrozOR ~ precip, data=reg) 
summary(Mreg7)
Mreg8 <- lm(retrozOR ~ temp, data=reg) 
summary(Mreg8)
Mreg9 <- lm(retrozOR ~ H3_prop + ili_a, data=reg) # H3_prop reduces ili_a explanatory power
summary(Mreg9)
Mreg10 <- lm(retrozOR ~ H3_prop + ili_a + ili_c, data=reg) # ili_a becomes significant with H3_prop when ili_c is added
summary(Mreg10)

## explore H3_prop covariate
Mreg2 <- lm(retrozOR ~ H3_prop, data=reg) # H3_prop most explanatory
summary(Mreg2)
plot(Mreg2) # increasing variance in residuals as regions become milder
plot(reg$H3_prop, reg$retrozOR) # greater variance among non-H3 season-region pairs

## explore ili_a covariate
Mreg3 <- lm(retrozOR ~ ili_a, data=reg) # ili_a significant
summary(Mreg3)
plot(Mreg3)
plot(reg$ili_a, reg$retrozOR) # no immediate issues

# H3_prop has minimal explanatory power for retrozOR (Adjusted R-squared = 0.1503)
# ili_a has even less explanatory power (Adjusted R-squared = 0.05176)
###################################


## EXTRAS ##
###################################
## state to region crosswalk ## 
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
crosswalk <- read.csv('stateabbr_regnum_crosswalk.csv', header=T, colClasses = 'character')
###################################
## vaccine coverage by state ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Vaccines/Vax_Coverage')
coverage <- read.csv('Vax_Coverage_WEAT_BRFSS.csv', header=T, colClasses = c('numeric', 'character', 'character', 'numeric', 'numeric', 'numeric', 'numeric'))

