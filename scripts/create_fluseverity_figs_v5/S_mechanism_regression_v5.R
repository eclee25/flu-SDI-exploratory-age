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
setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/SIFigures')

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
  return(list(R, p.value = pval))
}

cor.permtest <- function(mat, conf.level = 0.95){
  mat <- as.matrix(mat)
  n <- ncol(mat)
  p.mat <- matrix(NA, n, n)
  diag(p.mat) <- 0
  for(i in 1:(n-1)){
    for(j in (i+1):n){
      tmp <- permTest(mat[,i], mat[,j])
      p.mat[i,j] <- p.mat[j,i] <- tmp$p.value
    }
  }
  return(list(p.mat))
}

###################################
# viz of correlation matrix
colindexes <- c(2:7, 10, 8, 9)
nat_sub <- nat[,colindexes]
cor.mx <- cor(nat_sub) # corr matrix
cor.pval <- cor.permtest(nat_sub) # p-values of correlation coefficients

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


