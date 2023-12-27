from wave import open
import numpy as np
import signal_methods as sm

class Wave:
    def __init__(self, data, frame_rate):
        self.data = sm.normalize(data)
        self.frame_rate = frame_rate

    def make_spectrum(self):
        amplitudes = np.fft.rfft(self.data)
        frequencies = np.fft.rfftfreq(len(self.data), 1 / self.frame_rate)

        from Spectrum import Spectrum
        return Spectrum(amplitudes, frequencies, self.frame_rate)

    def zero_padding(self, n):
        zeros = np.zeros(n)
        zeros[:len(self.data)] = self.data

        self.data = zeros

    def write(self, file):

        reader = open(file, 'w')

        reader.setnchannels(1)
        reader.setsampwidth(2)
        reader.setframerate(self.frame_rate)

        frames = self.quantize().tobytes()
        reader.writeframes(frames)

        reader.close()

    def quantize(self):
        if max(self.data) > 1 or min(self.data) < -1:
            self.data = sm.normalize(self.data)

        return (self.data * 32767).astype(np.int16)
