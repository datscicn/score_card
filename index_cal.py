# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 12:59:08 2018

@author: longding
"""

#% 4.计算PSI，无法计算时()，返回-1
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

def get_trend_type(bd):
    bd=[x for x in list(bd) if type(x)!=type([])]
    if len(bd)>1:
        if get_seq_rank(bd)==100:
            trend_type='DESC'
        elif get_seq_rank(bd)==0:
            trend_type='ASC'
        elif bd.index(min(bd))*(len(bd)-1-bd.index(min(bd)))>0:
            if get_seq_rank(bd[0:bd.index(min(bd))+1])==100 and get_seq_rank(bd[bd.index(min(bd)):])==0:
                trend_type='U'
            else:
                trend_type=''
        elif bd.index(max(bd))*(len(bd)-1-bd.index(max(bd)))>0:
            if get_seq_rank(bd[0:bd.index(max(bd))+1])==0 and get_seq_rank(bd[bd.index(max(bd)):])==100:
                trend_type='DU'
            else:
                trend_type=''
        else:
                trend_type=''
    else:
        trend_type=''
    return trend_type
#% 7 排序指标
def get_seq_rank(x):
    '''
    value:0-100
    0   for min to max
    100 for max to min
    '''
    ls=list(x)
#    for i in range(sum([1 for xx in ls if xx==[]])):    ls.remove([])
    if [] in ls :ls.remove([])
    r=0;max_r=int(len(ls)*(len(ls)-1)/2)
    for i in range(1,len(ls)):
        r=r+sum([x>ls[i] for x in ls[0:i]])
    rank=int(r/max_r*100)
    return rank
def get_vif(f,fs,data):
    from sklearn import linear_model
    LM=linear_model.LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
    fs_=[x for x in fs if x!=f]
    X=data[fs_]
    y=data[f]
    LM.fit(X,y)
    y_pre=(LM.coef_* X).sum(axis=1)+LM.intercept_
    r2=1.0-((y-y_pre)**2).sum()/((y-y.mean())**2).sum()
    vif=1/(1-r2)
    return vif