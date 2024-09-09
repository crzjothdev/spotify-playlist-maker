import os
from datetime import datetime
from dotenv import dotenv_values
from spotify_api import Spotify
import threading
from server import run_server
from shared import auth_queue
from re import match
from relocation_api import getFilesInPath, moveTo

class Spm:
    playlist_name = None
    tracks = []

    def __init__(self) -> None:
        env_vars = dotenv_values('.env')

        self.id = env_vars.get('SPOTIFY_CLIENT_ID')
        self.secret = env_vars.get('SPOTIFY_CLIENT_SECRET')

    def run(self):
        print('\nWelcome to the Spotify Playlist Maker(SPM)\n')

        # checking if are there any file to be processed
        files = getFilesInPath('./pending/', r'(\d{4})-(\d{2})-(\d{2})\.txt')

        if files:
            print('Decide what would you like to do next:\n')
            print('1. Process on hold playlist creation files\n')
            print('2. Create a new playlist creation file\n')
            # validate that the entered value is integer and either 1 or 2
            selection = int(input())

            if selection == 1:
                self.__processFiles()
            else:
                self.__runMaker()
        else:
            self.__runMaker()

    def __clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def __processFiles(self):
        print("Starting the creation process...")

        spotify = Spotify(self.id, self.secret)
        # client user authorization
        spotify.authorize()
        # starting the web server
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        # waiting until code is available
        print("Waiting for authorization code...")
        auth_code = auth_queue.get()
        #exchanging authorization code for token
        spotify.login(auth_code)

        # creating the playlist
        files = getFilesInPath('./pending/')

        for file in files:
            matched = match(r'(\d{4})-(\d{2})-(\d{2})\.txt', file)
            if matched:
                # process the file creating the playlist
                # and moving it to a new folder
                with open(f'./pending/{file}', 'r') as pending:
                    playlist_name = pending.readline()
                    # reading all tracks id to create the playlist
                    tracks_uris = [line.strip() for line in pending.readlines()]
                
                    spotify.create_playlist(playlist_name, tracks_uris)

                f, s, t = matched.groups()
                moveTo(f'./pending/{file}', f'./target/{f}-{s}-{t}.txt')
            else:
                #moving the file to processed folder
                moveTo(f'./pending/{file}', f'./mis/{file}')

        print('Playlist created successfully!')

    def __runMaker(self):
        # playlist name
        self.playlist_name = input("Let's give a name to your playlist\nEnter the name: ")

        spotify = Spotify(self.id, self.secret)
        spotify.login()

        while True:
            #self.__clear()
            track_query = input('Search for track name, artists or album: (or q to finish): ')
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

        # opening the file in writable mode
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d")
        file = open(f'./pending/{formatted}.txt', "w")
        # writing the playlist name
        file.write(self.playlist_name + "\n")
        # writing down all tracks id
        for track in self.tracks:
            file.write(track.uri + "\n")

        print('Playlist staged successfully!')