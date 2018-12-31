# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 18:52:25 2018

@author: longding
"""

def get_woe_var(modeling,coarse_class_table):
    import pandas as pd
    f=coarse_class_table.feature[0]
    x=modeling[f]
    w=pd.Series([0]*len(x));w.name='w_'+f
    all_index=list(modeling.index)
    remain_index=list(modeling.index)
    for i in range(len(coarse_class_table)):
        lgk_rm=[w1==0 for w1 in w]
        if coarse_class_table.isnormal[i]=='abnormal':
            lgk=((x==coarse_class_table.min_bin[i])&lgk_rm)
        elif (coarse_class_table.min_bin[i]=='min') & (coarse_class_table.max_bin[i]=='max'):
            lgk=(([x1 not in list(coarse_class_table['min_bin'][coarse_class_table['isnormal']=='abnormal']) for x1 in x]) and lgk_rm)         
        elif coarse_class_table.min_bin[i]=='min':
            lgk=((x<=coarse_class_table.max_bin[i])&lgk_rm)
        elif coarse_class_table.max_bin[i]=='max':
            lgk=((x>coarse_class_table.min_bin[i])&lgk_rm)
        else:
            lgk=((x<=coarse_class_table.max_bin[i])&(x>coarse_class_table.min_bin[i])&lgk_rm)
        w[lgk]=coarse_class_table.woe[i]
    return w


def get_trend_type(class_table):
    bd=list(class_table['bad_rate'][class_table['isnormal']=='normal'])
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

def woe_to_score(woe,model_features,coef_table,f_i):
    score_g=((-woe)*coef_table['coef'][f_i+1]-coef_table['coef'][0]/len(model_features))*63.48 +484.67/len(model_features)
    return score_g

def bin_table_add_score(bin_table,model_features,coef_table):
    s=[]
    for i in range(len(bin_table['feature'])):
        f=bin_table['feature'][i]
        f_i=model_features.index('w_'+f)
        s.append(int(round(woe_to_score(bin_table['woe'][i],model_features,coef_table,f_i))))
    bin_table['score']=s
    return bin_table


def get_score_var(modeling,coarse_class_table):
    import pandas as pd
    f=coarse_class_table.feature[0]
    x=modeling[f]
    s=pd.Series([0]*len(x));s.name='s_'+f
    for i in range(len(coarse_class_table)):
        lgk_rm=[s1==0 for s1 in s]
        if coarse_class_table.isnormal[i]=='abnormal':
            lgk=((x==coarse_class_table.min_bin[i])&lgk_rm)
        elif (coarse_class_table.min_bin[i]=='min') & (coarse_class_table.max_bin[i]=='max'):
            lgk=(([x1 not in list(coarse_class_table['min_bin'][coarse_class_table['isnormal']=='abnormal']) for x1 in x]) and lgk_rm)         
        elif coarse_class_table.min_bin[i]=='min':
            lgk=((x<=coarse_class_table.max_bin[i])&lgk_rm)
        elif coarse_class_table.max_bin[i]=='max':
            lgk=((x>coarse_class_table.min_bin[i])&lgk_rm)
        else:
            lgk=((x<=coarse_class_table.max_bin[i])&(x>coarse_class_table.min_bin[i])&lgk_rm)
        s[lgk]=coarse_class_table.score[i]
    return s
