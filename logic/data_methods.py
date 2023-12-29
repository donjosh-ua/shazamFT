from glob import glob
from pickle import dump
from scipy.io.wavfile import read
from tqdm import tqdm
import fingerprint as fngp
from os import remove


db_name = 'database.dat'
song_index_name = 'song_index.dat'

def drop_db():
    try:
        remove(db_name)
        remove(song_index_name)
    except FileNotFoundError:
        pass

def load_db(folder: str):

    # Nombres de todas las canciones en la carpeta folder
    songs = glob(folder + '/*.wav')
    song_name_index = {}
    database = {}

    for index, filename in enumerate(tqdm(sorted(songs))):
        # Se crea una constelacion de puntos para cada cancion y su respectivo hash
        # La constelacion vendria a ser el identificador de la cancion en el dominio de frecuencias
        song_name_index[index] = filename
        print(f'Procesando {filename.split('/')[-1]}...')

        Fs, audio_input = read(filename)
        audio_input = audio_input.reshape(-1)
        constellation = fngp.create_constellation(audio_input, Fs)
        hashes = fngp.create_hashes(constellation, index)

        for hash, time_index_pair in hashes.items():
            if hash not in database:
                database[hash] = []
            database[hash].append(time_index_pair)


    # Guardado de los codigos hash
    with open(db_name, 'wb') as db:
        dump(database, db, 5)

    # Guardado de los nombres de las canciones
    with open(song_index_name, 'wb') as songs:
        dump(song_name_index, songs, 5)