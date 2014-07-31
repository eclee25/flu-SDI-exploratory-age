setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
acc <- read.csv('SDI_state_accuracy_counts_stlvl.csv', colClasses=c('character', 'numeric', 'numeric'), header=TRUE)

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/graph_outputs/current_14_7_3/regional')
png(filename="state_classif_accuracy_stlvl.png", width=600, height=400, units='px', bg = 'white')
par(mfrow = c(1,2))

hist(acc$early_retro, ylab='Number of States', xlab='Correct Classifications', main='state early warning matches\n state retrospective', ylim=c(0,25))
hist(acc$retro_retro, ylab='Number of States', xlab='Correct Classifications', main='state retrospective matches\n state retrospective', ylim=c(0,15))

dev.off()


setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
acc <- read.csv('SDI_state_accuracy_counts.csv', colClasses=c('character', 'numeric', 'numeric'), header=TRUE)

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/graph_outputs/current_14_7_3/regional')
png(filename="state_classif_accuracy.png", width=600, height=400, units='px', bg = 'white')
par(mfrow = c(1,2))

hist(acc$early_retro, ylab='Number of States', xlab='Correct Classifications', main='state early warning matches\n national retrospective', ylim=c(0,25))
hist(acc$retro_retro, ylab='Number of States', xlab='Correct Classifications', main='state retrospective matches\n national retrospective', ylim=c(0,15))

dev.off()

