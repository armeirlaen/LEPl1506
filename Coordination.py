import os
import coda_toolbox as coda
import friction_toolbox as fri
import glm_toolbox as glm
import signal_processing_toolbox as sig
import Plot as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


FS_coda =200
FS_glm = 800
def find_end(timec,timem,ac,am):
    
    maxc = np.max(ac)
    idxc = np.where(ac == maxc)
    
    maxm = np.max(am[30000:])
    idxm = np.where(am[30000:] == maxm)
    #print(idxc,maxc,idxm,maxm)
    if len(idxc[0]) == 1:
        endc = float(timec[idxc[0]])
        endm = float(timem[idxm[0]+30000])
    else :
        endc = float(timec[idxc[0][0]])
        endm = float(timem[idxm[0]+30000])
    
    delta = round(endc - endm,6) #besoin de rajouter -0,001 pour S5 car jsp pq time commence pas a 0
    #print(endc,endm)
    if delta > 0:
        add = np.where(timem == delta)
        zero = np.zeros(add[0])
        newam = np.concatenate((zero,am))
        newtimem = np.linspace(0,timem[len(timem)-1]+delta,num=len(newam))
    else :
        suppr = np.where(timem == abs(delta))
        list_suppr = np.arange(0,suppr[0])
        newam = np.delete(am,list_suppr)
        newtimem = np.linspace(0,timem[len(timem)-1]+delta,num=len(newam))
    
        #newtimec = np.linspace(0,(timec[0]-timec[-1]),len(timec))
    return(timec,newtimem,ac,newam)

def supprNan(mc):
    i = 0
    
    if np.isnan(mc[i]):
            mc[i] = 0
            i+=1
    while i < len(mc):
        #print(mc[0])
        if np.isnan(mc[i]):
            mc[i] = mc[i-1]
        i+=1
   
    #newmc = np.delete(mc,suppr)
    #newtime = time.drop(suppr)
    #return(newtime,newmc)



def plot_acc(glm,mc,timec,k,path):
    
    Pcoda = sig.filter_signal(mc[1])
    timem = glm.time
    am = sig.filter_signal(glm['LowAcc_X'])
    #ay = glm['LowAcc_Y']
    #az = glm['LowAcc_Z']
    
    if k in range(1,7):
        ac = -1*sig.derive(sig.derive(Pcoda,FS_coda),FS_coda)/10000 # -1 si mani a l'envers Pour S1 à l'endroit
    else :
        ac = 1*sig.derive(sig.derive(Pcoda,FS_coda),FS_coda)/10000
        
    #POUR S5 1->6
    #plt.subplot(6,1,k)
    #plt.plot(timem,am,color = 'red')
    #plt.plot(timec,ac)
    
    supprNan(ac)
    supprNan(am)
    
    timec,timem,ac,am = find_end(timec,timem,ac,am)    
    
    """
    plt.subplot(3,1,1)
    plt.plot(timeg,ax,color = 'green')
    plt.subplot(3,1,2)
    plt.plot(timec,dy)
    plt.subplot(3,1,3)
    plt.plot(timec,ddy)
    """
    plt.subplot(6,1,k)
    plt.plot(timem,am,color = 'green')
    plt.plot(timec,ac)
    
    
    
    
   
    if k == 6 :
        plt.title(path)
        plt.legend(['Manipulandum','CODA'],loc = 'upper left')
        plt.show()
        
    
    
def coordination(df_glm,df_coda,mc,k,path):
    timec = df_coda.timec
    plot_acc(df_glm,mc,timec,k,path)