from __future__ import division
import pandas as pd
import numpy as np
import os
import math
import sklearn.metrics as skl
from scipy import stats 
def pearson(x,y):
   return stats.pearsonr(x,y)
#sigmoid
def sigmoid(x):
    return 1. / (1 + np.exp(-x))

#Experimental data
path = r'/home/tjx/single_locus_prediction/independent_test/850kCpG_test_sample138_f4.txt' 
data_norm = pd.read_csv(path,header=0,sep='\t')
#Prediction data
path = r'/home/tjx/single_locus_prediction/independent_test/850kCpG_test_sample138_f4_logit_pre_Ms.txt'
data_pre = pd.read_csv(path,header=0,sep='\t')

p =[]
rmse= []
mae =[]
se=[]
sp=[]
mcc=[]
acc=[]
auc=[]
    
for i in range(1,len(list(data_norm))):

   
    a = list(data_norm)[i] 
    data_r =  data_norm[['ID',a]]                                                                    
    data_r = data_r.rename(columns={a:'real'}) 
    data_p =  data_pre[['ID',a]]                                                                    
    data_p = data_p.rename(columns={a:'pre'})    	    
    data = pd.merge(data_r,data_p , how='inner', on='ID')
    data = data.dropna(axis=0,how='any')

		
    y_r = list(data['real'])
    y_p = list(data['pre'])
		
    p.append( pearson(y_r,y_p)[0] )   
    rmse.append( (skl.mean_squared_error(y_r,y_p))**0.5 )
    mae.append(skl.mean_absolute_error(y_r,y_p))
    
    pred_y = []
    for j in range(len(y_p)):
        if y_p[j] >= 0.5 :
            pred_y.append( 1)
        if y_p[j] < 0.5 :
            pred_y.append( 0)  
    y_true = []        
    for j in range(len(y_r)):
        if y_r[j] >= 0.5 :
            y_true.append( 1)
        if y_r[j] < 0.5 :
            y_true.append( 0) 

            
    TP = 0
    FP = 0
    FN = 0
    TN = 0 

    for j in range(len(y_true)):
        if y_true[j] == 1:
            if pred_y[j] == 1:
                TP += 1
            else:
                FN += 1
        if y_true[j] == 0:
            if pred_y[j] == 0:
                TN += 1
            else:
                FP += 1            
    

    sp.append( (1 - FP / (TN + FP)) )   
    se.append( TP/(TP + FN) )               
    acc.append(skl.accuracy_score(y_true,pred_y))
    auc.append( skl.roc_auc_score(y_true,y_p) ) 	
    mcc.append( (TP*TN-FP*FN)/(((TN+FN)*(TN+FP)*(TP+FN)*(TP+FP))**0.5))




df = pd.DataFrame(np.random.randn(len(p), 8), columns=['rmse','mae','r','sp','se','acc','auc','mcc'])
df['rmse'] = rmse
df['mae'] = mae
df['r'] = p
df['sp'] = sp
df['se'] = se
df['acc'] = acc
df['auc'] = auc
df['mcc'] = mcc

#Output file       
df.to_csv(r'/home/tjx/single_locus_prediction/independent_test/independent_test_evaluation.txt'   ,sep='\t',header=True,index=False)    

