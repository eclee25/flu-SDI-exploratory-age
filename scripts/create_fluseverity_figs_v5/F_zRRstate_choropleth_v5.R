
## Name: Elizabeth Lee
## Date: 11/2/14
## Function: Draw retrospective zOR choropleth of states
### Extract mean zOR data by state from create_fluseverity_figs_v5/export_zRR_classifState_v5.py
### Filename: /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_7st.csv
## Data Source: 
## Notes: ggplot2 references: http://blog.revolutionanalytics.com/2009/11/choropleth-challenge-result.html
# 7/21/15: update notation
# 7/22/15: reduce margin sizes, similar to F_state_accuracy_choropleth
# 7/30/15: update state notation
# 10/15/15: change legend
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")


######## header #################################
rm(list = ls())
require(maps)
require(ggplot2)
require(grid)
setwd(dirname(sys.frame(1)$ofile)) # only works if you source the program

# plot formatting
mar = c(0,0,0,0)

#########################################
## plot data by state (statelevel classif) ##
setwd('../../Py_export')
orig2 <- read.csv('SDI_state_classif_covCareAdj_v5_7st.csv', header=TRUE, colClasses = c('numeric', 'character', 'numeric', 'numeric'))
names(orig2) <- c('season', 'state', 'retro_zOR', 'early_zOR', 'valid_normweeks')
orig2$mean_retro_zOR <- cut(orig2$retro_zOR, breaks = seq(-10, 14, by=3), ordered_result=TRUE)
# 11/2/14: reverse order of levels so that severe values are red and at the top of the legend
orig2$mean_retro_zOR <- factor(orig2$mean_retro_zOR, levels=rev(levels(orig2$mean_retro_zOR)))

# crosswalk state names with call letter abbreviations
setwd('../../../Census')
abbr <- read.csv('state_abbreviations.csv', header=TRUE, colClasses='character')
names(abbr) <- c('region', 'state')
abbr$region <- tolower(abbr$region) # convert state names to lower case because orig2 state names are lower case
orig3 <- merge(orig2, abbr, by = 'state', all=T)

us_state_map <- map_data('state')
setwd('../Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission3_ID/AddlFigures')

for (seas in 2:9){
  plotdata <- tbl_df(orig3) %>% filter(season==seas)
  seasonmap2 <- ggplot(plotdata, aes(map_id = region)) +
    geom_map(aes(fill = mean_retro_zOR), map = us_state_map, color = 'black') +
    scale_fill_brewer(expression(paste('severity, ', bar(rho["s,r"](tau)))), palette = 'RdYlBu', guide = 'legend', drop = F) +
    expand_limits(x = us_state_map$long, y = us_state_map$lat) +
    theme_minimal(base_size = 16, base_family = "") +
    theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank(), plot.margin = unit(mar, "mm")) +
    labs(x=NULL, y=NULL) 
  ggsave(seasonmap2, width=5, height=3, file=sprintf('RetrozRR_State_Season%s_stlvl.png', seas))
}
# 10/15/15


