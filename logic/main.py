import numpy as np
import matplotlib.pyplot as plt
import warnings as war
from Wave import Wave
import signal_methods as sm
from Spectrum import Spectrum

war.filterwarnings("ignore", category=RuntimeWarning)

sample_rate   = 4000
length_ts_sec = 1

c = (np.array(sm.get_signal_Hz(528, sample_rate, length_ts_sec)))
c3 = (np.array(sm.get_signal_Hz(132, sample_rate, length_ts_sec)))
e = (np.array(sm.get_signal_Hz(198, sample_rate, length_ts_sec)))
g = (np.array(sm.get_signal_Hz(330, sample_rate, length_ts_sec)))

cM = c+e+g+c3

## -------------------- ##
## 2 seconds of silence
## -------------------- ##
ts_silence = [0]*sample_rate*1

ts = list(e) + list(g) + list(cM)
print(ts)

starts, spec = Spectrum.create_spectrogram(ts, 256, 84)

audio = Wave(ts, sample_rate)

audio.write('audio.wav')

mag = sm.get_xns(ts)

Nxlim = 10

ks   = np.linspace(0, len(mag), Nxlim)
ksHz = sm.get_Hz_scale_vec(ks, sample_rate, len(ts))

# plt.figure(figsize=(20,3))
# plt.plot(mag)
# plt.xticks(ks,ksHz)
# plt.title("Frequency Domain")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("|Fourier Coefficient|")
# plt.show()

sm.plot_spectrogram(ts, spec, ks ,sample_rate, 256, starts)
