## Name: Elizabeth Lee
## Date: 11/5/14
## Function: clean data for nation level regression with benchmark index (normalization: 1997-8 through 2013-4, no 2009-10): season, H3 proportion among total subtypable isolates in region, ILINet toddler AR, ILINet child AR, ILINet adult AR, ILINet elderly AR, temperature, precipitation/humidity, antigenic novelty = weighted average of antigenic cluster match to immediately preceding year * proportion of type each season
### clean data for region level regression with retrospective severity index: season, region, H3 proportion among total subtypable isolates in region, SDI toddler AR, SDI child AR, SDI adult AR, SDI elderly AR, temperature by region, precipitation/humidity by region, antigenic novelty?

## 11/5: v5: age-specific incidence as covariates in the model adjusted for care seeking behavior for ILI and visits, rm OR regression, response = benchmark normalized across 1997-98 to 2013-14 period.
## 7/20/15: update with new beta values

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
require(corrplot)
##################################################################################
## nation level analysis, 1997-2014 ## 
###################################
## outcome: benchmark index long ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
bench <- read.csv('benchmark_ixT_avg_quantileThresh.csv', colClasses='numeric', header=T, na.strings="NA")
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
## population size by age ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census/Import_Data')
caPop <- read.csv('totalpop_age_Census_98-14.csv', header=FALSE, colClasses=c('numeric', 'character', 'numeric'))
tePop <- read.csv('pop_todEld_Census_98-14.csv', header=TRUE, colClasses='numeric')
names(caPop) <- c('season', 'age', 'pop')
cPop <- caPop[which(caPop[,2]=='C'),c(1,3)]
aPop <- caPop[which(caPop[,2]=='A'),c(1,3)]
totPop0 <- merge(tePop,cPop, by='season')
totPop <- merge(totPop0, aPop, by='season')
names(totPop) <- c('season', 'year', 'toddlers0.5pop', 'elderly65.pop', 'children5.24pop', 'adults25.64pop')

###################################
## ILI AR ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
ili <- read.csv('all_cdc_source_data.csv', colClasses = c(rep('character', 3), rep('numeric', 35)), header = TRUE, na.string='NA')
ilisub <- ili[as.numeric(ili$wk) > 39 | as.numeric(ili$wk) < 18,] # CDC does not collect data for weeks after 17 in certain seasons. for consistency, do not include weeks 18-20 as "flu season" in the index

### coverage and careseeking adjustments ###
## ILI care seeking behavior estimates (Biggerstaff2012 and Biggerstaff2014): toddler, child, adult, elderly, total pop
careseek_TCAEt <- c(0.672, 0.515, 0.409, 0.573, 0.450)
### ILINet coverage adjustments ###
ili_seas0 <- aggregate(cbind(ili_0.4, ili_5.24, ili_25.64, ili_65., patients) ~ season, data = ilisub, sum)
patients14 <- ili_seas0[which(ili_seas0$season==14),]$patients # number of visits in 2014
ili_seas0$visitsRatio <- patients14/ili_seas0$patients
### merge population with ILI data ###
ili_seas <- merge(ili_seas0, totPop, by='season')
ili_seas$totpop <- ili_seas$toddlers0.5pop + ili_seas$children5.24pop + ili_seas$adults25.64pop + ili_seas$elderly65.pop

# age-specific adjusted ILI
ili_seas$adj_0.4 <- ili_seas$ili_0.4 * ili_seas$visitsRatio / careseek_TCAEt[1] / ili_seas$toddlers0.5pop * 10000
ili_seas$adj_5.24 <- ili_seas$ili_5.24 * ili_seas$visitsRatio / careseek_TCAEt[2] / ili_seas$children5.24pop * 10000
ili_seas$adj_25.64 <- ili_seas$ili_25.64 * ili_seas$visitsRatio / careseek_TCAEt[3] / ili_seas$adults25.64pop * 10000
ili_seas$adj_65. <- ili_seas$ili_65. * ili_seas$visitsRatio / careseek_TCAEt[4] / ili_seas$elderly65.pop * 10000
# calculate total adjusted ILI
ili_seas$ili_tot <- ili_seas$ili_0.4 + ili_seas$ili_5.24 + ili_seas$ili_25.64 + ili_seas$ili_65.
ili_seas$adj_tot <- ili_seas$ili_tot * ili_seas$visitsRatio / careseek_TCAEt[5] / ili_seas$totpop * 10000


