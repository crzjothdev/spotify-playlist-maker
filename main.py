import os
from spotify_api import Spotify
print('''
Welcome to the Spotify Playlist Maker(SPM)
Firstly, give a name to your playlist
''')

# playlist name
plist_name = input('Enter the name: ')

# stop flag
stop = False
songs = []

client_id = 'e31e01950af748439305756aff97b5bb'
client_secret= '7ee6b94ab21a4cd3b580fd1469c7660e'

spotify = Spotify(client_id, client_secret)
spotify.login()

adding = True
selected_tracks = []

print('Now lets add some tracks\n')

while adding:
    track_query = input('Enter the name of yout track (or q to finish): ')

    if track_query == 'q':
        adding = False
    else:

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
        selected_tracks.append(tracks[index - 1])

for track in selected_tracks:
    print(f"{track}")

