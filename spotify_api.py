from base64 import b64encode
import requests

# Spotify API
class Spotify:
    uri = 'https://accounts.spotify.com/api/token'
    client_id = 'e31e01950af748439305756aff97b5bb'
    client_secret= '7ee6b94ab21a4cd3b580fd1469c7660e'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def login(self):
        encoded = b64encode(
                (f'{self.client_id}:{self.client_secret}').encode('ascii')
            ).decode('ascii')
        headers = { 
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded}'
        }

        response = requests.post(self.uri, data={ 'grant_type': 'client_credentials' }, headers=headers)

        if not response.ok:
            response.raise_for_status()

        response = response.json()

        self.access_token = response['access_token']
        self.token_type = response['token_type']
    
    def search_track(self, query):
        headers = { 'Authorization': f'{self.token_type} {self.access_token}'}
        uri = f'https://api.spotify.com/v1/search'

        params = {
            'q': query,
            'type': 'track',
            'limit': 5
        }

        response = requests.get(uri, headers=headers, params=params)

        if not response.ok:
            response.raise_for_status()

        response = response.json()
        tracks = []

        # parsing json format tracks to object
        for item in response['tracks']['items']:
            tracks.append(Track(
                item['album']['id'],
                item['album']['name'],
                item['album']['artists']
            ))

        return tracks

class Track:
    def __init__(self, id, name, artists) -> None:
        self.id = id
        self.name = name
        self.artists = artists

    def __str__(self) -> str:
        return f"{self.name} by {', '.join([artist['name'] for artist in self.artists])}"