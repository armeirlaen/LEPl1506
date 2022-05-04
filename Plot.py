import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pylab

r2 = np.zeros((6,12))

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
    
def graphe_position_2D(mc):
    
    fig = plt.figure(figsize=(4,4))
    
    ax = fig.add_subplot(111)
    ax.plot(mc[2][1000:10000],mc[1][1000:10000], color ='blue')
    
    ax.set_xlabel("Z")
    ax.set_ylabel("Y")
    ax.set_xlim(200,800)
    ax.set_ylim(-800,-200)
    plt.title('Position of the manipulandum')
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
    
    plt.subplot(1,1,k)
    time = df['time'][:30000]
    GF = df['GF'][8000:38000]
    plt.plot(time,GF,label = 'GF')
    m = np.full(len(time),np.mean(GF))
    #plt.plot(time,m,label = str(m[0]))
    #plt.plot(t,mean)
        
    plt.xlabel('Time [s]')
    plt.ylabel('GF [N]')
        
    plt.title('Grip force')
    plt.legend(loc = 'upper right')
    if k == 1 :
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

def erreur_quad(y1,y2):
    return(y1-y2)**2

def LFGF(df,path,k):
    time = df['time']
    GF = df['GF'][6000:30000]        
    LF = df['LFt'][6000:30000]
    fit = np.polyfit(LF,GF,1)
    ax = np.linspace(np.min(LF),np.max(LF),1000)
    ay = np.zeros(len(ax))
    for i in range(len(ax)):
        ay[i] = ax[i]*(fit[0]+0.1) + fit[1]
    """
    sum = 0
    for j in range(len(LF)) :
        y1 = GF[j]
        y2 = LF[j]*fit[0] + fit[1]
        sum += erreur_quad(y1,y2)
    
    r2[int(path[5])-1][int(path[8:10])-1] = sum/len(LF)
    """
    plt.subplot(2,1,k)
    if k == 1:
        plt.title('Dominant hand')
    else: plt.title('Non-dominant hand')
    plt.plot(LF,GF,label = 'GF')
    plt.plot(ax,ay,label = 'pente de la régression :'+str(round(fit[0],3)))
    plt.xlabel('Load force [N]')
    plt.ylabel(('Grip force [N]'))
    #plt.plot(time,LF,label = 'LF')
    
    #plt.xlim(-5,10)
    plt.legend(loc = 'upper left')
    if k == 2:
        plt.show()

def plot_histogramme(mean):
    #data = [[mean[0],mean[3],mean[6],mean[9]],[mean[1],mean[4],mean[7],mean[10]],[mean[2],mean[5],mean[8],mean[11]]]
    #data2 = [[mean[0],mean[1],mean[2],mean[6],mean[7],mean[8]],[mean[3],mean[4],mean[5],mean[9],mean[10],mean[11],]]
    #data3 = [[mean[0],mean[6]],[mean[1],mean[7]],[mean[2],mean[8]],[mean[3],mean[9]],[mean[4],mean[10]],[mean[5],mean[11]]]
    #data4 = [[mean[0],mean[1],mean[2]],[mean[3],mean[4],mean[5]],[mean[6],mean[7],mean[8]],[mean[9],mean[10],mean[11]]]
    
    plt.boxplot(mean,showfliers =False)
    #pylab.xticks([1,2,3],['Bloc 1','Bloc 2','Bloc 3'])
    #pylab.xticks([1,2],['Dominant Hand','Non-dominant Hand'])
    #pylab.xticks([1,2,3,4,5,6],['Dominant Hand B1','Non-dominant Hand B1',
    #'Dominant Hand B2','Non-dominant Hand B2',
    #                        'Dominant Hand B3','Non-dominant Hand B3'])
    plt.ylabel('GF')
    plt.title('GF according to dominant/non dominant hand while being upside/downside ')
    pylab.xticks([1,2,3,4],['Dominant Hand upside','Non-dominant Hand upside',
                                'Dominant Hand downside','Non-dominant Hand downside'])
    plt.show()
