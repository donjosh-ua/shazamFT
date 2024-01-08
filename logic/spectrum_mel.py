import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt

# Ruta del archivo de audio en formato WAV
archivo_audio = "logic/recording.wav"

# Cargar el archivo de audio
audio, sr = librosa.load(archivo_audio)

# Calcular el espectrograma
espectrograma = librosa.feature.melspectrogram(y=audio, sr=sr)

# Mostrar el espectrograma
librosa.display.specshow(librosa.power_to_db(espectrograma, ref=np.max), y_axis='mel', x_axis='time')
plt.colorbar(format='%+2.0f dB')
plt.title('Espectrograma de Audio')
plt.show()
