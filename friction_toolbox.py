# -*- coding: utf-8 -*-
"""
Some tools to analyze friction data.
    
Created on Wed Mar 2 
@author: opsomerl
"""
import numpy as np


def find_slip_onset(COPx,TFx,TFz,NF,cop_thresh=0.75,tf_thresh=0.25,nf_thresh=0.25):
    """ This method finds the points of slip onset at each reversal of the 
    rubbing direction within a friction task. 
    
    Syntax: mu,slip_index,iStart,iEnd = find_slip_onset(COPx,TFx,TFz,NF,...) 
   
    Inputs:
      COPx         displacement of the center of pressure along x-axis
      TFx          tangential force along x-axis
      TFz          tangential force along z-axis
      NF           normal force
   
    Outputs:
      slip_index           indices of slip onset
      mu                   static coefficient of friction at each slip point
      iStart, iEnd         start/end index of search zones
      """
    
    # Check input sizes
    if len(COPx)!=len(TFz) or len(TFz)!=len(TFx) or len(TFx)!=len(NF):
        raise NameError('Vectors must be the same length')
    
    # Compute the norm of the normal and tangential forces and TF/NF
    NF = abs(NF)
    TF = np.hypot(TFx,TFz)
    ratio = TF/NF
    
    # Find first index where NF>NF_thresh
    i0 = np.nonzero(NF>nf_thresh)[0][0]
    
    # Find first index where NF>NF_thresh starting from the end
    if NF[-1]>nf_thresh:
        iend=len(NF)-1
    else:
        reversed_NF=NF[::-1]
        iend=np.nonzero(reversed_NF>nf_thresh)[0][0]
        iend=len(NF)-iend
        
    # Find where tangential force changes sign. This marks the beginnings of each
    # search zone
    iRoots = i0 + np.nonzero(np.diff(np.sign(TFx[i0:iend])))[0]
    iStart = np.insert(iRoots,0,i0) #Add i0 as the beginning of the first search zone
    
    # Find the end of each search zone by looking at the COP displacement 
    # (end zone is reached when displacement is greater than cop_thresh)
    iEnd = np.zeros(len(iStart),dtype=int)
    out = np.zeros(len(iStart),dtype=bool)
    out[0]=True
    out[-1]=True
    
    for i in range(0,len(iStart)-1):       
        y_loc  = COPx[iStart[i]:iStart[i+1]]
        dy_loc = np.diff(y_loc,n=1)

        slope=np.nanmean(dy_loc[0:np.floor((iStart[i+1]-iStart[i])/2).astype(np.int)])
        
        if slope <0:
            extrem=min(COPx[iStart[i]:iStart[i+1]])
        else:
            extrem=max(COPx[iStart[i]:iStart[i+1]])
    
        displacement_thresh=cop_thresh*abs(extrem - y_loc[0])
        
        tf_loc=abs(np.mean(TFx[iStart[i]:iStart[i+1]]))
        nf_loc=np.mean(NF[iStart[i]:iStart[i+1]])
        
        if displacement_thresh > 0.002 and tf_loc > tf_thresh and nf_loc > nf_thresh:
            i_end_loc = np.nonzero(abs(y_loc-y_loc[0])>=displacement_thresh)[0][0]
            if i_end_loc==0:
                out[i]=True
            else:
                iEnd[i]=(iStart[i]+i_end_loc-1).astype(np.int)
                
        else:
            out[i]=True
    
    iStart=iStart[np.logical_not(out)]
    iEnd=iEnd[np.logical_not(out)]
    
    check_indexes=iEnd-iStart
    if any(check_indexes<=0):
        raise NameError('Some start indexes are equal to - or bigger than - their corresponding stop indexes')
    
    # Search for slip points as the points where TF/NF is maximal. TF/NF then
    # theoritically corresponds to the static coefficient of friction (mu)
    nz = len(iStart)
    mu = np.zeros(nz)
    slip_index = np.zeros(nz,dtype=int)
    directions = np.zeros(nz,dtype=int)
    
    for i in range(0,nz):
        mu_loc = ratio[iStart[i]:iEnd[i]]
        imax = np.argmax(mu_loc)
        
        y_loc  = COPx[iStart[i]:iEnd[i]]
        dy_loc = np.diff(y_loc,n=1)
        
        slip_index[i] = iStart[i]+imax-1
        mu[i] = mu_loc[imax]
        directions[i] = np.sign(np.nanmean(dy_loc))
        
    # Remove slip points corresponding to abnormally low values of TF or NF
    discard= (abs(TFx[slip_index])<tf_thresh).astype(bool) | (NF[slip_index]<nf_thresh).astype(bool)
    slip_index=slip_index[np.logical_not(discard)]
    mu=mu[np.logical_not(discard)]
    directions=directions[np.logical_not(discard)]
    
    # Remove outliers (code missing, can be added later if needed)
    
    # Return values
    
    return mu,slip_index,iStart,iEnd


def get_mu_fit(mu,NF):
    """ Fit a negative-power polynomial to the relationship between the static 
    coefficient of friction (mu) and the normal force (NF): mu = k*(NF)^(n-1)
    
    Syntax:  k,n = get_mu_fit(mu,NF)
   
    Inputs:
      mu         arrays of values of coefficient of friction
      NF         corresponding values of NF
   
    Outputs:
      k,n: parameters of the power law   
    """
    
    fit_coeff = np.polyfit(np.log(NF),np.log(mu),1)
    k = np.exp(fit_coeff[1])
    n = fit_coeff[0]+1
    
    return k,n
