import scipy

from buscador import print_matches
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

def plot_peaks(audio, Fs, num_peaks=12):

    N = len(audio)
    fft = scipy.fft.fft(audio)
    transform_y = 2.0 / N * np.abs(fft[0:N//2])
    transform_x = scipy.fft.fftfreq(N, 1 / Fs)[:N//2]
    plt.xlabel("Frequencia (Hz)")
    all_peaks, props = signal.find_peaks(transform_y)
    peaks, props = signal.find_peaks(transform_y, prominence=0, distance=200)
    largest_peaks_indices = np.argpartition(props["prominences"], -num_peaks)[-num_peaks:]
    largest_peaks = peaks[largest_peaks_indices]
    plt.plot(transform_x, transform_y, label="Spectrum")
    plt.scatter(transform_x[largest_peaks], transform_y[largest_peaks], color="r", zorder=10, label="Constrained Peaks")
    plt.xlim(0, 3000)
    plt.title('Peaks')
    plt.show()

Fs, audio_input = read('logic/recording.wav')
plot_peaks(audio=audio_input,Fs= Fs)
