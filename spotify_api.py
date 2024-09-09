from base64 import b64encode
import requests
import webbrowser

# Spotify API
class Spotify:
    uri = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret  

    def __headers(self):
        return { 'Authorization': f'{self.token_type} {self.access_token}'}  

    def authorize(self):
        uri = '&'.join([
            'https://accounts.spotify.com/authorize?',
            f'client_id={self.client_id}',
            'response_type=code',
            'redirect_uri=http://localhost:8889',
            'scope=playlist-modify-public%20playlist-modify-private'
        ])

        opened = webbrowser.open(uri, 1)
        # if the browser wasn't opened then display
        # the uri to be opened manually
        if not opened:
            print(f'If your browser did not open the url, open the next url manualy:\n{uri}')

    def login(self, auth_code = None):
        encoded = b64encode(
                (f'{self.client_id}:{self.client_secret}').encode('ascii')
            ).decode('ascii')
        headers = { 
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded}'
        }

        if auth_code is None:
            data = {
                'grant_type': 'client_credentials',
                'redirect_uri': 'http://localhost:8889'
            }
        else:
            data = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': 'http://localhost:8889'
            }

        response = requests.post(self.uri, data=data, headers=headers)

        if not response.ok:
            response.raise_for_status()

        response = response.json()

        self.access_token = response['access_token']
        self.token_type = response['token_type']
    
    def search_track(self, query):
        uri = f'https://api.spotify.com/v1/search'

        params = {
            'q': query,
            'type': 'track',
            'limit': 5
        }

        response = requests.get(uri, headers=self.__headers(), params=params)

        if not response.ok:
            response.raise_for_status()

        response = response.json()
        tracks = []

        # parsing json format tracks to object
        for item in response['tracks']['items']:
            tracks.append(Track(
                item['uri'],
                item['name'],
                item['artists']
            ))

        return tracks
    
    def create_playlist(self, name, uris):
        # getting the user_id
        uri = "https://api.spotify.com/v1/me"
        response = requests.get(uri, headers=self.__headers())

        if not response.ok:
            response.raise_for_status()
        
        response = response.json()
        user_id = response['id']

        # creating the playlist
        uri  = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = self.__headers()
        headers['Content-Type'] = 'application/json'

        data = {
            'name': name,
            'public': 'false'
        }
        
        response = requests.post(uri, json=data, headers=headers)

        if not response.ok:
            response.raise_for_status()

        # getting the playlist id
        response = response.json()

        playlist_id = response['id']

        # adding the track's ids to the playlist
        uri = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = self.__headers()
        headers['Content-Type'] = 'application/json'

        data = { 'uris': uris }

        print(data)

        response = requests.post(uri, json=data, headers=headers)

        if not response.ok:
            response.raise_for_status()


class Track:
    def __init__(self, uri, name, artists) -> None:
        self.uri = uri
        self.name = name
        self.artists = artists

    def __str__(self) -> str:
        return f"{self.name} by {', '.join([artist['name'] for artist in self.artists])}"