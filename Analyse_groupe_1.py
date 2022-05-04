# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 19:05:12 2022

@author: romai
"""
import os
import coda_toolbox as coda
import friction_toolbox as fri
import glm_toolbox as glm
import signal_processing_toolbox as sig
import Plot as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Coordination as crd
import statsmodels.formula.api
import statsmodels.api

"""
Partie du code sur les fichier du manipulandum(.glm)

"""
def allSujet(colname,Nbloc):
    
    df = pd.DataFrame(columns =  ['time','S1','S2','S3','S5','S6'])
    
    for Nsuj in [1,2,3,5,6]: #1,2,3,5,6
    
        strpath = "S"+str(Nsuj)+"_0"

        if Nbloc<10:
                pathg="GLM/"+strpath+"0"+str(Nbloc)+".txt"
                pathc = "Coda/"+strpath+"0"+str(Nbloc)+".txt"
        else:
            pathg="GLM/"+strpath+str(Nbloc)+".txt"
            pathc = "Coda/"+strpath+str(Nbloc)+".txt"
            
        df_glm = pd.read_csv(pathg, 
                         sep = ',', 
                         header = 0
                         )         
        df_coda = pd.read_csv(pathc,sep = ',',header = 0)
        ns = 'S'+str(Nsuj)
        df[ns] = df_glm[colname]
    df['time'] = df_glm['time']        
    return df        

def allFor1Sujet(colname,Nsuj):
    
    df = pd.DataFrame(columns =  ['time','B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12'])
    
    for Nbloc in range(1,13): #1,2,3,5,6
    
        strpath = "S"+str(Nsuj)+"_0"

        if Nbloc<10:
                pathg="GLM/"+strpath+"0"+str(Nbloc)+".txt"
                pathc = "Coda/"+strpath+"0"+str(Nbloc)+".txt"
        else:
            pathg="GLM/"+strpath+str(Nbloc)+".txt"
            pathc = "Coda/"+strpath+str(Nbloc)+".txt"
            
        df_glm = pd.read_csv(pathg, 
                         sep = ',', 
                         header = 0
                         )
        
        df_coda = pd.read_csv(pathc,sep = ',',header = 0)
        manc = coda.manipulandum_center(df_coda, markers_id = marker_manipulandum )
        mc = np.empty_like(manc)
        for j in range(3):
            mc[j] = sig.filter_signal(manc[j])
        idx1,idx2 = crd.cut(df_glm,df_coda,mc)
        
        bs = 'B'+str(Nbloc)
        df[bs] = df_glm[colname][idx1:idx2]
        
    df['time'] = df_glm['time']
    return df                        

def average(dfs):
    time = dfs['time']
    df = dfs.drop(columns = ['time'])
    data = df.values
    mean= np.mean(data,1)
    
    plt.plot(time,mean,label = 'mean',color = 'blue')
    plt.show()
        
def averageSens(dfs):
    time = dfs['time']
    df= dfs.drop(columns = ['time'])
    data = df.values
    dataup = data[:,:6]
    datadown = data[:,7:]
    meanup= np.mean(dataup,1)
    meandown= np.mean(datadown,1)
    ax1 = plt.subplot(1,2,1)
    plt.plot(time,meanup,label = 'mean up',color = 'red')
    plt.plot(time,dataup,color = 'red',alpha = 0.25)
    plt.title('Average upside')
    plt.subplot(1,2,2,sharey = ax1)
    plt.plot(time,meandown,label = 'mean down',color = 'green')
    plt.plot(time,datadown,color = 'green',alpha = 0.25)
    plt.title('Average downside')
    plt.show()            

def averageSensMain(dfs):
    time = dfs['time']
    df= dfs.drop(columns = ['time'])
    data = df.values
    
    dataup = data[:,:6]
    datadown = data[:,6:]
    dataupd = dataup[:,[1,3,5]]
    dataupg = dataup[:,[0,2,4]]
    datadownd = datadown[:,[1,3,5]]
    datadowng = datadown[:,[0,2,4]]
    meanupd = np.nanmean(dataupd,1)
    meandownd= np.nanmean(datadownd,1)
    meanupg = np.nanmean(dataupg,1)
    meandowng= np.nanmean(datadowng,1)
    
    mupd1 = np.nanmean(dataup[:,1])
    mupd2 = np.nanmean(dataup[:,3])
    mupd3 = np.nanmean(dataup[:,5])

    mupg1 = np.nanmean(dataup[:,0])
    mupg2 = np.nanmean(dataup[:,2])
    mupg3 = np.nanmean(dataup[:,4])
    
    mdwd1 = np.nanmean(datadown[:,1])
    mdwd2 = np.nanmean(datadown[:,3])
    mdwd3 = np.nanmean(datadown[:,5])
    
    mdwg1 = np.nanmean(datadown[:,0])
    mdwg2 = np.nanmean(datadown[:,2])
    mdwg3 = np.nanmean(datadown[:,4])
    """#
    result = np.array([mupd1,mupd2,mupd3,
                       mupg1,mupg2,mupg3,
                       mdwd1,mdwd2,mdwd3,
                       mdwg1,mdwg2,mdwg3])
    
    means = np.array([meanupd,meandownd,meanupg,meandowng])
    #plotAverageSensMain(result,time,means)
    return(result,time,means)

