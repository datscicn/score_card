# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:14:45 2018

@author: longding
"""
'''
功能介绍：
feature_stat       |特征统计，水平数+分位数等
get_Fine_Classing  |
'''
def feature_stat(data,variables):
    '''
    功能：计算数据集内所有特征的统计值
    逻辑：
    输入：数据集，特征集
    输出：特征+类型+中文+水平数+00-100
    '''
    from scipy import stats
    import pandas as pd
    import numpy as np
    import sys
    n_level=[];
    pcts=[];pcts11=[]
    for f_i in range(len(variables)):
        f=variables['features'][f_i]
        sys.stdout.write('\rFeature '+f+''*(30-len(f))+' is Caculating No.'+str(f_i+1))
        sys.stdout.flush()
        n_level.append(len(set(data[f])))
        if variables['value_type'][f_i]=='数值型':
            pcts.append([stats.scoreatpercentile(data[f], i* 100.0/10) for i in range(11)])
        else:
            pcts.append(['']*11)
    for i in range(11):
        pcts11.append([pcts[vi][i] for vi in range(len(variables))])
    cols=['Feature','Value_type','Name','N_level','Min','Pct10','Pct20','Pct30','Pct40','Pct50','Pct60','Pct70','Pct80','Pct90','Max'];
    data_list=[variables['features'],variables['value_type'],variables['explain'],n_level]+pcts11
    feature_stat_result=pd.DataFrame()
    for i in range(len(cols)):
        feature_stat_result[cols[i]]=data_list[i] 
    return feature_stat_result


#
#
#for f in fs:
#    if (min(modeling[f])==-999)&(min(modeling[f][[(x!=-999) for x in modeling[f]]])<-1):
#        special_values.append([-999])
#    elif (min(modeling[f])==-999)&(min(modeling[f][[(x!=-999) for x in modeling[f]]])>=-1):
#        special_values.append([-999,-1])
#    elif (min(modeling[f][[(x!=-999) for x in modeling[f]]])<-1):
#        special_values.append([])
#    else:
#        special_values.append([-1])
#    print('Complete '+str(len(variables['feature']))+' --> '+str(i+1))
#    i=i+1