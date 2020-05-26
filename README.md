# Spotify Playlist Management Tools

### What is this project?

A couple of python scripts that makes having too many playlists more manageable.

Personally, I have 300 different playlists on Spotify and I write scripts for my abnormal use case.  That's what this project is.

Functionality currently includes being able to search your playlists by artist.
Searching for playlist and returning average track information is next up for development.

NOTE: This is setup to manage all playlists you publically follow/own!

### Environment Setup

To setup your python environment pip install the requirements.txt file.

##### Spotify API Credentials

First you will have to acquire Spotify API access.  Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
& choose either `Create an App` or `Create a Client ID`.  Once you fill out some information you will be given a client id and a client secret.

Fill in the client id and client secret on lines 6-7 of get-auth-token.py.

##### Other Variables

- `username` - enter your username on line 6 of get-playlist-data.py.

-  `token` - the console output of get-auth-token.py should be entered on lines 4 of both get-playlist-data.py and search-for-artist.py

    This authorization token expires every hour, so to make use of the scripts easier currently the variable is populated using a shell environment variable named SPOTIFY_TOKEN. I suggest keeping this method instead of copying and pasting the value.

    On Linux/Unix environments the  variable can be populated from your terminal by calling:
    > export SPOTIFY_TOKEN=\`python get-auth-token.py\`.

    On Windows OS you could try something like:
    > python get-auth-token.py > out.txt

    > set /p SPOTIFY_TOKEN=<out.txt

    Alternatively, you could copy/paste or run a Linux emulator.

    More information about the authorization sequence used in get-auth-token.py can be found in [Spotify's API documentation for client credentials flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow).

### Generating Data

NOTE: Executions of get-playlist-data.py could take some time depending on how many playlists you have!

In order to run the 'Search for Artists Tool' you must generate an artists-on-playlists.json.  To do so, call ```python get-playlist-data.py artists```.  

In order run the the 'Playlist Statistics Retriever' you must generate a names-of-playlists.json and a stats-per-playlists.json.  To do so, call ```python get-playlist-data.py names``` and ```python get-playlist-data.py stats```.

### Calling the Search for Artists Tool

Run ```python search-for-artist.py "<insert artist name here>"``` to return the playlists in which the artist occurs.

### Calling the Playlist Statistics Retriever

Run ```python retrieve-playlist-stats.py "<insert playlist name here>"``` to return the average energy, liveness, speechiness, acousticness, instrumentalness, and danceability stats for the playlist.

Have fun :)
