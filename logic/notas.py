import numpy as np
from wave import open


def get_signal_Hz(Hz, sample_rate, length_ts_sec):
    ## 1 sec length time series with sampling rate 
    ts1sec = list(np.linspace(0,np.pi*2*Hz,sample_rate))

    ## 1 sec length time series with sampling rate
    ts = ts1sec*length_ts_sec
    
    return(list(np.sin(ts)))


sample_rate   = 4000
length_ts_sec = 1

c = (np.array(get_signal_Hz(528, sample_rate, length_ts_sec)))
c3 = (np.array(get_signal_Hz(132, sample_rate, length_ts_sec)))
e = (np.array(get_signal_Hz(198, sample_rate, length_ts_sec)))
g = (np.array(get_signal_Hz(330, sample_rate, length_ts_sec)))

cM = c+e+g+c3

## -------------------- ##
## 2 seconds of silence
## -------------------- ##
ts_silence = [0]*sample_rate*1

## -------------------- ##
## Add up to 7 seconds
## ------------------- ##
ts = list(e) + list(g) + list(cM)
