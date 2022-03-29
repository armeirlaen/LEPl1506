import os
import coda_toolbox as coda
import friction_toolbox as fri
import glm_toolbox as glm
import signal_processing_toolbox as sig
import Plot as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



path = "Groupe 1_CODA/"
filenames = os.listdir(path)
File = 14

marker_manipulandum = [4,5,6,7] #les markers utilisés sur le manipulandum

strpath = "GBIO_2022_Group_1_S1_20220008_0"
strpath1= "Bloc_S1_0"
num = [11]

for i in num:
    if i<10:
        path="Groupe 1/"+strpath1+"0"+str(i)+".glm"
    else:
        path="Groupe 1/"+strpath1+str(i)+".glm"
    curr_df = glm.import_data(path)

def find_end(timec,timem,ac,am):
    maxc = np.max(ac)
    idxc = np.where(ac == maxc)
    maxm = np.max(am)
    idxm = np.where(am == maxm)
    #print(idxc,maxc,idxm,maxm)
    endc = float(timec[idxc[0]])
    endm = float(timem[idxm[0]])
    
    delta = round(endc - endm,6)
    print(len(timem))
    print(timem)
    add = np.where(timem == delta)
    zero = np.zeros(add[0])
    newam = np.concatenate((zero,am))
    newtimem = np.linspace(0,timem[len(timem)-1]+delta,num=len(newam))
    
    
    
    return(timec,newtimem,ac,newam)

def supprNan(time,mc):
    i = 0
    start = True
    suppr = []
    while i < len(mc):
        #print(mc[0])
        while np.isnan(mc[i]) & start:
            suppr.append(i)
            i+=1
        start = False
        if np.isnan(mc[i]):
            mc[i] = mc[i-1]
        i+=1
   
    newmc = np.delete(mc,suppr)
    newtime = time.drop(suppr)
    return(newtime,newmc)

df = coda.import_data('Groupe 1_CODA/' + filenames[File-1])  #on import les données
mc = coda.manipulandum_center(df, markers_id = marker_manipulandum ) #on calcule les coordonnées du centre du manipulandum
timec = df.time
FS_coda =200
FS_glm = 800

def plot_acc(glm,mc,timec):
    
    Pcoda = sig.filter_signal(mc[1])
    dx = timec[1]-timec[0]
    timem = glm.time
    ax = sig.filter_signal(glm['LowAcc_X'])
    ay = glm['LowAcc_Y']
    az = glm['LowAcc_Z']
    dy= np.zeros(len(Pcoda))
    ddy = np.zeros(len(Pcoda))
    
    
    Acoda = -sig.derive(sig.derive(Pcoda,FS_coda),FS_coda)/10000
    
    timec,ac = supprNan(timec,Acoda)
    timem,am = supprNan(timem,ax)
    
    timec,timem,ac,am = find_end(timec,timem,ac,am)    
    
    """
    plt.subplot(3,1,1)
    plt.plot(timeg,ax,color = 'green')
    plt.subplot(3,1,2)
    plt.plot(timec,dy)
    plt.subplot(3,1,3)
    plt.plot(timec,ddy)
    """
    
    plt.plot(timem,am,color = 'green')
    plt.plot(timec,ac)
    
    
    
    #plt.plot(time,ay,color = 'red')
    #plt.plot(time,az)
    plt.show()
    
plot_acc(curr_df,mc,timec)
