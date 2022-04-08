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

"""
Partie du code sur les fichier du manipulandum(.glm)

"""
def allSujet(colname,Nbloc):
    
    df = pd.DataFrame(columns =  ['time','S1','S2','S3','S5','S6'])
    
    for Nsuj in [1,2,3,5,6]: #1,2,3,5,6
    
        strpath = "S"+str(Nsuj)+"_0"

        if Nbloc<10:
            pathg="GLM/"+strpath+"0"+str(Nbloc)+".txt"
        else:
            pathg="GLM/"+strpath+str(Nbloc)+".txt"
            
        df_glm = pd.read_csv(pathg, 
                         sep = ',', 
                         header = 0
                         )         
        
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
        else:
            pathg="GLM/"+strpath+str(Nbloc)+".txt"
            
        df_glm = pd.read_csv(pathg, 
                         sep = ',', 
                         header = 0
                         )         
        
        bs = 'B'+str(Nbloc)
        df[bs] = df_glm[colname]
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
    plt.plot(time,meanup,label = 'mean up',color = 'red')
    plt.plot(time,meandown,label = 'mean down',color = 'green')
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
    meanupd = np.mean(dataupd,1)
    meandownd= np.mean(datadownd,1)
    meanupg = np.mean(dataupg,1)
    meandowng= np.mean(datadowng,1)
    plt.plot(time,meanupd,label = 'mean up right',color = 'red')
    plt.plot(time,meandownd,label = 'mean down right',color = 'green')
    plt.plot(time,meanupg,label = 'mean up left',color = 'orange')
    plt.plot(time,meandowng,label = 'mean down left',color = 'blue')
    plt.show()    

def averageMain(dfs):
    time = dfs['time']
    df= dfs.drop(columns = ['time'])
    data = df.values
    dataup = data[:,:6]
    datadown = data[:,7:]
    meanup= np.mean(dataup,1)
    meandown= np.mean(datadown,1)
    plt.plot(time,meanup,label = 'mean up',color = 'red')
    plt.plot(time,meandown,label = 'mean down',color = 'green')
    plt.show()         
        
numcoord =[10,11,12,13,14,15]
numforce =[i for i in range(1,7)]
marker_manipulandum = [4,5,6,7]


Nsuj = 1



df_GF = allFor1Sujet(('LFt'),Nsuj)
#averageSensMain(df_GF)
#pl.plot_Gf1(df_GF,Nsuj)




def sujBySuj():
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
            pl.expo(mc,df_glm)
            #print(df_coda['Marker7_X'])
            #pl.plot_Gf(df_glm,path1,k)
            #pl.graphe_position(mc,df_coda.timec,path,k)
            #pl.LFGF(df_glm,path1,k)
            #crd.coordination(df_glm,df_coda,mc,k,path)
            #print(i)
            
            
sujBySuj()   