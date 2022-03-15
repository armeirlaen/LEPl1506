import matplotlib.pyplot as plt

import numpy as np



def graphe_position(pos_x,pos_y,pos_z):
    time = np.linspace(0,52,len(pos_x))
    
    plt.subplot(3,1,1)
    plt.plot(time,pos_x)
    
    plt.subplot(3,1,2)
    plt.plot(time,pos_y)
    
    plt.subplot(3,1,3)
    plt.plot(time,pos_z)
    
    
    
    plt.show()
    
def graphe_pos_3D(pos_x,pos_y,pos_z):
    
    fig = plt.figure(figsize=(4,4))
    
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(pos_x,pos_y,pos_z)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    plt.show()
    
def only_y(centers):
    time = np.linspace(0,52,len(centers[0]))
    i=0
    while i < len(centers):
        
        plt.subplot(len(centers),1,i+1)
        plt.plot(time,centers[i])
        i+=1
    
    plt.show()