## 11/5/14 RR, based on flu season adjusted AR ##
# function to calculate RR
calculateOR <- function(numeratorAR, denominatorAR){
  RR <- numeratorAR/denominatorAR
  return (RR)
}

ili_seas$OR_ac <- calculateOR(ili_seas$adj_25.64, ili_seas$adj_5.24)
ili_seas$OR_ce <- calculateOR(ili_seas$adj_5.24, ili_seas$adj_65.)
ili_seas$OR_ct <- calculateOR(ili_seas$adj_5.24, ili_seas$adj_0.4)
ili_seas$OR_ae <- calculateOR(ili_seas$adj_25.64, ili_seas$adj_65.)
ili_seas$OR_at <- calculateOR(ili_seas$adj_25.64, ili_seas$adj_0.4)

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
nat <- data.frame(season=dum2$season, benchmark=dum2$ixT_avg_noILI, H3=dum2$a_H3_prop, ili_t=dum2$adj_0.4, ili_c=dum2$adj_5.24, ili_a=dum2$adj_25.64, ili_e=dum2$adj_65., precip=dum2$mn_pcp, temp=dum2$mn_tavg, ili_tot=dum2$adj_tot, OR_ac=dum2$OR_ac, OR_ce=dum2$OR_ce, OR_ct=dum2$OR_ct, OR_ae=dum2$OR_ae, OR_at=dum2$OR_at)

# 7/20/15 write to file
# adjusted age-specific incidence for coverage and care-seeking
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(nat,'regression_data_ixT_v5.csv', row.names=FALSE) # 7/20/15 5:30 pm

###################################
## read data ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
nat <- read.csv('regression_data_ixT_v5.csv', header=T, colClasses='numeric')

###################################
## is the benchmark normally distributed? ##
qqnorm(nat$benchmark, ylab='benchmark index'); qqline(nat$benchmark, col=2)

###################################
## cross-correlation plots between covariates ##
# plot formatting
w = 464 
h = 464
ps = 14
margin = c(1, 4, 1, 4) + 0.1 # bottom, left, top, right
omargin = c(1, 1, 1, 1)
un = "px"
setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/SIFigures')

###################################
panel.hist <- function(x, ...)
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(usr[1:2], 0, 1.5) )
  h <- hist(x, plot = FALSE)
  breaks <- h$breaks; nB <- length(breaks)
  y <- h$counts; y <- y/max(y)
  rect(breaks[-nB], 0, breaks[-1], y, col = "blue", ...)
}
panel.cor <- function(x, y, digits = 2, prefix = "", cex.cor, ...)
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  r <- abs(cor(x, y))
  txt <- format(c(round(r, 3), 0.123456789), digits = digits)[1]
  txt <- paste0(prefix, txt)
  if(r>0.4) {cex.cor <- 1/strwidth(txt) * 0.8}
  else {cex.cor <- 1/strwidth(txt) * 0.4}
  text(0.5, 0.5, txt, cex = cex.cor)
}
cor.mtest <- function(mat, conf.level = 0.95){
  mat <- as.matrix(mat)
  n <- ncol(mat)
  p.mat <- lowCI.mat <- uppCI.mat <- matrix(NA, n, n)
  diag(p.mat) <- 0
  diag(lowCI.mat) <- diag(uppCI.mat) <- 1
  for(i in 1:(n-1)){
    for(j in (i+1):n){
      tmp <- cor.test(mat[,i], mat[,j], conf.level = conf.level)
      p.mat[i,j] <- p.mat[j,i] <- tmp$p.value
      lowCI.mat[i,j] <- lowCI.mat[j,i] <- tmp$conf.int[1]
      uppCI.mat[i,j] <- uppCI.mat[j,i] <- tmp$conf.int[2]
    }
  }
  return(list(p.mat, lowCI.mat, uppCI.mat))
}
###################################
# viz of correlation matrix
colindexes <- c(2:7, 10, 8, 9)
nat_sub <- nat[,colindexes]
cor.mx <- cor(nat_sub) # corr matrix
cor.pval <- cor.mtest(nat_sub,0.95) # p-values of correlation coefficients

