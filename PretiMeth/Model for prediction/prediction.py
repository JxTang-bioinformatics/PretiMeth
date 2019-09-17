from __future__ import division
import pandas as pd
import numpy as np
import os
import math
#sigmoid
def sigmoid(x):
    return 1. / (1 + np.exp(-x))


#sample for prediction
path = r'/home/tjx/single_locus_prediction/independent_test/GSM2883349-42710.txt' 
#Header is set according to different files
data = pd.read_csv(path,header=3,sep='\t')
data = data[data['Detection Pval']<0.05]
data = data[['ID','VALUE']]

#match list
path = r'/home/tjx/single_locus_prediction/exp with obs match table_0528.txt'
pre_table = pd.read_csv(path,header=0,sep='\t')

data_all_pre = pre_table[['exp']]
data_all_pre = data_all_pre.rename(columns={'exp':'ID'}) 

#Model parameter
path = r'/home/tjx/single_locus_prediction/results/logits_para_model_Ms_0528.txt'
para1 = pd.read_csv(path,header=0,sep='\t')

#predicting
for j in range(1,len(list(data))):
    a = list(data)[j] 
    data =  data[['ID',a]] 
                                                                   
    data = data.rename(columns={'ID':'obs'}) 
    data1 = pd.merge(pre_table,data[['obs',a]] , how='inner', on='obs')
    '''
    data = data.rename(columns={'x1_obs':'x2_obs'}) 
    data1 = pd.merge(data1,data[['x2_obs',a]] , how='inner', on='x2_obs')
    '''
    data1 = data1.sort_values(axis = 0,ascending = True,by = 'exp')  
    data1 = data1.reset_index(drop = True)
             
    para = para1[para1.exp.isin(list(data1['exp']))]
    para = para.sort_values(axis = 0,ascending = True,by = 'exp')  
    para = para.reset_index(drop = True)
    
    para_value = para.values
    data1_value = data1.values
    
    pre1 = []
    
    for i in range(len(data1_value)):
        x1 = data1_value[i,2]*para_value[i,1] + para_value[i,2]      
        pre1.append( sigmoid(x1) )       

    df = pd.DataFrame(np.random.randn(len(pre1), 2), columns=['ID' ,'%s' % a ])
    df['ID'] = list(data1['exp'])
    df['%s' % a ] = pre1
  
    data_all_pre = pd.merge(data_all_pre,df , how='left', on='ID')

#Output file
data_all_pre.to_csv(r'/home/tjx/single_locus_prediction/independent_test/850kCpG_test_sample138_f4_logit_pre_Ms.txt'  ,sep='\t',header=True,index=False,float_format='%.4f')    

