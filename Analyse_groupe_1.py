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


"""
Partie du code sur les fichier CODA
"""

filename = "Groupe 1_CODA/GBIO_2022_Group_1_S1_20220008_003.TXT"
marker_manipulandum = [5,6,7,8] #les markers utilisés sur le manipulandum
df = coda.import_data(filename)  #on import les données

mc = coda.manipulandum_center(df, markers_id = marker_manipulandum ) #on calcule les coordonnées du centre du manipulandum

"""
Partie du code sur les fichier du manipulandum(.glm)
"""

file = "Groupe 1/Bloc_S1_001.glm"
baseline = [0,1,2]

glm_df = glm.import_data(file)

print(glm_df)

CPL,CPR = glm.compute_cop(glm_df,baseline)

print(CPL)