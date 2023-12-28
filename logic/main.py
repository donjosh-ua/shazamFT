import buscador as bs
import data_methods as dm


if __name__ == '__main__':

    # Descomentar esta linea para cargar canciones a la base de datos
    # dm.load_db('./data')

    # Direccion del archivo de muestra de audio para realizar la busqueda
    archivo_wav = 'logic/recording.wav'

    try:
        cancion = bs.get_song_in_db(archivo_wav) 
        print(f'{cancion.split('/')[-1] + ' is playing' if cancion is not None else "No se encontró"}')
    except FileNotFoundError:
        print('No se ha encontrado el archivo')
