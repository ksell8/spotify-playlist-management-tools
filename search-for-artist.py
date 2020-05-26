import requests, json, sys, os, click

#windows users copy console output of get-auth-token.py here
token= os.environ.get("SPOTIFY_TOKEN")

header={"Authorization":"Bearer " + token}

@click.command()
@click.argument('artist')
def search(artist):
    new_query = artist.replace(" ", "%20")

    type="artist"
    url="https://api.spotify.com/v1/search?q="+new_query+"&type="+type

    response = requests.get(url, headers=header)

    data = response.json()

    index = choose_result(data["artists"]["items"])
    id = data["artists"]["items"][index]["id"]

    get_playlists_with_artist(data["artists"]["items"][index]["name"],id)

def choose_result(data):
    index = 0
    for artist in data:
        print(str(index)+": "+data[index]["name"])
        index+=1
    index = click.prompt('Which artist did you mean?', default=0)
    return index

def get_playlists_with_artist(artist,id):
    if not os.path.exists('artists-on-playlists.json'):
        raise Exception("`python3 get-playlist-data.py artists` must be run before this program can execute.")
    with open("artists-on-playlists.json", 'r') as f:
        data = json.load(f)
    if id in data.keys():
        print(artist + " appears on the following playlists:")
        for playlist in data[id]:
            url="https://api.spotify.com/v1/playlists/"+playlist

            response = requests.get(url, headers=header)

            data = response.json()

            print(data["name"])
    else:
        print(artist+" does not appear on any playlists.")


if __name__ == "__main__":
    search()
