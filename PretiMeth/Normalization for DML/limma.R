library(data.table)
library(limma)
#Quantile normalization for normal and cancer samples, respectively

#Normal sample set
data_b<-fread('D:\\NormTCGA\\BRCA450K\\BRCA_Normal_97.txt',sep='\t',header=TRUE,data.table = F, verbose = T, integer64 = 'numeric')

b <- data_b[1:nrow(data_b),2:ncol(data_b)]
Normeddata <- normalizeBetweenArrays(b)
Normeddata<- round(Normeddata,4)
data_b[1:nrow(data_b),2:ncol(data_b)] <- Normeddata

write.table(data_b,file="D:\\NormTCGA\\BRCA450K\\BRCA_Normal_97_Norm.txt",quote=FALSE,row.names = FALSE, col.names = TRUE,sep="\t")

#Tumor sample set
data_b<-fread('D:\\NormTCGA\\BRCA450K\\BRCA_Normal_97.txt',sep='\t',header=TRUE,data.table = F, verbose = T, integer64 = 'numeric')

b <- data_b[1:nrow(data_b),2:ncol(data_b)]
Normeddata <- normalizeBetweenArrays(b)
Normeddata<- round(Normeddata,4)
data_b[1:nrow(data_b),2:ncol(data_b)] <- Normeddata

write.table(data_b,file="D:\\NormTCGA\\BRCA450K\\BRCA_Normal_97_Norm.txt",quote=FALSE,row.names = FALSE, col.names = TRUE,sep="\t")
