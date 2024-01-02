from buscador import print_matches


if __name__ == '__main__':

    #Canciones almacenadas en la base de datos
    
    # Avicii - Wake Me Up
    # Bruno Mars - When I Was Your Man
    # Charlie Puth - We Dont Talk Anymore
    # Ed Sheeran - Thinking Out Loud
    # Green Day - Boulevard Of Broken Dreams
    # MAGIC! - Rude
    # OneRepublic - Counting Stars
    # PUBLIC - Make You Mine
    # Radiohead - Creep
    # Shawn Mendes - Treat You Better

    # Direccion del archivo de muestra de audio para realizar la busqueda
    input_wav = 'logic/recording.wav'
    print_matches(input_wav, num_matches=5)
