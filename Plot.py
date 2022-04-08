import matplotlib.pyplot as plt

import numpy as np
import signal_processing_toolbox as sig
import Coordination as crd
from scipy.optimize import curve_fit

def graphe_position(mc,time,file,k):
    
    time = np.linspace(0,52,len(mc[0]))
    
    plt.subplot(6,1,k)
    plt.title(file)
    plt.plot(time,mc[0])
    plt.plot(time,mc[1])
    plt.plot(time,mc[2])
    
    #plt.legend('-',['X','Y','Z'])
    
    if k == 6:
        plt.show()
    
def graphe_pos_3D(mc):
    
    fig = plt.figure(figsize=(4,4))
    
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(mc[0],mc[1],mc[2])
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    plt.show()
    
def only_y(mc,time,idx):
    #while i < len(mc):
        #mean = np.full(len(centers[i]),-500)
        
    #plt.subplot(len(mc),1,i+1)
    plt.plot(time,mc)
   
    
    plt.legend(['-',str(float(time[idx]))])
    #i+=1
    plt.show()
    

def plot_Gf(df,path,k):
    
    plt.subplot(6,1,k)
    time = df['time']
    GF = df['GF']
    plt.plot(time,GF,label = 'GF')
    m = np.full(len(time),np.mean(GF))
    plt.plot(time,m,label = str(m[0]))
    #plt.plot(t,mean)
        
        
    plt.title(path)
    plt.legend(loc = 'upper right')
    plt.show()
    
def plot_Gf1(df,Nsuj):
    time = df['time']
    
    for i in range(1,2):
        GF = df['B'+str(i)]
        if i <7:
            plt.plot(time,GF,label = 'B'+str(i),alpha=0.25,color = 'red')
        else :
            plt.plot(time,GF,label = 'B'+str(i),alpha=0.25,color = 'green')
        
    #plt.plot(t,mean)
    plt.title('GF sujet'+str(Nsuj))
    plt.legend(loc = 'upper right')
    plt.show()     
    
def LFGF(df,path,k):
    time = df['time']
    GF = df['GF']        
    LF = df['LFt']
    plt.subplot(6,1,k)
    plt.title(path)
    plt.plot(time,GF,label = 'GF')
    plt.plot(time,LF,label = 'LF') 
    plt.legend()
    plt.show()

def func(x, a, b, c): # simple quadratic example
    return a*x**2 + b*x + c

def expo(mc,df):
    time = df['time']
    
    nGF = df['GF'] #Filter and derive x
    #plt.plot(mc[1])
    Vcoda = sig.derive(mc[1],200)
    crd.supprNan(Vcoda)
    #plt.plot(Vcoda)
    idxmax,idxmin,bloc = crd.find_mouv(Vcoda) #Get blocs
    plt.figure(1)
    
    centering = len(nGF)/len(Vcoda)
    mean = (np.zeros(10))
    xmean = (np.zeros(10))
    k=-1
    for j in range(0,20,2): #Take mean GF of blocs
        k=k+1
        for x in range(int(bloc[j]),int(bloc[j+1])):
            mean[k] = mean[k] + nGF[int(x*centering)]
        mean[k] = mean[k]/(bloc[j+1]-bloc[j])
        xmean[k] = time[int((bloc[j+1]*centering+bloc[j]*centering)/2)]
        plt.scatter(xmean[k],mean[k])
    
    popt, pcov = curve_fit(func,xmean,mean)
    tiltles = str(popt[0])+" * x**2 "+str(popt[1])+" * x + "+str(popt[2])
    plt.plot(xmean, func(xmean, *popt), label=tiltles)
    plt.title(tiltles)
    print(bloc)
    plt.plot(time,nGF,label = 'GF',alpha=0.25,color = 'red')
    plt.show()
    
    plt.figure(2)
    nxaxis = (np.zeros(10))
    for i in range(10):
        nxaxis[i] = i
    popt, pcov = curve_fit(func,nxaxis,mean)
    plt.scatter(nxaxis,mean)
    plt.plot(nxaxis, func(nxaxis, *popt))
    #plt.show()
    return pcov[0]