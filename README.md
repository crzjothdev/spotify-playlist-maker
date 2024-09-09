# Spotify Playlist Maker

**Spotify Playlist Maker** is a console application that allows you to create Spotify playlists without needing the desktop app. It also keeps a file-based history of created playlists with their respective tracks. Straightforward, lightweight, and easy to use!

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Requirements
- Python 3
- Spotify Account

## Installation

1. Download or clone the repository from [https://github.com/crzjothdev/spotify-playlist-maker.git]()

2. Create the three required folders:
   - `target`
   - `pending`
   - `mis`

3. Create the `.env` file and add the following environment variables:
   ```bash
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   ```

4. Install required dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Run the `main.py` file located in the main directory.
   ```bash
   python3 main.py
   ```

6. (Optional) If you are running the application out of a container change
the address `0.0.0.0` to `127.0.0.1` in the server.py file.

## Usage
1. Enter a name for the playlist, then press Enter to continue.
2. Enter a query for the track you would like to add to your playlist.
3. If your track does not appear in the list, you can press *r* to search again.
4. Press *q* to quit the program.

The program creates a file in the `pending` directory so if you whant to save your changes on Spotify you have to run the `main.py`, it will appear a menue with the following options:
1 to process pending playlists
2 to stage a new playlist

5. Press *1* to process all staged playlists
6. Grant the application to modify your public and private playlist

The processed files will be located in the `target` directory, any other
folder will be moved to `mis` directory

## License

MIT License
