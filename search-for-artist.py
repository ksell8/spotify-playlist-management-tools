import requests, json, sys, os

#windows users copy console output of get-auth-token.py here
token= os.environ.get("SPOTIFY_TOKEN")

header={"Authorization":"Bearer " + token}

def search(query):
    query = query.replace(" ", "%20")
    type="artist"
    url="https://api.spotify.com/v1/search?q="+query+"&type="+type

    response = requests.get(url, headers=header)

    data = response.json()

    id = data["artists"]["items"][0]["id"]

    return id

def get_playlists_with_artist(id):
    with open("artists-on-playlists.json", 'r') as f:
        data = json.load(f)
    if data[id]:
        for playlist in data[id]:
            url="https://api.spotify.com/v1/playlists/"+playlist

            response = requests.get(url, headers=header)

            data = response.json()

            print(data["name"]+"\n")



if __name__ == "__main__":
    try:
        id = search(sys.argv[1])
        print(sys.argv[1] + " appears on the following playlists:\n")
        get_playlists_with_artist(id)
    except:
        print("Artist not found.")
