library(impute)
library(data.table)
#Samples for imputing
#25 complete data and one with missing value data for testing
dataforpre<-fread('C:\\Users\\tjx\\Desktop\\pre0907\\GSM3902399-248064_forknnpre_A.txt',sep='\t',header=TRUE,data.table = F, verbose = T, integer64 = 'numeric')

set.seed(12345)
saved.state <- .Random.seed
dataforpre.imputed <- impute.knn(as.matrix(dataforpre))
# Assuming all goes well with no guarantees in case of error...
.Random.seed <- dataforpre.imputed$rng.state
sum(saved.state - dataforpre.imputed$rng.state) # should be zero!
#Output file
write.table(dataforpre.imputed$data,file="C:\\Users\\tjx\\Desktop\\pre0907\\imputeknn\\dataforpre_imputation_A.txt",quote=FALSE,row.names = FALSE, col.names = TRUE,sep="\t")
