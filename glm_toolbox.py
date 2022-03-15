import pandas as pd
from scipy import signal
import numpy as np
import math

def import_data(file_path):
    """Import data from a *.glm file and store it in a data frame"""
      
    # Columns to import
    ColNames = ['time (s)',	
                'Fxal (N)',
                'Fyal (N)',	
                'Fzal (N)',	
                'Txal (Nm)',	
                'Tyal (Nm)',	
                'Tzal (Nm)',	
                'Fxar (N)',	
                'Fyar (N)',	
                'Fzar (N)',	
                'Txar (Nm)',	
                'Tyar (Nm)',	
                'Tzar (Nm)',
                'OPxal (m)',	
                'OPyal (m)',
                'OPxar (m)',	
                'OPyar (m)',	
                'OPxgl (m)',	
                'OPzgl (m)',	
                'OPxgr (m)',	
                'OPzgr (m)',	
                'Fxgl (N)',	
                'Fygl (N)',	
                'Fzgl (N)',	
                'Txgl (Nm)',	
                'Tygl (Nm)',	
                'Tzgl (Nm)',	
                'Fxgr (N)',	
                'Fygr (N)',	
                'Fzgr (N)',	
                'Txgr (Nm)',	
                'Tygr (Nm)',	
                'Tzgr (Nm)',	
                'Fx (N)',	
                'Fy (N)',	
                'Fz (N)',	
                'Tx (Nm)',	
                'Ty (Nm)',	
                'Tz (Nm)',	
                'GF (N)',	
                'LFv (N)',	
                'LFh (N)',	
                'LFt (N)',	
                'LowAcc/X (g)',	
                'LowAcc/Y (g)',	
                'LowAcc/Z (g)',	
                'HighAcc (g)',		
                'RateGyro/X (V/deg.s-1)',	
                'RateGyro/Y (V/deg.s-1)',	
                'RateGyro/Z (V/deg.s-1)',	
                'EnvAcc/X (g)',	
                'EnvAcc/Y (g)',	
                'EnvAcc/Z (g)',	
                'Metronome_b0',	
                'Metronome_b1',	
                'Metronome_b2',	
                'CODA_clock',		
                'LED1',	
                'LED2',	
                'LED3',	
                'LED4',	
                'Switch_MEv2']
        
    # New column names (without unit and front slash)
    NewColNames =  ['time',	
                    'Fxal',
                    'Fyal',	
                    'Fzal',	
                    'Txal',	
                    'Tyal',	
                    'Tzal',	
                    'Fxar',	
                    'Fyar',	
                    'Fzar',	
                    'Txar',	
                    'Tyar',	
                    'Tzar',
                    'OPxal',	
                    'OPyal',
                    'OPxar',	
                    'OPyar',	
                    'OPxgl',	
                    'OPzgl',	
                    'OPxgr',	
                    'OPzgr',	
                    'Fxgl',	
                    'Fygl',	
                    'Fzgl',	
                    'Txgl',	
                    'Tygl',	
                    'Tzgl',	
                    'Fxgr',	
                    'Fygr',	
                    'Fzgr',	
                    'Txgr',	
                    'Tygr',	
                    'Tzgr',	
                    'Fx',	
                    'Fy',	
                    'Fz',	
                    'Tx',	
                    'Ty',	
                    'Tz',	
                    'GF',	
                    'LFv',	
                    'LFh',	
                    'LFt',	
                    'LowAcc_X',	
                    'LowAcc_Y',	
                    'LowAcc_Z',	
                    'HighAcc',		
                    'RateGyro_X',	
                    'RateGyro_Y',	
                    'RateGyro_Z',	
                    'EnvAcc_X',	
                    'EnvAcc_Y',	
                    'EnvAcc_Z',	
                    'Metronome_b0',	
                    'Metronome_b1',	
                    'Metronome_b2',	
                    'CODA_clock',		
                    'LED1',	
                    'LED2',	
                    'LED3',	
                    'LED4',	
                    'Switch_MEv2']
        
    # Load data and store it in a data frame   
    df = pd.read_csv(file_path, 
                      sep = '\t', 
                      header = 0, 
                      usecols = ColNames)
    
    # Rename columns
    df.columns = NewColNames

    return df
      

def compute_cop(glm_df,baseline,z0=0.00155,angle=0.523599):
    """ Compute the vertical position of the center of pressure on the left (CPL) 
    and right (CPR) force sensors. The center of pressure is the point of 
    application of the resultant force of the finger.
    
    syntax: CPL,CPR = compute_cop(glm_df,baseline,...)
    
    Inputs:
        glm_df      glm data frame (as returned by import_data)
        baseline    arrays of indices giving the baseline zone
        
    Outputs:
        CPL, CPR    coordinate of left and right CoP, resp., along the x-axis 
                    of the manipulandum.
    """

    # Forces/torques in ATI reference frames. 
    Fal = -np.array([glm_df.loc[:,'Fxal'],glm_df.loc[:,'Fyal'],glm_df.loc[:,'Fzal']])
    Far = -np.array([glm_df.loc[:,'Fxar'],glm_df.loc[:,'Fyar'],glm_df.loc[:,'Fzar']])
    Tal = -np.array([glm_df.loc[:,'Txal'],glm_df.loc[:,'Tyal'],glm_df.loc[:,'Tzal']])
    Tar = -np.array([glm_df.loc[:,'Txar'],glm_df.loc[:,'Tyar'],glm_df.loc[:,'Tzar']])
    
    # Calibrate forces relative to baseline
    Fal = np.subtract(Fal,np.nanmean(Fal[:,baseline],1).reshape((3,1)))
    Far = np.subtract(Far,np.nanmean(Far[:,baseline],1).reshape((3,1)))
    Tal = np.subtract(Tal,np.nanmean(Tal[:,baseline],1).reshape((3,1)))
    Tar = np.subtract(Tar,np.nanmean(Tar[:,baseline],1).reshape((3,1)))
    
    # Compute CoP using forces and torques (in ATI reference frame)
    CPL_ati = -np.array([(Tal[1,:] + Fal[0,:]*z0)/Fal[2,:], -(Tal[0,:] - Fal[1,:]*z0)/Fal[2,:]])
    CPR_ati = -np.array([(Tar[1,:] + Far[0,:]*z0)/Far[2,:], -(Tar[0,:] - Far[1,:]*z0)/Far[2,:]]) 
    
    # Converts into GLM reference frame
    CPL = -CPL_ati[0,:]*math.sin(angle) - CPL_ati[1,:]*math.cos(angle)
    CPR =  CPR_ati[0,:]*math.sin(angle) + CPR_ati[1,:]*math.cos(angle)
    
    return CPL,CPR
        
       
        
        
        
        
        
        
