import pandas as pd
def drawdown(return_series:pd.Series):
    wealth_index=1000*(1+return_series).cumprod()
    previous_peaks=wealth_index.cummax()
    drawdowns=(wealth_index-previous_peaks)/previous_peaks
    return pd.DataFrame({
        "Wealth":wealth_index,
        "Peaks":previous_peaks,
        "Drawdown":drawdowns               
    })

def get_ffme_returns():
    me_m=pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv",header=0,index_col=0,parse_dates=True,na_values=-99.99)
    rets=me_m[['Lo 10','Hi 10']]
    rets.columns=['SmallCap','LargeCap']
    rets=rets/100
    rets.index=pd.to_datetime(rets.index,format="%Y%m").to_period('M')
    return rets

def get_hfi_returns():
    hfi=pd.read_csv("edhec-hedgefundindices.csv",header=0,index_col=0,parse_dates=True)
    hfi=hfi/100
    hfi.index=hfi.index.to_period('M')
    return hfi

def skewness(r):
    demeaned_r=r-r.mean()
    sigma_r=r.std(ddof=0)
    return (demeaned_r**3).mean()/sigma_r**3

def kurtosis(r):
    demeaned_r=r-r.mean()
    sigma_r=r.std(ddof=0)
    return (demeaned_r**4).mean()/sigma_r**4

def semideviation(r):
    is_negative=r<0
    return r[is_negative].std(ddof=0)

import scipy.stats
import numpy as np
def is_normal(r,level=0.01):
    statistic,pvalue=scipy.stats.jarque_bera(r)
    return pvalue>level

def var_historic(r,level=5):
    """VaR Historic"""
    if isinstance(r,pd.DataFrame):
        return r.aggregate(var_historic,level=level)
    elif isinstance(r,pd.Series):
        return -np.percentile(r,level,axis=0)
    else:
        return TypeError("Expected input to be Series or DataFrame")

from scipy.stats import norm    
def var_gaussian(r,level=5):
    """VaR Gaussian"""
    z=norm.ppf(level/100)
    return -(r.mean()+z*r.std(ddof=0))

    

    

