import os
import coda_toolbox as coda
import friction_toolbox as fri
import glm_toolbox as glm
import signal_processing_toolbox as sig
import Plot as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema



FS_coda =200
FS_glm = 800



def find_max_loc(vc):
    threshold = np.max(vc)/7
    maxi = argrelextrema(vc, np.greater)
    keep = []
    #◘print(maxi)
    for i in maxi[0]:
        if vc[i] > threshold :
            keep.append(i)
            
    keep = np.array(keep)
    keep = keep[1:]
    
    j = 0
    while j < len(keep):
        while (keep[j] - keep[j-2] < 400) & (keep[j] - keep[j-2] >0) & (keep[j]!=0):
            keep = np.delete(keep,j)
            keep = np.append(keep,0)   
        if (j < len(keep)) & (keep[j]!=0):    
            
            max = vc[keep[j]]
            #print('max:',round(max/10,1))
            arr = vc[keep[j]-100:keep[j]]
            difference_array = np.absolute(arr-max/10)
            index = difference_array.argmin()
           
            #print(start)
            idx = index-100+keep[j]
            
            
            arr1 = vc[keep[j]:keep[j]+100]
            difference_array = np.absolute(arr1-max/10)
            index1 = difference_array.argmin()
        
            idx1 = index1+keep[j]
            keep[j] = idx
            keep = np.insert(keep,j+1,idx1)
        j+=2

    keep = keep[0:20] 
   
    return keep

def find_min_loc(vc):
    threshold = np.min(vc)/3
    maxi = argrelextrema(vc, np.less)
    keep = []
    #◘print(maxi)
    for i in maxi[0]:
        if vc[i] < threshold :
            keep.append(i)
            
    keep = np.array(keep)
    
    j = 0
    while j < len(keep):
        
        if (keep[j] - keep[j-2] < 400) & (keep[j] - keep[j-2] >0):
           
            keep = np.delete(keep,j)
            
        if j < len(keep):
            max = vc[keep[j]]
            #print('max:',round(max/10,1))
            arr = vc[keep[j]-75:keep[j]]
            difference_array = np.absolute(arr-max/10)
            index = difference_array.argmin()
            
            #print(start)
            idx = index-75+keep[j]
            
            arr1 = vc[keep[j]:keep[j]+75]
            difference_array = np.absolute(arr1-max/10)
            index1 = difference_array.argmin()
            idx1 = index1+keep[j]
            
            keep[j] = idx
            keep = np.insert(keep,j+1,idx1)
            
        j+=2
      
    keep = keep[0:20]
    return keep

def find_end(timec,timem,ac,am):
    
    maxc = np.max(ac)
    idxc = np.where(ac == maxc)
    
    maxm = np.max(am[30000:])
    idxm = np.where(am[30000:] == maxm)
    print(idxc,maxc,idxm,maxm)
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
    Vcoda = sig.derive(Pcoda,FS_coda)
    if k in range(1,7):
        ac = 1*sig.derive(Vcoda,FS_coda)/10000 # -1 si mani a l'envers Pour S1 à l'endroit
    else :
        ac = 1*sig.derive(Vcoda,FS_coda)/10000
        
    #POUR S5 1->6
    #plt.subplot(6,1,k)
    #plt.plot(timem,am,color = 'red')
    #plt.plot(timec,ac)
    
    supprNan(ac)
    supprNan(am)
    
    timec,timem,ac,am = find_end(timec,timem,ac,am)
    supprNan(Vcoda)
    idxmax,idxmin,bloc = find_mouv(Vcoda) 
    
    """
    plt.subplot(3,1,1)
    plt.plot(timeg,ax,color = 'green')
    plt.subplot(3,1,2)
    plt.plot(timec,dy)
    plt.subplot(3,1,3)
    plt.plot(timec,ddy)
    """
    plt.subplot(6,1,k)
    #plt.plot(timec,ac,color = 'green')
    #plt.plot(timem,am)
    plt.plot(timec,Vcoda)
    plt.scatter(timec[idxmax],Vcoda[idxmax],color = 'red')
    plt.scatter(timec[idxmin],Vcoda[idxmin],color = 'green') 
    
    
    
   
    if k == 6 :
        plt.title(path)
        plt.legend(['Manipulandum','CODA'],loc = 'upper left')
        plt.show()
        
def find_mouv(Vcoda):
    idxmax = find_max_loc(Vcoda)
    idxmin = find_min_loc(Vcoda)
    print(idxmin,idxmax)
    bloc = np.concatenate((idxmax,idxmin))

    k = 0
    l = 0
    i = 0
    """
    while i < len(bloc):
            bloc[i] = idxmax[k]
            bloc[i+1]=idxmax[k+1]
            k+=2
            bloc[i+2] = idxmin[l]
            bloc[i+3]=  idxmin[l+1]
            l+=2
            
            i+=4
            
    """        
    #plt.scatter(timec[idxmax],Vcoda[idxmax],color = 'red')
    #plt.scatter(timec[idxmin],Vcoda[idxmin],color = 'green') 
    #print(bloc)
    return(idxmax,idxmin,bloc)
    
def coordination(df_glm,df_coda,mc,k,path):
    timec = df_coda.timec
    plot_acc(df_glm,mc,timec,k,path)