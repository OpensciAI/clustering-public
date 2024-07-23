library(IsingFit)
library(qgraph)

data <- read.csv('csv/symptoms_withhf_premenopause_onehot.csv')

# Drop columns with very little variance so IsingFit does not complain.
#data$nipple_discharge <- NULL

#data$ovulation_pain <- NULL
#data$ovulation <- NULL

#data$hot_flashes <- NULL
#data$night_sweats <- NULL

Res <- IsingFit(data, family = 'binomial')

Res$weiadj
