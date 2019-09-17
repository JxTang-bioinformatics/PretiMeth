# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:19:12 2019

@author: 50230
"""


from __future__ import division
import math
import pandas as pd
import numpy as np
import os
import statsmodels.formula.api as smf
import sklearn.metrics as skl
from sklearn.model_selection import KFold
from scipy import stats 
def pearson(x,y):
   return stats.pearsonr(x,y)
#sigmoid
def sigmoid(x):
    return 1. / (1 + np.exp(-x))  

###############################
#Set up 5-fold cross validation
kf = KFold(n_splits=5)

#Match list
read_path=r'/home/tjx/single_locus_prediction/exp with obs match table_0528.txt'
f=open(read_path) 
data_=pd.read_csv(f,sep='	',header=0,index_col=None)

#model loci data for training
read_path=r'/home/tjx/single_locus_prediction/850kCpG_train_sample_665_exp413719_f4_Norm.txt' 
f=open(read_path) 
sheet_exp_=pd.read_csv(f,sep='	',header=None,index_col=0)
sheet_exp_=sheet_exp_
#feature loci data for training
read_path=r'/home/tjx/single_locus_prediction/850kCpG_train_sample_665_obs450137_f4_Norm.txt' 
f=open(read_path) 
sheet_obs_=pd.read_csv(f,sep='	',header=None,index_col=0)
sheet_obs_=sheet_obs_
#In order to perform parallel calculation on the server, 413,719 sites are divided into four groups of 0, 1, 2, and 3, which were defined as the num.
for the_num in [0]:
    print(the_num)
    range_=list(range(the_num*110000,min(110000*(the_num+1),len(data_))))
    sheet_exp=sheet_exp_.loc[data_['%s' % list(data_)[0]].loc[range_]] 
    sheet_obs=sheet_obs_.loc[data_['%s' % list(data_)[1]].loc[range_]]  
    sheet_obs=sheet_obs.drop_duplicates()
    data=np.array(data_)
    
    
    #Model evaluation index, including: RMSE, MAE, R-Square,SP,SE,MCC,ACC,AUC and Pearson correlation coefficient.
    #MS:use only feature loci

    
    Ms_mse = []
    Ms_mae = []
    Ms_r2 = []
    Ms_sp = []
    Ms_se = []
    Ms_acc = []
    Ms_auc = []
    
    Ms_precision = []
    Ms_recall = []
    
    Ms_mcc = []
    Ms_pearson = []
    #Positive and negative sample size for each loci
    Ms_num = []
    Ms_p_num = []
    Ms_n_num = []
    
    #Site number
    cg_name = []
    #Model parameter
    
    coef_ms_1 = []
    intercept_ms_1 = []   
    
    #model: Logistic    
    typ = 'logits'
        
    for i in range(the_num*110000,min(110000*(the_num+1),len(data))):
        #Load data        
        if i%100 == 0:
            print(i)     
        cg_exp=data[i][0]
        cg_obs1=data[i][1]
        
    
        cg_data=pd.concat([sheet_exp.loc[cg_exp],sheet_obs.loc[cg_obs1]],axis=1,ignore_index=True)
    
        cg_data.dropna(axis=0, how='any', inplace=True)
        cg_data.index = range(len(cg_data))
        
        y=cg_data[0]
        x=cg_data[list(cg_data)[1:]]
        x['Intercept'] =1	
        
        Ms_num.append(len(cg_data))
        Ms_p_num.append(sum(cg_data[0]>=0.5))
        Ms_n_num.append(sum(cg_data[0]<0.5))
        
        y_t = []
        for j in range(len(y)):
            if y[j] >= 0.5 :
                y_t.append(1)
            if y[j] < 0.5 :
                y_t.append(0) 
        y_t = np.array(y_t)
        ####
    
        o_r2 = []
        o_mse = []
        o_mae = []
        o_sp = []
        o_se = []
        o_acc = [] 
        o_auc = []
    
        o_precision = []
        o_recall = []
    	
        o_mcc =[]
        o_pearson = []
    

        ####
        #cross validation
        for train_index, test_index in kf.split(x, y):
            X_train, X_test = x.iloc[train_index], x.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]        
    				#Fitting model
            reg = smf.Logit(y_train, X_train[[list(X_train)[0]]+[list(X_train)[1]]]).fit(disp=0)		   
            pred_y = list(reg.predict(X_test[[list(X_test)[0]]+[list(X_test)[1]]]))
            o_pearson.append( pearson(y_test,pred_y)[0])		  
            pred_y_o = list(pred_y)
            o_r2.append(skl.r2_score(y_test,pred_y))
            o_mse.append( (skl.mean_squared_error(y_test,pred_y))**0.5 )
            o_mae.append(skl.mean_absolute_error(y_test,pred_y))
    
            for j in range(len(pred_y)):
                if pred_y[j] >= 0.5 :
                    pred_y[j] = 1
                if pred_y[j] < 0.5 :
                    pred_y[j] = 0   
                    
            TP = 0
            FP = 0
            FN = 0
            TN = 0 
            y_true = y_t[test_index]
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
    
            if (TN + FP) != 0:
                o_sp.append( (1 - FP / (TN + FP)) )
            else:
                o_sp.append(1)   
            if (TP + FN) != 0:
                o_se.append( TP/(TP + FN) )
            else:
                o_se.append(1)              
            
            o_acc.append(skl.accuracy_score(y_true,pred_y))
            if ((TP + FN) == 0 )or((TN + FP) == 0):
                o_auc.append( 1 )
            else:
                o_auc.append( skl.roc_auc_score(y_true,pred_y_o) )
    
            
            if (TP+FP) != 0:
                o_precision.append( TP/(TP+FP) ) 
            else:
                o_precision.append( 1 )  
            if (TP+FN) != 0:
                o_recall.append( TP/(TP+FN) ) 
            else:
                o_recall.append( 1 )  
    			
            if 	 (TN+FN)*(TN+FP)*(TP+FN)*(TP+FP) != 0:
                o_mcc.append( (TP*TN-FP*FN)/(((TN+FN)*(TN+FP)*(TP+FN)*(TP+FP))**0.5))
            else:
                o_mcc.append(0)
	   
        
        Ms_r2.append(np.mean(o_r2))
        Ms_mse.append(np.mean(o_mse))
        Ms_mae.append(np.mean(o_mae))
        Ms_sp.append(np.mean(o_sp))
        Ms_se.append(np.mean(o_se))   
        Ms_acc.append(np.mean(o_acc))
        Ms_auc.append(np.mean(o_auc))    
        Ms_mcc.append(np.mean(o_mcc))
        Ms_pearson.append(np.mean(o_pearson))
    	
  
       
        Ms_precision.append(np.mean(o_precision))
        Ms_recall.append(np.mean(o_recall))  
    
      
        
				#Fitting final model    	
        reg = smf.Logit(y, x[ [list(x)[0]]+[list(x)[1]] ]).fit(disp=0)
        #Storage parameter
        coef_ms_1.append(reg.params[1])
        intercept_ms_1.append(reg.params['Intercept'])  
                  
        cg_name.append(cg_exp)
        
       
    
    
      
    
    df = pd.DataFrame(np.random.randn(len(cg_name), 12), columns=['cg','rmse','mae','precision','recall','r2','sp','se','acc','auc','mcc','pearson'])
    df['cg'] = cg_name
    df['precision'] = Ms_precision
    df['recall'] = Ms_recall
    df['rmse'] = Ms_mse
    df['mae'] = Ms_mae
    df['r2'] = Ms_r2
    df['sp'] = Ms_sp
    df['se'] = Ms_se
    df['acc'] = Ms_acc
    df['auc'] = Ms_auc
    df['mcc'] = Ms_mcc
    df['pearson'] = Ms_pearson
    df.to_csv(r'/home/tjx/single_locus_prediction/%d_%s_CV5_Evaluation_model_Ms.txt' % (the_num,typ) ,sep='\t',index=False)    
    
    
    
    df = pd.DataFrame(np.random.randn(len(coef_ms_1), 3), columns=['exp','coef','intercept'])
    df['exp'] = cg_name
    df['coef'] = coef_ms_1
    df['intercept'] = intercept_ms_1
    df.to_csv(r'/home/tjx/single_locus_prediction/%d_%s_para_model_Ms.txt' % (the_num,typ) ,sep='\t',index=False)    
    
    df = pd.DataFrame(np.random.randn(len(cg_name),4), columns=['cg','all_num','hyper','hypor'])
    df['cg'] = cg_name
    df['all_num'] = Ms_num
    df['hyper'] = Ms_p_num
    df['hypor'] = Ms_n_num
    df.to_csv(r'/home/tjx/single_locus_prediction/%d_%s_samplenum_Ms.txt' % (the_num,typ) ,sep='\t',index=False)    
    
     
  

