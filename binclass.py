# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:25:55 2018

@author: longding
"""
'''
功能介绍：
get_bin_table      |
get_Fine_Classing  |
'''
def get_bin_table(data,f,special_value=[],group=10,EquiDistant=False,dist=5,value_type='数值型'):
    '''
    功能：计算数据集某个特征的分组,提供等距分组&等量分组(默认)
    逻辑：1.所有特殊值全部单独列出，不根据单个数据集
         2.
    输入：数据集，特征，特殊值
    输出：特征+类型+中文+水平数+00-100
    for 数值型变量（整数或小数）
    1  a b x<=b
    2  b c b<x<=c
    .. d e d<x
    '''
    from scipy import stats
    import numpy as np
    import pandas as pd    
    feature=[];group_id=[];group_flag=[];isnormal=[];min_bin=[];max_bin=[];group_i=0
    #特殊值(非数值取成特殊值，并排序)
    for value in special_value:
        group_i=group_i=1;feature.append(f);group_id.append(group_i);
        group_flag.append(value);isnormal.append('ABN.');min_bin.append(value);max_bin.append(value);
    #数值
    if value_type=='数值型':
        normal_x=[x for x in data[f] if x not in special_value]
        n_levels=len(set(normal_x));
        if n_levels==0:
            nor_group=0;nor_min_bin=[];nor_max_bin=[]
        elif n_levels>group:
            if EquiDistant==False:
                pre_pct=[stats.scoreatpercentile(normal_x, i* 100.0/group,interpolation_method='lower') for i in range(group+1)]
            else:
                pre_pct=list(range(min(normal_x),max(normal_x),dist))
            #分位数去重
            if pre_pct[0]==pre_pct[int(group/10)]:#为了预防最小值太多忽略的情况
                pct=[pre_pct[0]]+list(np.sort([i for i in set(pre_pct)]))
            else:
                pct=list(np.sort([i for i in set(pre_pct)]))
            nor_group=len(pct)-1
            nor_min_bin=['min']+pct[1:nor_group];nor_max_bin=pct[1:nor_group]+['max']
        else:
            pct=list(np.sort([i for i in set(normal_x)]))
            nor_group=len(pct)
            nor_min_bin=['min']+pct[0:n_levels-1];nor_max_bin=pct[0:n_levels-1]+['max']
        te=[];
        for i in range(nor_group):
                te.append('('+str(nor_min_bin[i])+','+str(nor_max_bin[i])+']')
    else:
        nor_min_bin=[];nor_max_bin=[];nor_group=0;te=[]
    #汇总
    min_bin=special_value+nor_min_bin;max_bin=special_value+nor_max_bin;
    isnormal=['abnormal']*len(special_value)+['normal']*nor_group
    group_id=range(1,nor_group+len(special_value)+1)
    #输出
    bin_table=pd.DataFrame()
    bin_table['feature']    =[f]*(nor_group+len(special_value))
    bin_table['group_id']   =group_id
    bin_table['group_flag'] =special_value+te
    bin_table['isnormal']   =isnormal
    bin_table['min_bin']    =min_bin
    bin_table['max_bin']    =max_bin
    return bin_table

def get_Fine_Classing(data,bin_table,bad_var,good_var,is_mean_value=False):
    '''
    功能：计算数据集某个特征的分组ClassTable
    逻辑： 
    输入：数据集，bin_table,是否计算均值
    输出：特征的iv/ks,FineClassTable
    '''
    import copy
    import math
    f=bin_table['feature'][0];
    fy=data[[f,bad_var,good_var]]
    special_value=list(bin_table['max_bin'][bin_table['isnormal']=='abnormal'])
    all_total,event_total,non_event_total =sum(data[bad_var])+sum(data[good_var]),sum(data[bad_var]),sum(data[good_var])
    iv = 0;
    total=[];bad=[];good=[];
    total_pct=[];bad_pct=[];good_pct=[];
    cum_total=[];cum_bad=[];cum_good=[];
    bad_rate=[];woe=[];pre_ks=[];cum_br=[]
    mean_value=[];logodds=[];pre_iv=[];
    for gi in range(len(bin_table)):
        if bin_table.isnormal[gi]=='abnormal':
            g_fy=fy[fy[f]==bin_table.max_bin[gi]]
        else:
            n_fy=fy[[xi not in special_value for xi in fy[f]]];
            if bin_table.min_bin[gi]=='min' and bin_table.max_bin[gi]!='max':
                g_fy=n_fy[n_fy[f]<=bin_table.max_bin[gi]]
            elif bin_table.max_bin[gi]=='max' and bin_table.min_bin[gi]!='min':
                g_fy=n_fy[n_fy[f]>bin_table.min_bin[gi]]
            elif  bin_table.max_bin[gi]=='max' and bin_table.min_bin[gi]=='min':
                g_fy=fy[fy[f]>-1]
            else:
                g_fy=n_fy[(n_fy[f]>bin_table.min_bin[gi])&(n_fy[f]<=bin_table.max_bin[gi])]
        all_count,event_count,non_event_count =sum(g_fy[bad_var])+sum(g_fy[good_var]),sum(g_fy[bad_var]),sum(g_fy[good_var])
        total.append(all_count);bad.append(event_count);good.append(non_event_count);
        total_pct.append(1.0*all_count/all_total);
        bad_pct.append(1.0 * event_count / event_total);
        good_pct.append(1.0 * non_event_count / non_event_total);
        cum_total.append(sum(total_pct));cum_bad.append(sum(bad_pct));cum_good.append(sum(good_pct));
        pre_ks.append(abs(sum(bad_pct)-sum(good_pct)))
        if len(g_fy)==0 or sum(g_fy[bad_var])==0 or sum(g_fy[good_var])==0:
            cum_br.append(0)
            bad_rate.append(0)
            logodds.append(0)
            pre_iv.append(0)       
            woe.append(0);
            if is_mean_value==True:
                mean_value.append(0)
        else:
            cum_br.append(sum(bad)/sum(total))
            bad_rate.append(event_count/all_count)
            logodds.append(round(math.log(non_event_count/event_count),4))
            woe1 = round(math.log((1.0 * event_count / event_total)/(1.0 * non_event_count / non_event_total)),4)
            pre_iv.append((((1.0 * event_count / event_total)-(1.0 * non_event_count / non_event_total))*woe1))
            woe.append(woe1);
            if is_mean_value==True:
                mean_value.append(sum(g_fy[f])/len(g_fy))
    iv=sum(pre_iv);ks=max(pre_ks)
    #table out
    fine_class_table=copy.deepcopy(bin_table)
    cols=['total','bad','good','bad_rate','ks','log_odds','total_pct','bad_pct','good_pct','cum_total','cum_bad','cum_good','cum_br','woe','pre_iv']      
    data_list=[total,bad,good,bad_rate,pre_ks,logodds,total_pct,bad_pct,good_pct,cum_total,cum_bad,cum_good,cum_br,woe,pre_iv]
    if is_mean_value==True:
        cols.insert(0,'mean');data_list.insert(0,mean_value);
    for i in range(len(cols)):
        fine_class_table[cols[i]]=data_list[i]
    return fine_class_table,iv,ks


#%%
def get_coarse_flag(coarse_class_table,br_dis=0.01,pct_dis=0.03):
    '''
    功能：依据某一原则得到新的分组合并标签
    '''
    ci=0;coarse_flag=[]
    for tp in coarse_class_table['group_id'][coarse_class_table['isnormal']=='abnormal']:
        ci=ci+1;coarse_flag.append(ci);
    class_table=coarse_class_table[coarse_class_table['isnormal']=='normal'];class_table.index=range(len(class_table))
    dis=[abs(class_table['bad_rate'][i]-class_table['bad_rate'][i-1]) for i in range(1,len(class_table))] 
    if len(dis)>1 and ((min(dis)<br_dis) or (min(class_table['total_pct'])<pct_dis)):
        if min(dis)<br_dis:
            ci=ci+1;coarse_flag.append(ci);
            for x in dis:
                if x>min(dis):     ci=ci+1;coarse_flag.append(ci);
                else:              coarse_flag.append(ci)
        elif min(class_table['total_pct'])<pct_dis:
            for i in range(len(class_table)):
                if i==1 and class_table['total_pct'][0]==min(class_table['total_pct']):
                    coarse_flag.append(ci);
                elif i!=0 and class_table['total_pct'][i]==min(class_table['total_pct']):
                    coarse_flag.append(ci);
                else:  
                    ci=ci+1;coarse_flag.append(ci);
    else:
        for tp in coarse_class_table['group_id'][coarse_class_table['isnormal']=='normal']:
            ci=ci+1;coarse_flag.append(ci);
    return coarse_flag

def get_new_bin(coarse_class_table,coarse_flag):
    '''
    功能：根据新的标签，重新合并得到新的bin_table
    '''
    import pandas as pd;
    feature=[];group_id=[];group_flag=[];
    isnormal=[];min_bin=[];max_bin=[]
    for i in list(set(coarse_flag)):
        bini=coarse_class_table[[x==i  for x in coarse_flag]]
        feature.append(bini['feature'].values[0]);
        group_flag.append('('+str(bini['min_bin'].values[0])+','+str(bini['max_bin'].values[len(bini)-1])+']');
        group_id.append(i)
        isnormal.append(bini['isnormal'].values[0]);
        min_bin.append(bini['min_bin'].values[0]);
        max_bin.append(bini['max_bin'].values[len(bini)-1]);
    new_bin_table=pd.DataFrame()
    cols=['feature', 'group_id', 'group_flag', 'isnormal', 'min_bin', 'max_bin']
    data_list=[feature,group_id,group_flag,isnormal,min_bin,max_bin]
    for i in range(len(cols)):
        new_bin_table[cols[i]]=data_list[i]
    return new_bin_table

        
def get_a_Coarse(modeling,fine_class_table):
    coarse_flag=get_coarse_flag(fine_class_table,br_dis=0.01,pct_dis=0.03);
    new_bin_table=get_new_bin(fine_class_table,coarse_flag)
    return new_bin_table

def get_coarse_index(fine_class_table):
    class_table=fine_class_table[fine_class_table['isnormal']=='normal'];class_table.index=range(len(class_table))
    if len(class_table)==1:
         min_dis=0
         min_pct=0
    else:
         min_dis=min([abs(class_table['bad_rate'][i]-class_table['bad_rate'][i-1]) for i in range(1,len(class_table))])
         min_pct=min(class_table['total_pct'])
    return min_dis,min_pct
#%%
def get_Coarse_Classing(modeling,fine_class_table,bad_var,good_var,coarse_flag=[],n_try=20,br_auto=False,br_dis=0.01,pct_dis=0.03,auto_coarse=True):
    if auto_coarse==True:
        import sys
        if br_auto==True:
            br_dis=round(sum(modeling[bad_var])/(sum(modeling[bad_var])+sum(modeling[good_var]))/8,2)
        min_dis,min_pct=get_coarse_index(fine_class_table)
        i=1;coarse_class_table=fine_class_table;n_b=1;n_a=0;
        iv=sum(fine_class_table['pre_iv']);ks=max(fine_class_table['ks'])
        while n_b>n_a and i<=n_try and ((min_dis<br_dis) or (min_pct<pct_dis)):
            sys.stdout.write('\rFeature:'+fine_class_table['feature'][0]+''*(30-len(fine_class_table['feature'][0]))+'  Trying '+str(i)+' '*(len(str(i)))+' Times')
            sys.stdout.flush()
            coarse_flag=get_coarse_flag(coarse_class_table,br_dis,pct_dis);
            n_b=len(coarse_class_table)
            new_bin_table=get_new_bin(coarse_class_table,coarse_flag)
            n_a=len(new_bin_table)
            coarse_class_table,iv,ks=get_Fine_Classing(modeling,new_bin_table,bad_var,good_var,is_mean_value=False)
            min_dis,min_pct=get_coarse_index(coarse_class_table)
            i=i+1
    else:
        coarse_class_table=fine_class_table
        n_b=len(coarse_class_table)
        new_bin_table=get_new_bin(coarse_class_table,coarse_flag)
        n_a=len(new_bin_table)
        coarse_class_table,iv,ks=get_Fine_Classing(modeling,new_bin_table,bad_var,good_var,is_mean_value=False)

    return coarse_class_table,iv,ks
    
    
