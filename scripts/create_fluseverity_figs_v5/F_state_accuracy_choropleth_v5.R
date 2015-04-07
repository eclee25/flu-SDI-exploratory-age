
## Name: Elizabeth Lee
## Date: 11/2/14
## Function: Draw choropleth where scale counts number of correct matches: early (state lvl) to retro (national lvl), retro (state) to retro (national), and early (state) to retro (state)
### Extract classification counts by state from create_fluseverity_figs_v5/evaluate_state_early_warning_v5.py 
## Data Source: Py_export/SDI_state_accuracy_counts_covCareAdj_v5.csv
## Notes: ggplot2 references: http://blog.revolutionanalytics.com/2009/11/choropleth-challenge-result.html
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

setwd('/home/elee/R/source_functions')
source("dfsumm.R")

require(maps)
require(ggplot2)

#########################################
## plot formatting
leg_sz = 1.5
#########################################
## plot data by state ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
# 2/23/15 add NA strings
orig2 <- read.csv('SDI_state_accuracy_counts_covCareAdj_v5.csv', na.strings = '-99', header=TRUE, colClasses = c('character', 'factor', 'factor', 'factor'))
names(orig2) <- c('state', 'earlyst_retronat', 'retrost_retronat', 'earlyst_retrost') # state is state call letter

# crosswalk state names with call letter abbreviations
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census')
abbr <- read.csv('state_abbreviations.csv', header=TRUE, colClasses='character')
names(abbr) <- c('region', 'state')
abbr$region <- tolower(abbr$region) # convert state names to lower case because orig2 state names are lower case
orig3 <- merge(orig2, abbr, by = 'state', all=T)

us_state_map <- map_data('state')
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/fluseverity_figs_v5')

choropleth2 <- merge(us_state_map, orig3, by='region', all=T)
choropleth2 <- choropleth2[order(choropleth2$order),]

# early warning state match retrospective national
map_est_rnat <- ggplot(choropleth2, aes(long, lat, group=group)) +
  geom_polygon(aes(fill=earlyst_retronat), size = 0.2) +
  geom_polygon(data=us_state_map, color='white', fill=NA) +
  theme_minimal(base_size = 12, base_family = "") +
  theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
    labs(x=NULL, y=NULL) +
  scale_fill_brewer("matches", type='seq', palette=2, labels=levels(orig3$earlyst_retronat), drop=FALSE) + 
  ggtitle('state early warning & national retrospective')
ggsave(map_est_rnat, width=5, height=3, file='earlySt_retroNat_matchCt_stlvl.png') 

# retrospective state match retrospective national
map_rst_rnat <- ggplot(choropleth2, aes(long, lat, group=group)) +
  geom_polygon(aes(fill=retrost_retronat), size = 0.2) +
  geom_polygon(data=us_state_map, color='white', fill=NA) +
  theme_minimal(base_size = 12, base_family = "") +
  theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
  labs(x=NULL, y=NULL) +
  scale_fill_brewer("matches", type='seq', palette=11, labels=levels(orig3$retrost_retronat), drop=FALSE) + 
  ggtitle('state & national retrospective')
ggsave(map_rst_rnat, width=5, height=3, file='retroSt_retroNat_matchCt_stlvl.png') 

# early warning state match retrospective state
map_est_rst <- ggplot(choropleth2, aes(long, lat, group=group)) +
  geom_polygon(aes(fill=earlyst_retrost), size = 0.2) +
  geom_polygon(data=us_state_map, color='white', fill=NA) +
  theme_minimal(base_size = 12, base_family = "") +
  theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
  labs(x=NULL, y=NULL) +
  scale_fill_brewer("matches", type='seq', palette=3, labels=levels(orig3$earlyst_retrost), drop=FALSE) + 
  ggtitle('state early warning & retrospective')
ggsave(map_est_rst, width=5, height=3, file='earlySt_retroSt_matchCt_stlvl.png') 

