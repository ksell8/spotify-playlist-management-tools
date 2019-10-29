# Spotify Playlist Searcher

### What is the Spotify Playlist Searcher?

A couple of python scripts that makes having too many playlists more manageable.

Functionality currently includes being able to search your playlists by artist.
Searching by song is the next to be supported with more to follow.

NOTE: This search is of all playlists you follow/own!

### How do I use the Searcher?

##### Spotify API Credentials

First you will have to acquire Spotify API access.  Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
& choose either `Create an App` or `Create a Client ID`.  Once you fill out some information you will be given a client id and a client secret.

Fill in the client id and client secret on lines 6-7 of get-auth-token.py.

##### Other Variables

- `username` - enter your username on line 9 of get-playlist-data.py.

-  `token` - the console output of get-auth-token.py should be entered on lines 4 of both get-playlist-data.py and search-for-artist.py
    This authorization token expires every hour, so to make use of the scripts easier currently the variable is being populated using shell environment variables.
    Unless you are running on a Windows OS I would suggest keeping this method instead of copying and pasting the value.
    The environment variable can be populated by calling: export SPOTIFY_TOKEN=\`python get-auth-token.py\`.

    More information about the authorization sequence used in get-auth-token.py can be found in [Spotify's API documentation for client credentials flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow).

##### Setting up the JSON

The main script (search-for-artist.py) using a JSON called artists-on-playlists.json generated by calling get-playlist-data.py.  So call get-playlist-data.py
before expecting search-for-artist.py to run properly.  This may take some time depending on how many playlists you have.

The JSON is populated by a dictionary with keys being artist identifiers and values being a list of playlist identifiers that the artists appear on.

##### Calling the Searcher

Run ```python search-for-artist.py "<insert artist name here>"``` to return the playlists in which the artist occurs.

Have fun :)
