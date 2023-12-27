import numpy as np
import signal_methods as sm


class Spectrum:

    def __init__(self, amplitudes, frequencies, frame_rate):
        self.amplitudes = np.asanyarray(amplitudes)
        self.frequencies = np.asanyarray(frequencies)
        self.frame_rate = frame_rate

    @staticmethod
    def create_spectrogram(ts, NFFT, noverlap=None):
        """ ts: original time series
            NFFT: The number of data points used in each block for the DFT.
            Fs: the number of points sampled per second, so called sample_rate
            noverlap: The number of points of overlap between blocks. The default value is 128 """

        if noverlap is None:
            noverlap = NFFT / 2

        noverlap = int(noverlap)
        starts = np.arange(0, len(ts), NFFT - noverlap, dtype=int)

        # remove any window with less than NFFT sample size
        starts = starts[starts + NFFT < len(ts)]
        xns = []
        for start in starts:
            # short term discrete fourier transform
            ts_window = sm.get_xns(ts[start:start + NFFT]) 
            xns.append(ts_window)

        specX = np.array(xns).T
        # rescale the absolute value of the spectrogram as rescaling is standard
        spec = 10*np.log10(specX)
        assert spec.shape[1] == len(starts) 
        return (starts,spec)
