# -*- coding: utf-8 -*-
"""
Some tools to process signals: filtering, differentiating, etc.
    
Created on Thu Mar 18 08:06:14 2021

@author: opsomerl
"""
import numpy as np
from scipy import signal
from scipy import interpolate as interp

def filter_signal(y, fs=200, fc=10, N=4, type='low'):
    """Filters signal y by using a Butterworth filter of order N and a cut-off 
    frequency fc. y must be 1-dimensional"""
    
    # Converts the cut-off frequency to [pi rad/s]
    Wn = fc/(fs/2)
    
    # Temporarily replace NaN's with cubic spline interpolation/extrapolation
    available = np.isfinite(y)
    if not any(available):
        return(y)
    
    ns  = len(y)
    xsp = np.arange(0,ns)
    qsp = interp.pchip(xsp[available],y[available],extrapolate=False)
    ysp = qsp(xsp)
    y[~available] = ysp[~available]
        
    # Create butterworth digital filter
    b,a = signal.butter(N,Wn,btype=type,analog=False)
    
    # Filter y with a zero-phase forward and reverse digital IIR
    Istart = min(np.where(available)[0])
    Iend   = max(np.where(available)[0])
    ys_f = signal.filtfilt(b,a,y[Istart:Iend])
    
    # Output
    ys = np.copy(y)
    ys[Istart:Iend] = ys_f    
    
    # Put NaNs back
    ys[~available] = np.nan
    
    return ys


def derive(sig,freq):
    """Computes the derivative of the input signal. 
    
     Syntax: out = derive(sig,freq)      
    
     Inputs:
       sig           input signal (1-d numpy array)
       freq          sampling frequency
       axis          axis along which the derivative is computed 
    
     Outputs:
       out           derivative of input signal"""
  
        
    # Q vector
    qs = round(0.01*freq)
    denom = 2 /freq * sum(np.square((np.linspace(1,qs,num=qs))))
    Q = np.linspace(-qs,qs,num=(2*qs+1))
    
    
    # Compute derivatives
    out = -np.convolve(sig,Q,'same')/denom
        
    out[:qs] = np.nan
    out[-qs:] = np.nan
        
    
    return out