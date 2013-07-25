library(ggplot2)
library(zipcode)

#zipcode_weighted file has list of nodes and data (nodes = zipcodes, data = OR or incidence)
communities <- read.csv('zipcode_weighted.txt', header=F, sep=",")
data(zipcode)
mergeddata = merge(communities, zipcode, by.x='zip', by.y='zip')

#b <- c(0,1,2,3,5,6,7,8,10,15,16,17,18,28)
b <- scan('zipcode_unique_commid.txt')
r = data.frame(comm=b,kolor=rainbow(length(b)))

mergetwo <- merge(mergeddata, r, by.x='V2', by.y='comm')
g = ggplot(data=mergetwo) + geom_point(aes(x=longitude, y=latitude, color=kolor), size=1) + scale_colour_identity()
g = g + labs(x=NULL, y=NULL)
g = g + opts(panel.background = theme_blank(), panel.grid.major = theme_blank(), panel.grid.minor = theme_blank(), legend.position = "none", axis.ticks = theme_blank(), axis.text.y = theme_blank(), axis.text.x = theme_blank())
ggsave(g, width=6, height=4, filename="zipcode_weighted.png")


#b <- c(0,1,2,3,5,6,7,8,10,15,16,17,18,28)
#g = ggplot(data=mergeddata) + geom_point(aes(x=longitude, y=latitude, colour=V2, group=V2)) 

# g = g + theme_bw() + scale_x_continuous(limits = c(-125, -66), breaks=NA)
# g = g + scale_y_continuous(limits=c(25,50), breaks=NA)

# r <- scan('colors.txt', what="")
# r <- c("#FF0000","#FFFFFF","#00FFFF","#C0C0C0","#0000FF","#808080","#0000A0","#000000","#FF0080","#FFA500","#800080","#A52A2A","#FFF00","#800000","#00FF00","#008000","#FF00FF","#808000","#56A5EC")

# g = g + scale_colour_manual(values=r, breaks=b)
# g = g + scale_colour_manual(values=r)
# g = g + scale_colour_brewer(palette="Spectral", breaks=b)

# g = g + scale_colour_gradientn(breaks=b, labels=format(b), colours=rainbow(40))
# g = g + labs(x=NULL, y=NULL)
# ggsave(g, width=6, height=4, filename="zips.png")
