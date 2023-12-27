import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def normalize(data):
    high, low = abs(max(data)), abs(min(data))
    return data / max(high, low)

def convert_wav(file):
    data, samprate = sf.read(file)
    sf.write(file, data, samprate, subtype = 'PCM_16')

def read_wave(file):

    reader = open(file)

    _, sampwidth, framerate, nframes, _, _ = reader.getparams()
    frames = reader.readframes(nframes)

    reader.close()

    dtypes = {1: np.int8, 2: np.int16, 4: np.int32}

    if sampwidth not in dtypes:
        raise ValueError('unsupported sample width')

    data = np.frombuffer(frames, dtype=dtypes[sampwidth])

    num_channels = reader.getnchannels()
    if num_channels == 2:
        data = data[::2]
    
    from Wave import Wave
    return Wave(data, framerate)

def get_signal_Hz(Hz,sample_rate,length_ts_sec):
    ## 1 sec length time series with sampling rate 
    ts1sec = list(np.linspace(0,np.pi*2*Hz,sample_rate))
    ## 1 sec length time series with sampling rate 
    ts = ts1sec*length_ts_sec
    return(list(np.sin(ts)))

def get_xn(Xs,n):
    '''
    calculate the Fourier coefficient X_n of 
    Discrete Fourier Transform (DFT)
    '''
    L  = len(Xs)
    ks = np.arange(0,L,1)
    xn = np.sum(Xs*np.exp((1j*2*np.pi*ks*n)/L))/L
    return(xn)

def get_xns(ts):
    '''
    Compute Fourier coefficients only up to the Nyquest Limit Xn, n=1,...,L/2
    and multiply the absolute value of the Fourier coefficients by 2, 
    to account for the symetry of the Fourier coefficients above the Nyquest Limit. 
    '''
    mag = []
    L = len(ts)
    for n in range(int(L/2)): # Nyquest Limit
        mag.append(np.abs(get_xn(ts,n))*2)
    return (mag)

def get_Hz_scale_vec(ks,sample_rate,Npoints):
    freq_Hz = ks*sample_rate/Npoints
    freq_Hz  = [int(i) for i in freq_Hz ] 
    return(freq_Hz )

def plot_spectrogram(ts, spec, ks, sample_rate, L, starts, mappable = None):
    plt.figure(figsize=(20,8))
    plt_spec = plt.imshow(spec,origin='lower')

    ## create ylim
    Nyticks = 10
    ks      = np.linspace(0,spec.shape[0],Nyticks)
    ksHz    = get_Hz_scale_vec(ks,sample_rate,len(ts))
    plt.yticks(ks,ksHz)
    plt.ylabel("Frequency (Hz)")

    ## create xlim
    Nxticks = 6
    total_ts_sec = len(ts)/sample_rate
    ts_spec = np.linspace(0,spec.shape[1],Nxticks)
    ts_spec_sec  = ["{:4.2f}".format(i) for i in np.linspace(0,total_ts_sec*starts[-1]/len(ts), Nxticks)]
    plt.xticks(ts_spec,ts_spec_sec)
    plt.xlabel("Time (sec)")

    plt.title("Spectrogram L={} Spectrogram.shape={}".format(L,spec.shape))
    plt.colorbar(mappable,use_gridspec=True)
    plt.show()
    return(plt_spec)
