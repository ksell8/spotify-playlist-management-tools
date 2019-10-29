import requests, json, os

#windows users copy console output of get-auth-token.py here
token=os.environ.get("SPOTIFY_TOKEN")

header={"Authorization":"Bearer " + token}

#set this to username
username=''

def get_playlists():
    url="https://api.spotify.com/v1/"+username+"/playlists"

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

if __name__ == "__main__":
    playlists_list = get_playlists()
    artist_dict = get_artists_json(playlists_list)

    with open("artists-on-playlists.json",'w') as f:
        json.dump(artist_dict, f)
