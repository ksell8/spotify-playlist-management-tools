import requests, json, os, sys, argparse

token=os.environ.get("SPOTIFY_TOKEN")
header={"Authorization":"Bearer " + token}
#edit this to your username!
user = ""

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


def get_tracks(uri):
    playlist_id = uri
    url="https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks"

    response = requests.get(url, headers=header)
    data = response.json()
    track_list = []
    while data["next"]:
        for song in data["items"]:
            if not song["track"]["is_local"]:
                track_list.append(song)
        url = data["next"]
        response = requests.get(url, headers=header)
        data = response.json()
    if data["items"]:
        for song in data["items"]:
            if not song["track"]["is_local"]:
                track_list.append(song)

    return track_list


def get_artists_json(playlists_list):
    artist_dict = {}
    for playlist in playlists_list:
        track_list = get_tracks(playlist)
        for song in track_list:
            for artist in song["track"]["artists"]:
                id = artist["id"]
                if id in list(artist_dict):
                    if playlist not in artist_dict[id]:
                        artist_dict[id].append(playlist)
                else:
                    artist_dict[id] = []
                    artist_dict[id].append(playlist)

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
        track_list = get_tracks(playlist)
        track_ids = []
        features_dict = {}
        for song in track_list:
            track_ids.append(song["track"]["id"])

        current_pos = 0
        current_max_length = 100
        total = len(track_ids)

        for feature in features_to_include:
            sum = 0
            while current_max_length < total:
                #construct query
                tracks_to_string = list_to_string(track_ids[current_pos:current_max_length])
                url="https://api.spotify.com/v1/audio-features/?ids="+tracks_to_string
                response = requests.get(url, headers=header)
                data = response.json()
                for song in data["audio_features"]:
                    sum+=song[feature]
                current_pos = current_max_length
                current_max_length += 100
            #get remaining/playlists less than max length
            tracks_to_string = list_to_string(track_ids[current_pos:total-1])
            url = "https://api.spotify.com/v1/audio-features/?ids="+tracks_to_string
            response = requests.get(url, headers=header)
            data = response.json()
            for song in data["audio_features"]:
                sum+=song[feature]

            average = sum/total
            features_dict[feature] = average
        stats_dict[playlist] = features_dict

    return stats_dict

def list_to_string(list):
    str = ""
    for item in list:
        if str == "":
            str = item
        else:
            str += ","+item
    return str



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data JSONs about your playlists using Spotify's API.")
    parser.add_argument('toGenerate', choices=['artists', 'stats', 'names'])
    args = parser.parse_args()
    if args.toGenerate == "artists":
        playlists_list = get_playlists()
        artist_dict = get_artists_json(playlists_list)
        with open("artists-on-playlists.json",'w') as f:
            json.dump(artist_dict, f)
    if args.toGenerate == "stats":
        playlists_list = get_playlists()
        stats_dict = get_stats_json(playlists_list)
        with open("stats-per-playlist.json", "w") as f:
            json.dump(stats_dict, f)
    if args.toGenerate == "names":
        names_dict = get_names_json()
        with open("names-of-playlists.json", "w") as f:
            json.dump(names_dict, f)
