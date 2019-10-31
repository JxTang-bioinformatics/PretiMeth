from __future__ import division
from sys import argv
import pandas as pd
import numpy as np
import os

#sigmoid
def sigmoid(x):
    return 1. / (1 + np.exp(-x))

##model for prediction     

if __name__ == '__main__':
    #All data located in the same directory
    DataPath = r'%s' % argv[1]
    #Input data     
    InputDataName = '%s' % argv[2]
                  
    path = r'%s\%s' % (DataPath,InputDataName) 
    i = 0
    for line in open(path):
        i += 1
        line=line.replace('\n','').split('	')
        if 'cg' in line[0]:
            break
                
    data = pd.read_csv(path,header=i-2,sep='\t')
    data = data[data['%s' % list(data)[2]]<0.05]
    data = data[['%s' % list(data)[0],'%s' % list(data)[1]]]
    D = list(data)[0]
    #match list
    path = r'%s/Parameter1.txt' % DataPath
    pre_table = pd.read_csv(path,header=0,sep='\t')
    
    data_all_pre = pre_table[['exp']]
    data_all_pre = data_all_pre.rename(columns={'exp':'%s' % list(data)[0]}) 
    
    #Model parameter
    path = r'%s/Parameter2.txt' % DataPath
    para1 = pd.read_csv(path,header=0,sep='\t')
        
    #Model evaluation index
    path = r'%s/logits_CV5_Evaluation.txt' % DataPath
    evaluation = pd.read_csv(path,header=0,sep='\t')    
    evaluation = evaluation.rename(columns={'cg':'%s' % list(data)[0]})    
    
    print ('Starting')
    
    #predicting
    for j in range(1,len(list(data))):
        a = list(data)[j] 
        data =  data[['%s' % list(data)[0],a]] 
                                                                       
        data = data.rename(columns={'%s' % list(data)[0]:'obs'}) 
        data1 = pd.merge(pre_table,data[['obs',a]] , how='inner', on='obs')
    
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
    
        df = pd.DataFrame(np.random.randn(len(pre1), 2), columns=['%s' % D ,'Pre_Value'])
        df['%s' % D] = list(data1['exp'])
        df['Pre_Value' ] = pre1
      
        data_all_pre = pd.merge(data_all_pre,df , how='left', on='%s' % D)
    
    data_all_pre = pd.merge(data_all_pre,evaluation , how='left', on='%s' % D)        
    #Output file
    file_dir = r'%s/OutputFile' % DataPath
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    data_all_pre.to_csv(r'%s/Prediction_for_%s' % (file_dir,InputDataName)  ,sep='\t',header=True,index=False,float_format='%.4f')    
    print('Done!')