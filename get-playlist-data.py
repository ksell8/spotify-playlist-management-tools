import requests, json, os, sys

token=os.environ.get("SPOTIFY_TOKEN")
header={"Authorization":"Bearer " + token}
#edit this to your username!
user = "ksell8"

def get_playlists():
    url="https://api.spotify.com/v1/users/"+user+"/playlists"

    response = requests.get(url, headers=header)

    data = response.json()
    playlist_list = []

    while data["next"]:
        for playlist in data["items"]:
            playlist_list.append(playlist["id"])
        url = data["next"]
        response = requests.get(url, headers=header)
        data = response.json()

    #necessary to get last chunk of data
    for playlist in data["items"]:
        playlist_list.append(playlist["id"])

    return playlist_list


def get_tracks(uri,url=''):
    playlist_id = uri
    if url == '':
        url="https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks"

    response = requests.get(url, headers=header)

    return response.json()


def get_artists_json(playlists_list):
    artist_dict = {}
    for playlist in playlists_list:
        data = get_tracks(playlist)
        while data["next"]:
            for song in data["items"]:
                for artist in song["track"]["artists"]:
                    id = artist["id"]
                    if id in list(artist_dict):
                        if playlist not in artist_dict[id]:
                            artist_dict[id].append(playlist)
                    else:
                        artist_dict[id] = []
                        artist_dict[id].append(playlist)
            data = get_tracks(playlist, data["next"])
        if data["items"]:
            for song in data["items"]:
                try:
                    for artist in song["track"]["artists"]:
                        id = artist["id"]
                        if id in list(artist_dict):
                            if playlist not in artist_dict[id]:
                                artist_dict[id].append(playlist)
                        else:
                            artist_dict[id] = []
                            artist_dict[id].append(playlist)
                except:
                    print("you have found the empty playlist, congratulations\n")

    return artist_dict

def get_names_json():
    url="https://api.spotify.com/v1/users/"+user+"/playlists"

    response = requests.get(url, headers=header)

    data = response.json()
    names_dict = {}

    while data["next"]:
        for playlist in data["items"]:
            name = playlist["name"]
            id = playlist["id"]
            names_dict[name] = id
        url = data["next"]
        response = requests.get(url, headers=header)
        data = response.json()

    #necessary to get last chunk of data
    for playlist in data["items"]:
        name = playlist["name"]
        id = playlist["id"]
        names_dict[name] = id

    return names_dict

def get_stats_json(playlists_list):
    stats_dict = {}
    #edit this line to change the audio features accounted for in resulting json
    #for more information about what can be included https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/ will find the average
    features_to_include = ["danceability","acousticness","energy","instrumentalness","liveness","speechiness"]
    for playlist in playlists_list:
        data = get_tracks(playlist)
        tracks_in_playlist = []
        while data["next"]:
            for song in data["items"]:
                tracks_in_playlist.append(song["track"]["id"])

        #construct query
        tracks_to_string = list_to_string(tracks_in_playlist)
        url="https://api.spotify.com/v1/audio_features?ids="+list_to_string

        response = requests.get(url, headers=header)
        data = response.json()
        features_dict = {}
        total = len(tracks_in_playlist)
        for feature in features_to_include:
            sum = 0
            #need to figure out how to iterate over this object

            average = sum/total
            features_dict[feature] = average

        #need to get dict to fill into here
        stats_dict[playlist] = features_dict
    return stats_dict

def list_to_string(list):
    str = ""
    for item in list:
        if str == "":
            str = item
        else:
            str += ","+item


if __name__ == "__main__":
    try:
        if sys.argv[1] == "artists":
            playlists_lists = get_playlists()
            artist_dict = get_artists_json(playlists_list)
            with open("artists-on-playlists.json",'w') as f:
                json.dump(artist_dict, f)
        if sys.argv[1] == "stats":
            playlists_lists = get_playlists()
            stats_dict = get_stats_json(playlists_list)
            with open("stats-per-playlist.json", "w") as f:
                json.dump(stats_dict, f)
        if sys.argv[1] == "names":
            names_dict = get_names_json()
            with open("names-of-playlists.json", "w") as f:
                json.dump(names_dict, f)

    except:
        print("Something went wrong here, remember to include artists || stats || names as a param.")
        raise
3
