import os
from datetime import datetime
from dotenv import dotenv_values
from spotify_api import Spotify

class Spm:
    playlist_name = None
    tracks = []

    def __init__(self) -> None:
        env_vars = dotenv_values('.env')

        self.id = env_vars.get('SPOTIFY_CLIENT_ID')
        self.secret = env_vars.get('SPOTIFY_CLIENT_SECRET')

    def run(self):
        print('\nWelcome to the Spotify Playlist Maker(SPM)\n')

        # playlist name
        self.playlist_name = input("Let's give a name to your new playlist\nEnter the name: ")

        spotify = Spotify(self.id, self.secret)
        spotify.login()

        while True:
            self.__clear()

            track_query = input('Enter the name of your track (or q to finish): ')

            if track_query == 'q':
                break

            tracks = spotify.search_track(track_query)

            for i, track in enumerate(tracks):
                print(f"{i + 1}. {track}\n")

            choise = input("Chose by entering the item number(or r to re-search): ")

            if choise == 'q':
                break
            elif choise == 'r':
                continue

            index = int(choise)
            # adding the selected track to the playlist name
            self.tracks.append(tracks[index - 1])

    def __clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
