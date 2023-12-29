import numpy as np
from scipy import signal


def create_constellation(audio, Fs, window_length=0.5, num_peaks=15):

    window_length_samples = (lambda x: x + x % 2)(int(window_length * Fs))
    constellation_map = []
    amount_to_pad = (lambda x: x - audio.size % x)(window_length_samples)
    song_input = np.pad(audio, (0, amount_to_pad))
    frequencies, _, stft = signal.stft(song_input, 
                                           Fs, 
                                           nperseg=window_length_samples,  
                                           nfft=window_length_samples, 
                                           return_onesided=True)

    for time_idx, window in enumerate(stft.T):
        
        spectrum = abs(window)

        # Encuentra las frecuencias mas importantes en la ventana
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)
        n_peaks = min(num_peaks, len(peaks))
        
        # Filtra las n frecuencias mas importantes
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]

        constellation_map += [[time_idx, frequencies[peak]] for peak in peaks[largest_peaks]]

    return constellation_map


def create_hashes(constellation_map, id_song=None):
    # Los hash se crean mediante una funcion de combinatoria

    hashes = {}

    for index, (time, freq) in enumerate(constellation_map):

        for other_time, other_freq in constellation_map[index : index + 100]: 

            diff = other_time - time

            if not 1 <= diff < 10:
                continue

            hash = freq_to_hash(freq, other_freq, diff)
            hashes[hash] = (time, id_song)

    return hashes


def freq_to_hash(freq, other_freq, diff, freq_upper=23_000, freq_bits=10):

    freq_binned = freq / freq_upper * (2 ** freq_bits)
    other_freq_binned = other_freq / freq_upper * (2 ** freq_bits)
    
    return int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)

