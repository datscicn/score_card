# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 17:47:07 2018

@author: longding
"""

def get_val_coarse_class_table(validations,coarse_class_table,special_value,val_bad_var,val_good_var):
    from score_card import binclass
    bin_table=coarse_class_table[['feature','group_id','isnormal','min_bin','max_bin']]
    coarse_class_table_vals=[];iv_vals=[];ks_vals=[];psis=[]
    for val in validations:
        coarse_class_table_val,iv_val,ks_val=binclass.get_Fine_Classing(val,bin_table,val_bad_var,val_good_var,is_mean_value=False)
        coarse_class_table_vals.append(coarse_class_table_val);iv_vals.append(iv_val);ks_vals.append(ks_val)
        x1=coarse_class_table['total_pct'][coarse_class_table['isnormal']=='normal']
        x2=coarse_class_table_val['total_pct'][coarse_class_table_val['isnormal']=='normal']
        psis.append(get_psi(x1,x2))
    return coarse_class_table_vals,iv_vals,ks_vals,psis

def get_psi(x1,x2):
    import math
    x1_sum=sum(x1);x2_sum=sum(x2)
    x1_=[x/x1_sum*1.0 for x in x1]
    x2_=[x/x2_sum*1.0 for x in x2]
    x_=[x2_[i]/x1_[i] for i in list(range(len(x1)))]
    x_abs=[math.ceil(abs(i)) for i in x_]
    if 0 in x_abs:
        psi=-1
    else:
        psi_=[math.log(x_[i])*(x2_[i]-x1_[i]) for i in list(range(len(x_)))]
        psi=sum(psi_)
    return psi

def get_corr_delet(corr,ma=0.7):
    fe=list(corr.columns)
    for i in range(len(fe)):
        if sum(corr[fe[len(fe)-i-1]]>ma)>1:
            corr=corr.drop(fe[len(fe)-i-1], axis=0)
            corr=corr.drop(fe[len(fe)-i-1], axis=1)
    fe_fn=list(corr.columns)
    return fe_fn,corr
def to_score(p):
    import numpy as np
    pp=p-0.0001*(p==1)+0.0001*(p==0);#if prob=1 or 0
    ppp=np.log((1-pp)/pp);
    base=777;odds=100;pdo=44;factor=pdo/np.log(2);offset=base-pdo*np.log(odds)/np.log(2);
    score_=np.round(factor*ppp+offset)
    score=[int(i)  for i in score_]
    return score;

