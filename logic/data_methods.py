from glob import glob
from pickle import dump
from scipy.io.wavfile import read
import fingerprint as fngp

def create_db(folder: str):

    songs = glob(folder + '/*.wav')
    song_name_index = {}
    database = {}

    for index, filename in enumerate(sorted(songs)):

        song_name_index[index] = filename

        Fs, audio_input = read(filename)
        constellation = fngp.create_constellation(audio_input, Fs)
        hashes = fngp.create_hashes(constellation, index)

        for hash, time_index_pair in hashes.items():
            if hash not in database:
                database[hash] = []
            database[hash].append(time_index_pair)

    with open('database.dat', 'wb') as db:
        dump(database, db, 5)

    with open('song_index.dat', 'wb') as songs:
        dump(song_name_index, songs, 5)