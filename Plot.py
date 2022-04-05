import matplotlib.pyplot as plt

import numpy as np



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
    
    for i in range(1,13):
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
    
