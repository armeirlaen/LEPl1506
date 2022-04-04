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
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math as math


"""
Partie du code sur les fichier CODA
"""

marker_manipulandum = [5,6,7,8] #les markers utilisés sur le manipulandum


pathToFolder = "C:/Users/arthu/Documents/Résultats_Labo_0803/"
strpath = "GBIO_2022_Group_1_"
strpathbis = "_20220008_0"
strpath1= "Bloc_"
strpath1bis="_0"

Sujets = {"S1" : { "A l'endroit" : [[3,4,6,7,8,9],[1,2,3,4,5,6]], "A l'envers" : [[10,11,12,13,14,15],[7,8,9,10,11,12]] },
          "S2" : { "A l'endroit" : [[1,2,3,4,5,6],[1,2,3,4,5,6]], "A l'envers" : [[7,8,9,10,11,12],[7,8,9,10,11,12]] },
          "S3" : { "A l'endroit" : [[1,2,3,5,6,7],[1,2,3,4,5,6]], "A l'envers" : [[9,10,11,12,13,14],[7,8,9,10,11,12]] },
          "S4" : { "A l'endroit" : [[2,3,4],[1,2,3]], "A l'envers" : [[],[]] }
          }


def printCoord(pa):
    df = coda.import_data(pa)
    mc= coda.manipulandum_center(df, markers_id = marker_manipulandum )
    x=mc[0]
    y=mc[1]
    z=mc[2]
    return x,y,z

num =[3,4,6,7,8,9]

def plotX(Sujet,Orientation):
    num = Sujets[Sujet][Orientation][0]

    #Plot x 
    k=0
    for i in num:
        k+=1
        if i<10:
            pat=pathToFolder+"Groupe 1_CODA/"+strpath+Sujet+strpathbis+"0"+str(i)+".TXT"
        else:
            pat=pathToFolder+"Groupe 1_CODA/"+strpath+Sujet+strpathbis+str(i)+".TXT"
        x,y,z = printCoord(pat)
        plt.subplot(6,1,k)
        time=np.linspace(0,51,len(x))
        plt.plot(time,x)
        plt.title("x:00"+str(i))

    plt.show()

def plotY(Sujet,Orientation):
    num = Sujets[Sujet][Orientation][0]

    #Plot y
    k=0
    for i in num:
        k+=1
        if i<10:
            pat=pathToFolder+"Groupe 1_CODA/"+strpath+Sujet+strpathbis+"0"+str(i)+".TXT"
        else:
            pat=pathToFolder+"Groupe 1_CODA/"+strpath+Sujet+strpathbis+str(i)+".TXT"
        x,y,z = printCoord(pat)
        plt.subplot(6,1,k)
        time=np.linspace(0,51,len(y))
        plt.plot(time,y)
        plt.title("y:00"+str(i))
    

    plt.show()
"""
Partie du code sur les fichier du manipulandum(.glm)
"""


#glm_df = glm.import_data(file)


def printForce(df):
    time= df.time
    x= df.Fxal
    y= df.Fyal
    LF=(x**2+y**2)**0.5
    GF= df.Fzal
    return time,LF,GF
    
def plotGF(Sujet,Orientation):
    num = Sujets[Sujet][Orientation][1]
    #Plot GF
    for i in range(1,13):
        if i<10:
            path=pathToFolder+"Groupe 1/"+"Bloc_"+Sujet+"_00"+str(i)+".glm"
        else:
            path=pathToFolder+"Groupe 1/"+"Bloc_"+Sujet+"_0"+str(i)+".glm"
        curr_df = glm.import_data(path)
        t,LFi,GFi= printForce(curr_df)
        exp = np.polyfit(t, np.log(GFi), 1, w=np.sqrt(GFi))
        #plt.subplot(6,1,k)
        plt.plot(t,exp)
        plt.plot(t,GFi,label=str(i))
        plt.legend(loc="upper left")
        #plt.title("GF:00"+str(i))

    plt.show()

def plotLF(Sujet,Orientation):
    #PLot LF
    for i in range(5,7):
        if i<10:
            path=pathToFolder+"Groupe 1/"+"Bloc_"+Sujet+"_00"+str(i)+".glm"
        else:
            path=pathToFolder+"Groupe 1/"+"Bloc_"+Sujet+"_0"+str(i)+".glm"
        curr_df = glm.import_data(path)
        t,LFi,GFi= printForce(curr_df)
        ex = np.polyfit(t, np.log(LFi), 1, w=np.sqrt(LFi))
        #plt.subplot(6,1,k)
        expPlot = GFi
        j=0
        for x in t:
            expPlot[j] = math.exp(ex[0]) * math.exp(ex[0]*x)
            j+=1
        plt.plot(t,expPlot)
        plt.plot(t,LFi,label=str(i))
        
        plt.legend()
        #plt.title("LF:00"+str(i))

    plt.show()

def plotLFGF(Sujet,Orientation):
    #PLot LF
    for i in range(1,13):
        if i<10:
            path=pathToFolder+"Groupe 1/"+Sujet+"_00"+str(i)+".glm"
        else:
            path=pathToFolder+"Groupe 1/"+Sujet+"_0"+str(i)+".glm"
        curr_df = glm.import_data(path)
        t,LFi,GFi= printForce(curr_df)
        plt.subplot(6,1,k)
        plt.plot(GFi,LFi,label=str(k))
        plt.legend()
        plt.title("LF:00"+str(k))

    plt.show()

    
    

#plotY("S1","A l'endroit")
plotLF("S1","A l'endroit")


#CPL,CPR = glm.compute_cop(glm_df,baseline)

#print("CPL",CPL)