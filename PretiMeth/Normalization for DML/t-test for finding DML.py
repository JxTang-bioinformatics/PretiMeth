from __future__ import division
import math
import pandas as pd
import numpy as np
import os
from scipy.stats import ttest_ind,levene

#file name of normal sample set
positive = 'BLCA_Normal_21_Pre_Norm'
#file name of tumor sample set
negative = 'BLCA_Tumor_419_Pre_Norm'

def p_adjust_bh(p):
    """Benjamini-Hochberg p-value correction for multiple hypothesis testing."""
    p = np.asfarray(p)
    by_descend = p.argsort()[::-1]
    by_orig = by_descend.argsort()
    steps = float(len(p)) / np.arange(len(p), 0, -1)
    q = np.minimum(1, np.minimum.accumulate(steps * p[by_descend]))
    return q[by_orig]  
    
    

#Normal
path = r'/home/tjx/TCGA/850K/%s.txt' % positive
normal = pd.read_csv(path,header=0,sep='\t')

#Tumor
path = r'/home/tjx/TCGA/850K/%s.txt' % negative
tumor = pd.read_csv(path,header=0,sep='\t')




normal_value = normal.values
tumor_value = tumor.values



loca = []
diff = []
n_num = []
t_num = []
n_mean = []
t_mean = []
pvalue = []
for i in range(len(normal_value)):
    n = normal_value[i,1:]
    t = tumor_value[i,1:]
    nn = []
    for j in range(len(n)):
        if math.isnan(n[j]):
            k = 0               
        else:
            nn.append(n[j])
    tt = []
    for j in range(len(t)):
        if math.isnan(t[j]):
            k = 0               
        else:
            tt.append(t[j])    
            
    if  (len(nn) != 0) and (len(tt) !=0 ): 
        if  ((np.mean(nn) != 0) and (np.mean(tt) != 0)) and ((np.mean(nn) != 1) and (np.mean(tt) != 1)) :           
            loca.append(normal_value[i,0])                                         
            diff.append(np.mean(nn)-np.mean(tt))
            n_num.append( len(nn) ) 
            t_num.append( len(tt) )
            n_mean.append(np.mean(nn))
            t_mean.append(np.mean(tt))
            #Analysis of variance and t-test
	    if levene(nn,tt)[1] > 0.05 :
                pvalue.append(ttest_ind(nn,tt,equal_var=True)[1])
            else:
                pvalue.append(ttest_ind(nn,tt,equal_var=False)[1])


df = pd.DataFrame(np.random.randn(len(pvalue), 7), columns=['ID', 'n_num', 't_num','n_mean','t_mean', 'diff' , 'pvalue'])
df['ID'] = loca
df['n_num'] = n_num
df['t_num'] = t_num
df['n_mean'] = n_mean
df['t_mean'] = t_mean
df['diff'] = diff
df['pvalue'] = pvalue
df = df.dropna(axis=0,how='any') 
#Convert to q-values
adj =  p_adjust_bh(list(df['pvalue']))   
df['adj.Pval'] = list(adj)    

#Output file   
df.to_csv(r'/home/tjx/TCGA/DMLs/850k/%s.txt' % negative.split('_')[0] ,sep='\t',header=True,index=False)    
 
