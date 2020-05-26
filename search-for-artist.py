import requests, json, sys, os, argparse

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
    if not os.path.exists('artists-on-playlists.json'):
        raise Exception("`python3 get-playlist-data.py artists` must be run before this program can execute.")
    with open("artists-on-playlists.json", 'r') as f:
        data = json.load(f)
    if data[id]:
        for playlist in data[id]:
            url="https://api.spotify.com/v1/playlists/"+playlist

            response = requests.get(url, headers=header)

            data = response.json()

            print(data["name"])
        return
    print("Artist not found.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for which playlists have a particular artist on them.")
    parser.add_argument('artist')
    args = parser.parse_args()
    try:
        id = search(args.artist)
    except:
        print("Artist not found on Spotify.")
        exit(1)
    print(args.artist + " appears on the following playlists:")
    get_playlists_with_artist(id)
