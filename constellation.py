import scipy

from buscador import print_matches
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

def plot_constellation(audio, Fs, window_length=0.5, num_peaks=12):
    #Determina si el audio esta en uno o dos canales
    if audio.ndim == 1 :
        audio = audio.reshape(-1)
    else :
        audio = audio[:, 0].ravel()
        
    window_length_samples = (lambda x: x + x % 2)(int(window_length * Fs))
    constellation_map = []
    amount_to_pad = (lambda x: x - audio.size % x)(window_length_samples)
    song_input = np.pad(audio, (0, amount_to_pad))
    frequencies, _, stft = signal.stft(song_input,
                                        Fs, 
                                        nperseg=window_length_samples,  
                                        nfft=window_length_samples, 
                                        return_onesided=True)

    for time_index, window in enumerate(stft.T):
        
        spectrum = abs(window)

        # Encuentra las frecuencias mas importantes en la ventana
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)
        n_peaks = min(num_peaks, len(peaks))

        # Filtra las n frecuencias mas importantes
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]

        constellation_map += [[time_index, frequencies[peak]] for peak in peaks[largest_peaks]]

    pico_tiempos = [x[0]/3 for x in constellation_map] 
    pico_frecuencias = [x[1] for x in constellation_map]
    plt.xlim([0,12])
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Frecuencia (Hz)")
    plt.scatter(pico_tiempos, pico_frecuencias, color='black', marker='x')
    plt.title("Constellation")
    plt.show()

Fs, audio_input = read('logic/recording.wav')
plot_constellation(audio=audio_input,Fs= Fs)
