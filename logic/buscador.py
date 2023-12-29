from pickle import load
from scipy.io.wavfile import read
import fingerprint as fngp


try:
    database = load(open('database.dat', 'rb'))
    song_name_index = load(open('song_index.dat', 'rb'))
except FileNotFoundError:
    pass


def score_hashes_against_database(hashes):

    matches_per_song = {}
    for hash, (sample_time, _) in hashes.items():
        if hash in database:
            matching_occurences = database[hash]
            for source_time, song_index in matching_occurences:
                if song_index not in matches_per_song:
                    matches_per_song[song_index] = []
                matches_per_song[song_index].append((hash, sample_time, source_time))
            
    scores = {}
    for song_index, matches in matches_per_song.items():
        song_scores_by_offset = {}
        for hash, sample_time, source_time in matches:
            delta = source_time - sample_time
            if delta not in song_scores_by_offset:
                song_scores_by_offset[delta] = 0
            song_scores_by_offset[delta] += 1

        max = (0, 0)
        for offset, score in song_scores_by_offset.items():
            if score > max[1]:
                max = (offset, score)
        
        scores[song_index] = max

    # Sort the scores for the user
    scores = list(sorted(scores.items(), key=lambda x: x[1][1], reverse=True)) 
    
    return scores

def get_song_in_db(songname):
    
    Fs, audio_input = read(songname)
    constellation = fngp.create_constellation(audio_input, Fs)
    hashes = fngp.create_hashes(constellation, None)
    song_id, _ = score_hashes_against_database(hashes)[0]

    if song_id is None:
        print('No se ha encontrado la cancion')
        return None

    return song_name_index[song_id] if song_id in song_name_index else None

def print_matches(file_name, num_matches=1):

    Fs, audio_input = read(file_name)
    constellation = fngp.create_constellation(audio_input, Fs)
    hashes = fngp.create_hashes(constellation, None)

    scores = score_hashes_against_database(hashes)[:num_matches]
    print(f'Cancion con mayor parecido\n{song_name_index[scores.pop(0)[0]].split("/")[-1]}')
    if num_matches == 1:
        return
    
    print('Otras coincidencias')
    for song_id, _ in scores:
        print(f"{song_name_index[song_id].split("/")[-1]}")