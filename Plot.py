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
    return a*(x**2) + b*x +c

def expo(mc,df,df_coda,nb):
    time = df['time']
    
    nGF = df['GF'] #Filter and derive x
    Vcoda = sig.derive(mc[1],200)
    ac = 1*sig.derive(Vcoda,200)/10000
    
    am = sig.filter_signal(df['LowAcc_X'])
    
    crd.supprNan(ac)
    crd.supprNan(am)
    
    Vcoda = sig.derive(mc[1],200)
    crd.supprNan(Vcoda)
    idxmax,idxmin,bloc = crd.find_mouv(Vcoda) #Get blocs
    #plt.figure(1)
    
    timec,time,ac,am = crd.find_end(df_coda.timec,time,ac,am)

    time = df['time']
    centering = len(nGF)/len(Vcoda)
    mean = (np.zeros(10))
    xmean = (np.zeros(10))
    k=-1
    for j in range(0,20,2): #Take mean GF of blocs
        k=k+1
        if timec[bloc[j+1]]<51.5:
            ind1 = np.where(time == timec[bloc[j]])[0]
            ind2 = np.where(time == timec[bloc[j+1]])[0]
            if len(ind1)!=0:
                ind1 = ind1[0]
            else:
                ind1 = np.where(time == int(timec[bloc[j]]))[0][0]
            if len(ind2)!=0:
                ind2 = ind2[0]
            else:
                ind2 = np.where(time == int(timec[bloc[j+1]]))[0][0]
        else:
            ind1 = np.where(time == timec[bloc[j]]-1)[0]
            ind2 = np.where(time == timec[bloc[j+1]]-1)[0]
            if len(ind1)!=0:
                ind1 = ind1[0]
            else:
                ind1 = np.where(time == int(timec[bloc[j]]-1))[0][0]
            if len(ind2)!=0:
                ind2 = ind2[0]
            else:
                ind2 = np.where(time == int(timec[bloc[j+1]]-1))[0][0]
        for x in range(ind1,ind2):
            mean[k] = mean[k] + nGF[x]
        mean[k] = mean[k]/(ind2-ind1)
        xmean[k] = time[ind1]+(time[ind2]-time[ind1])/2
        #plt.scatter(xmean[k],mean[k])
    
    #popt, pcov = curve_fit(func,xmean,mean)
    #tiltles = str(popt[0])+" * x**2 "+str(popt[1])+" * x + "+str(popt[2])
    #plt.plot(xmean, func(xmean, *popt), label=str(nb))
    #plt.title(tiltles)
    #plt.plot(time,nGF,label = 'GF',alpha=0.25,color = 'red')
    #plt.legend()
    #plt.show()
    
    #plt.figure(2)
    #nxaxis = (np.zeros(10))
    #for i in range(10):
    #    nxaxis[i] = i
    #popt, pcov = curve_fit(func,nxaxis,mean)
    #plt.scatter(nxaxis,mean)
    #plt.plot(nxaxis, func(nxaxis, *popt), label=str(nb))
    #plt.show()
    #plt.legend()
    return mean