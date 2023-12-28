from pickle import load
from scipy.io.wavfile import read
import fingerprint as fngp


database = load(open('database.dat', 'rb'))
song_name_index = load(open('song_index.dat', 'rb'))


def score_hashes_against_database(hashes):

    matches_per_song = {}
    
    for hash, (sample_time, _) in hashes.items():
        
        if hash in database:
            matching_occurences = database[hash]
            for source_time, song_index in matching_occurences:
                if song_index not in matches_per_song:
                    matches_per_song[song_index] = []
                matches_per_song[song_index].append((hash, sample_time, source_time))
            
    match_scores = {}
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
        
        # print(song_scores_by_offset.items())
        # match_scores[song_index] = max(song_scores_by_offset.items(), key=lambda item: item[1])
        match_scores[song_index] = max

    return list(sorted(match_scores.items(), key=lambda x: x[1][1], reverse=True))


def get_song_in_db(songname):
    
    Fs, audio_input = read(songname)
    constellation = fngp.create_constellation(audio_input, Fs)
    hashes = fngp.create_hashes(constellation, None)
    song_id, _ = score_hashes_against_database(hashes)[0]

    if song_id is None:
        print('No se ha encontrado la cancion')
        return None

    return song_name_index[song_id] if song_id in song_name_index else None