par(mar = margin)
png(filename="corrmx_pairs.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
pairs(~benchmark + H3 + ili_t + ili_c + ili_a + ili_e + ili_tot + precip + temp, data=nat, diag.panel=panel.hist, upper.panel=panel.cor)
dev.off() 

# save fig: coefficients
par(mar = margin)
png(filename="corrmx_coefficients.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
corrplot(cor.mx, method='ellipse', type='lower', tl.col='black', diag=FALSE, addCoef.col='black')
dev.off() # saved 7/20/15 5:34 pm

# save fig: p-values
par(mar = margin)
png(filename="corrmx_pvalues.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
corrplot(cor.mx, method='ellipse', type='lower',tl.col='black', diag=FALSE, p.mat=cor.pval[[1]], insig='p-value', sig.level=-1)
dev.off()

# save fig: representation
par(mar = margin)
png(filename="corrmx_significant.png", units=un, width=w, height=h, pointsize=ps, bg = 'white')
corrplot(cor.mx, method='ellipse', type='lower', tl.col='black', diag=FALSE, p.mat=cor.pval[[1]], insig='pch', sig.level=0.05)
dev.off() # saved 7/20/15 5:34 pm

# 7/20/15: not in analysis
# # RR charts (nothing is significant with the benchmark)
# colindexes2 <- c(2, 3, 15, 11, 14, 13, 12, 8, 9)
# nat_sub2 <- nat[,colindexes2]
# cor.mx2 <- cor(nat_sub2)
# cor.pval2 <- cor.mtest(nat_sub2, 0.95)
# corrplot(cor.mx2, method='ellipse', type='lower', tl.col='black', diag=FALSE, p.mat=cor.pval2[[1]], insig='pch', sig.level=0.05, addCoef.col='black')

###################################
# ## nation level linear models ## 
# # leaps example
# leaps1 <- regsubsets(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp + ili_a + ili_c + ili_t + ili_e, data=nat, offset = ili_tot, nbest=10)
# summary(leaps1)
# plot(leaps1, scale='r2')

# # for steps adjacent to "best" model (lowest AIC model)
# # calculate delta AIC
# calculateDeltaAIC <- function(AICtable){
#   minAIC <- min(AICtable$AIC)
#   AICtable$deltaAIC <- AICtable$AIC - minAIC
#   return (AICtable)
# }
# # calculate Akaike weights (okay for nested models)
# calculateAkaikeWts <- function(AICtable){
#   if ('deltaAIC' %in% names(AICtable)){
#     numerators <- exp(-AICtable$deltaAIC/2)
#     denom <- sum(numerators)
#     AICtable$AkaikeWts <- numerators/denom
#   }
#   else {
#     AICtable <- calculateDeltaAIC(AICtable)
#     numerators <- exp(-AICtable$deltaAIC/2)
#     denom <- sum(numerators)
#     AICtable$AkaikeWts <- numerators/denom
#   }
#   return (AICtable)
# }


## no offset (ILIs) ##
Mnat3n <- lm(ix_noILI ~ H3_prop + precip + temp +  ili_a + ili_c + ili_t + ili_e, data=nat)
summary(Mnat3n)
# step3n <- stepAIC(Mnat3n, direction='both', k=log(dim(nat)[1])) # BIC
step3n <- stepAIC(Mnat3n, direction='both')
step3n$anova
Mnat3nf <- lm(ix_noILI ~ H3_prop+ temp + ili_a + ili_e, data=nat)
summary(Mnat3nf)

test <- lm(ix_noILI ~ H3_prop, data=nat)
summary(test)

plot(nat$ili_e, nat$temp)
plot(nat$ili_t, nat$temp)


## no offset (ORs) ##
Mnat2n <- lm(ix_noILI ~ H3_prop + precip + temp + OR_ac + OR_at + OR_ae, data=nat)
summary(Mnat2n)
step2n <- stepAIC(Mnat2n, direction='both')
step2n$anova
Mnat2nf <- lm(ix_noILI ~ H3_prop + temp + OR_ac, data=nat)
summary(Mnat2nf)

plot(nat$ili_a, nat$ix_noILI)
cor(nat$ili_tot, nat$ix_noILI)
# ###########################################################
# ## OFFSETS ##
# ## reg offset (all) ##
# Mnat1 <- lm(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp + ili_a + ili_c + ili_t + ili_e, data=nat, offset = ili_tot)
# summary(Mnat1)
# step1 <- stepAIC(Mnat1, direction='both')
# step1$anova
# Mnat1f <- lm(ix_noILI ~ H3_prop + temp + ili_a, data=nat, offset = ili_tot)
# summary(Mnat1f)
# # data frame for age-specific ILI and OR AIC results
# Mnat1_stepchanges <- c('none', '+OR_ce', '+ili_c', '+OR_ca', '+ili_t', '+ili_e', '+OR_ct', '+precip', '-temp', '-ili_a', '-H3_prop')
# # Mnat1_AIC <- c(19.526, 20.319, 20.711, 20.728, 21.132, 21.276, 21.494, 21.520, 24.389, 24.771, 26.992)
# # Mnat1_AICtab <- data.frame(steps = Mnat1_stepchanges, AIC = Mnat1_AIC)
# # Mnat1_AICtab_wts <- calculateAkaikeWts(Mnat1_AICtab)
# 
# ## log offset (all) ##
# Mnat1l <- lm(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp + ili_a + ili_c + ili_t + ili_e, data=nat, offset = log(ili_tot))
# summary(Mnat1l)
# step1l <- stepAIC(Mnat1l, direction='both')
# step1l$anova
# Mnat1lf <- lm(ix_noILI ~ H3_prop + temp + ili_a, data=nat, offset = log(ili_tot))
# summary(Mnat1lf)
# # data frame for age-specific ILI and OR AIC results
# Mnat1l_stepchanges <- c('none', '+OR_ce', '+ili_c', '+OR_ca', '+ili_e', '+ili_t', '+OR_ct', '+precip', '-temp', '-ili_a', '-H3_prop')
# # Mnat1l_AIC <- c(19.299, 20.321, 20.710, 20.772, 21.000, 21.072, 21.266, 21.297, 23.840, 23.878, 26.543)
# # Mnat1l_AICtab <- data.frame(steps = Mnat1l_stepchanges, AIC = Mnat1l_AIC)
# # Mnat1l_AICtab_wts <- calculateAkaikeWts(Mnat1l_AICtab)
# 
# ## reg offset (ORs) ##
# Mnat2 <- lm(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp, data=nat, offset = ili_tot)
# summary(Mnat2)
# step2 <- stepAIC(Mnat2, direction='both')
# step2$anova
# Mnat2f <- lm(ix_noILI ~ H3_prop + OR_ca + temp, data=nat, offset = ili_tot)
# summary(Mnat2f)
# # data frame for OR AIC results
# Mnat2_stepchanges <- c('none', '-OR_ca', '+OR_ce', '+OR_ct', '+precip', '-H3_prop', '-temp')
# # Mnat2_AIC <- c(24.285, 24.771, 24.871, 25.673, 26.235, 34.199, 34.439)
# # Mnat2_AICtab <- data.frame(steps = Mnat2_stepchanges, AIC = Mnat2_AIC)
# # Mnat2_AICtab_wts <- calculateAkaikeWts(Mnat2_AICtab)
# 
# ## log offset (ORs) ##
# Mnat2l <- lm(ix_noILI ~ H3_prop + OR_ca + OR_ce + OR_ct + precip + temp, data=nat, offset = log(ili_tot))
# summary(Mnat2l)
# step2l <- stepAIC(Mnat2l, direction='both')
# step2l$anova
# Mnat2lf <- lm(ix_noILI ~ H3_prop + OR_ca + temp, data=nat, offset = log(ili_tot))
# summary(Mnat2lf)
# # data frame for OR AIC results
# Mnat2l_stepchanges <- c('none', '-OR_ca', '+OR_ce', '+OR_ct', '+precip', '-H3_prop', '-temp')
# # Mnat2l_AIC <- c(23.404, 23.878, 24.104, 24.813, 25.383, 33.196, 33.232)
# # Mnat2l_AICtab <- data.frame(steps = Mnat2l_stepchanges, AIC = Mnat2l_AIC)
# # Mnat2l_AICtab_wts <- calculateAkaikeWts(Mnat2l_AICtab)
#
# ## log offset (ILIs) ##
# Mnat3l <- lm(ix_noILI ~ H3_prop + precip + temp +  ili_a + ili_c + ili_t + ili_e, data=nat, offset = log(ili_tot))
# summary(Mnat3l)
# step3l <- stepAIC(Mnat3l, direction='both')
# step3l$anova
# Mnat3lf <- lm(ix_noILI ~ H3_prop + temp + ili_a, data=nat, offset = log(ili_tot))
# summary(Mnat3lf)
# # dataframe for age-specific ILI AIC results (log ili_tot offset)
# Mnat3l_stepchanges <- c('none', '+ili_c', '+ili_e', '+ili_t', '+precip', '-temp', '-ili_a', '-H3_prop')
# # Mnat3l_AIC <- c(19.299, 20.710, 21.000, 21.072, 21.297, 23.840, 23.878, 26.543)
# # Mnat3l_AICtab <- data.frame(steps = Mnat3l_stepchanges, AIC = Mnat3l_AIC)
# # Mnat3l_AICtab_wts <- calculateAkaikeWts(Mnat3l_AICtab)
#
# ## reg offset (ILIs) ##
# Mnat3 <- lm(ix_noILI ~ H3_prop + precip + temp +  ili_a + ili_c + ili_t + ili_e, data=nat, offset = ili_tot)
# summary(Mnat3)
# step3 <- stepAIC(Mnat3, direction='both')
# step3$anova
# Mnat3f <- lm(ix_noILI ~ H3_prop + temp + ili_a, data=nat, offset = ili_tot)
# summary(Mnat3f)
# # dataframe for age-specific ILI AIC results (non log ili_tot offset)
# Mnat3_stepchanges <- c('none', '+ili_c', '+ili_t', '+ili_e', '+precip', '-temp', '-ili_a', '-H3_prop')
# # Mnat3_AIC <- c(19.526, 20.711, 21.132, 21.276, 21.520, 24.389, 24.771, 26.992)
# # Mnat3_AICtab <- data.frame(steps = Mnat3_stepchanges, AIC = Mnat3_AIC)
# # Mnat3_AICtab_wts <- calculateAkaikeWts(Mnat3_AICtab)

# ## EXTRAS ##
# ###################################
# ## state to region crosswalk ## 
# setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
# crosswalk <- read.csv('stateabbr_regnum_crosswalk.csv', header=T, colClasses = 'character')
# ###################################
# ## vaccine coverage by state ##
# setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Vaccines/Vax_Coverage')
# coverage <- read.csv('Vax_Coverage_WEAT_BRFSS.csv', header=T, colClasses = c('numeric', 'character', 'character', 'numeric', 'numeric', 'numeric', 'numeric'))