def plotAverageSensMain(result,time,means):
    mupd1 = result[0]
    mupd2 = result[1]
    mupd3 = result[2]
    mupg1 = result[3]
    mupg2 = result[4]
    mupg3 = result[5]
    mdwd1 = result[6]
    mdwd2 = result[7]
    mdwd3 = result[8]
    mdwg1 = result[9] 
    mdwg2 = result[10]
    mdwg3 = result[11]
    meanupd = means[0]
    meandownd = means[1]
    meanupg = means[2]
    meandowng = means[3]
    """#
   
    ax1 = plt.subplot(2,2,1)
    plt.plot(time,meanupg,label = 'mean upside non-dominant hand',color = 'orange')
    plt.plot(time,dataupg,color = 'orange',alpha = 0.25)
    plt.plot(time,np.full(time.shape,mupg1),color = 'red',alpha = 0.50,label = 'mean of bloc 1 ='+str(round(mupg1,3)))
    plt.plot(time,np.full(time.shape,mupg2),color = 'blue',alpha = 0.50,label = 'mean of bloc 2 ='+str(round(mupg2,3)))
    plt.plot(time,np.full(time.shape,mupg3),color = 'green',alpha = 0.50,label = 'mean of bloc 3 ='+str(round(mupg3,3)))
    plt.xlabel('Time')
    plt.ylabel('LF')
    plt.legend()
    plt.title('Average upside non-dominant hand')
    
    plt.subplot(2,2,2,sharey = ax1)
    plt.plot(time,meanupd,label = 'mean upside dominant hand',color = 'red')
    plt.plot(time,dataupd,color = 'red',alpha = 0.25)
    plt.plot(time,np.full(time.shape,mupd1),color = 'red',alpha = 0.50,label = 'mean of bloc 1 ='+str(round(mupd1,3)))
    plt.plot(time,np.full(time.shape,mupd2),color = 'blue',alpha = 0.50,label = 'mean of bloc 2 ='+str(round(mupd2,3)))
    plt.plot(time,np.full(time.shape,mupd3),color = 'green',alpha = 0.50,label = 'mean of bloc 3 ='+str(round(mupd3,3)))
    plt.xlabel('Time')
    plt.ylabel('LF')
    plt.legend()
    plt.title('Average upside dominant hand')
    
    plt.subplot(2,2,3,sharey = ax1)
    plt.plot(time,meandowng,label = 'mean downside non-dominant hand',color = 'blue')
    plt.plot(time,datadowng,color = 'blue',alpha = 0.25)
    plt.plot(time,np.full(time.shape,mdwg1),color = 'red',alpha = 0.50,label = 'mean of bloc 1 ='+str(round(mdwg1,3)))
    plt.plot(time,np.full(time.shape,mdwg2),color = 'blue',alpha = 0.50,label = 'mean of bloc 2 ='+str(round(mdwg2,3)))
    plt.plot(time,np.full(time.shape,mdwg3),color = 'green',alpha = 0.50,label = 'mean of bloc 3 ='+str(round(mdwg3,3)))
    plt.xlabel('Time')
    plt.ylabel('LF')
    plt.legend()
    plt.title('Average downside non-dominant hand')
    
    
    plt.subplot(2,2,4,sharey = ax1)
    plt.plot(time,meandownd,label = 'mean downside dominant hand',color = 'green')
    plt.plot(time,datadownd,color = 'green',alpha = 0.25)
    plt.plot(time,np.full(time.shape,mdwd1),color = 'red',alpha = 0.50,label = 'mean of bloc 1 ='+str(round(mdwd1,3)))
    plt.plot(time,np.full(time.shape,mdwd2),color = 'blue',alpha = 0.50,label = 'mean of bloc 2 ='+str(round(mdwd2,3)))
    plt.plot(time,np.full(time.shape,mdwd3),color = 'green',alpha = 0.50,label = 'mean of bloc 3 ='+str(round(mdwd3,3)))
    plt.xlabel('Time')
    plt.ylabel('LF')
    plt.title('Average downside dominant hand')
    plt.legend()
    plt.show()

  

def averageMain(dfs):
    time = dfs['time']
    df= dfs.drop(columns = ['time'])
    data = df.values
    datad = data[:,[1,3,5]]
    datag = data[:,[0,2,4]]
    meand= np.mean(datad,1)
    meang= np.mean(datag,1)
    ax1 = plt.subplot(1,2,1)
    plt.plot(time,meang,label = 'mean up',color = 'red')
    plt.plot(time,datag,color = 'red',alpha = 0.25)
    plt.title('Average left hand')
    plt.subplot(1,2,2,sharey = ax1)
    plt.plot(time,meand,label = 'mean down',color = 'green')
    plt.plot(time,datad,color = 'green',alpha = 0.25)
    plt.title('Average right hand')
    plt.show()               
        
numcoord =[10,11,12,13,14,15]
numforce =[i for i in range(4,6)]
marker_manipulandum = [4,5,6,7]


Nsuj = 6



df_GF = allFor1Sujet(('LFt'),Nsuj)
averageSensMain(df_GF)
#pl.plot_Gf1(df_GF,Nsuj)



def sujBySuj():
    meanbloc = np.zeros(12)
    for Nsuj in [2]: #1,2,3,5,6
    
    
        strpath = "S"+str(Nsuj)+"_0" #"GBIO_2022_Group_1_S"+Nsuj+"_202200008_0" pourS1,S2,S3,S4
    
           
        num = numforce
    
        k=0
        for i in num:
            k+=1
            if i<10:
                path1="GLM/"+strpath+"0"+str(i)+".txt"
                path = "Coda/"+strpath+"0"+str(i)+".txt"
            else:
                path1="GLM/"+strpath+str(i)+".txt"
                path = "Coda/"+strpath+str(i)+".txt"
                
            df_coda = pd.read_csv(path, 
                             sep = ',', 
                             header = 0
                             )
            
            
            manc = coda.manipulandum_center(df_coda, markers_id = marker_manipulandum )
            mc = np.empty_like(manc)
            for j in range(3):
                mc[j] = sig.filter_signal(manc[j])
            
            df_glm = pd.read_csv(path1, 
                             sep = ',', 
                             header = 0
                             )
            #print(df_coda['Marker7_X'])
            #pl.plot_Gf(df_glm,path1,k)
            
            #pl.LFGF(df_glm,path1,k)
            #crd.coordination(df_glm,df_coda,mc,k,path)
            #print(i)
            #pl.graphe_position_2D(mc)
            
            
    """
        df_GF = allFor1Sujet(('GF'),Nsuj)
        result,time,means = averageSensMain(df_GF)
        
        for i in range (len(meanbloc)):
            if result[i] > 2 :
                meanbloc[i] += result[i]
            else :
                meanbloc[i] += result[i+1]
    meanbloc = meanbloc/5
    #plotAverageSensMain(meanbloc, time, means)  
    pl.plot_histogramme(meanbloc)
    """
   
    
#sujBySuj()   

def boxplot():
    meanbloc = np.zeros((6,12))
    for Nsuj in [1,2,3,5,6]:
        df_GF = allFor1Sujet(('LFt'),Nsuj)
        result,time,means = averageSensMain(df_GF)
        meanbloc[Nsuj-1] = result
    mean = np.delete(meanbloc,3,0)
    datagup = np.resize(mean[:,[0,1,2]],15)
    databup = np.resize(mean[:,[3,4,5]],15)
    datagdw = np.resize(mean[:,[6,7,8]],15)
    databdw = np.resize(mean[:,[9,10,11]],15)
    """
    for i in range(14):
        if datagup[i] < 2:
            datagup = np.delete(datagup, i)
        if databup[i] < 2:
            databup = np.delete(databup, i)
        if datagdw[i] < 2:
            atagdw= np.delete(datagdw, i)
        if databdw[i] < 2:
            databdw = np.delete(databdw, i)
    """
    data = [datagup,databup,datagdw,databdw]
    pl.plot_histogramme(data)
    return data
#boxplot()

def anova():
    datanp = boxplot()
    data = pd.DataFrame({'upg':datanp[0],'upb':datanp[1],'dwg':datanp[2],'dwb':datanp[3]})
    data1 = pd.DataFrame({'Up':np.concatenate((datanp[0],datanp[1])),'Down':np.concatenate((datanp[2],datanp[3]))})
    data2 = pd.DataFrame({'GH':np.concatenate((datanp[0],datanp[2])),'BH':np.concatenate((datanp[1],datanp[3]))})
    data3 = pd.DataFrame({'Dup': datanp[0]-datanp[1],'Ddw':datanp[2]-datanp[3]})
    fit = statsmodels.formula.api.ols('GH ~ BH ', data2).fit()
    table = statsmodels.api.stats.anova_lm(fit)
    print('Test anova H0 : [GF_ MD - GF_MnD]up = GF_MD -  GF_MnD]down \n',table)
#anova()

def anova2():
    datanp = np.resize(boxplot(),60)
    ori = np.zeros(20)
    main =  np.zeros(20)
    suj = np.zeros(20,dtype =int)
    dat = np.zeros(20,dtype =float)
    k = 1
    for i in range(20):
        suj[i] = k
        k+=1
        if k ==7:
            k = 1
        if k == 4:
            k+=1
        dat[i] = np.mean(datanp[3*i:3*i+2])
        
        if i < 5:
            ori[i] = 1
            main[i] = 1
        elif i < 10:
            ori[i] =  1
            main[i] = 0
        elif i < 15:
            ori[i] = 0
            main[i] = 1
        elif i < 20:
            ori[i] = 0
            main[i] = 0
    Tdata = np.array([suj,dat,ori,main])
    
    data = pd.DataFrame(np.transpose(Tdata),columns=['Suj_ID','GF','Orientation','Main'])
    #print(data)
    fit = statsmodels.stats.anova.AnovaRM(data,'GF','Suj_ID',within = ['Orientation','Main']).fit()
    print('Test Anova 2 way \n',fit)
#anova2()