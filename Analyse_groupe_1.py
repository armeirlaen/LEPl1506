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


"""
Partie du code sur les fichier CODA
"""

filename = "C:/Users/arthu/Documents/Résultats_Labo_0803/Groupe 1_CODA/GBIO_2022_Group_1_S1_20220008_003.TXT"
marker_manipulandum = [5,6,7,8] #les markers utilisés sur le manipulandum

numcoord =[3,4,6,7,8,9]
numforce =[i for i in range(1,7)]

def printCoord(pa):
    df = coda.import_data(pa)
    mc= coda.manipulandum_center(df, markers_id = marker_manipulandum )
    x=mc[0]
    y=mc[1]
    z=mc[2]
    return x,y,z

num =[3,4,6,7,8,9]

k=0
for i in num:
    k+=1
    pat= "C:/Users/arthu/Documents/Résultats_Labo_0803/Groupe 1_CODA/GBIO_2022_Group_1_S1_20220008_00"+str(i)+".TXT"
    x,y,z = printCoord(pat)
    plt.subplot(6,1,k)
    time=np.linspace(0,51,len(x))
    plt.plot(time,x)
    plt.title("x:00"+str(i))

plt.show()

k=0
for i in num:
    k+=1
    pat= "C:/Users/arthu/Documents/Résultats_Labo_0803/Groupe 1_CODA/GBIO_2022_Group_1_S1_20220008_00"+str(i)+".TXT"
    x,y,z = printCoord(pat)
    plt.subplot(6,1,k)
    time=np.linspace(0,51,len(y))
    plt.plot(time,y)
    plt.title("y:00"+str(i))

plt.show()
"""
Partie du code sur les fichier du manipulandum(.glm)
"""

file = "C:/Users/arthu/Documents/Résultats_Labo_0803/Groupe 1/Bloc_S1_006.glm"
baseline = [0,1,2]

glm_df = glm.import_data(file)


def printForce(df):
    time= df.time
    x= df.Fxal
    y= df.Fyal
    LF=(x**2+y**2)**0.5
    GF= df.Fzal
    return time,LF,GF
    
num = numforce

k=0
for i in num:
    k+=1
    path="C:/Users/arthu/Documents/Résultats_Labo_0803/Groupe 1/Bloc_S1_00"+str(i)+".glm"
    curr_df = glm.import_data(path)
    t,LFi,GFi= printForce(curr_df)
    plt.subplot(6,1,k)
    plt.plot(t,GFi)
    plt.title("GF:00"+str(i))

plt.show()

k=0
for i in num:
    k+=1
    path="C:/Users/arthu/Documents/Résultats_Labo_0803/Groupe 1/Bloc_S1_00"+str(i)+".glm"
    curr_df = glm.import_data(path)
    t,LFi,GFi= printForce(curr_df)
    plt.subplot(6,1,k)
    plt.plot(t,LFi)
    plt.title("LF:00"+str(i))

plt.show()

CPL,CPR = glm.compute_cop(glm_df,baseline)

print("CPL",CPL)