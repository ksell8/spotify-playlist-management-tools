import json, sys

def search(playlist):
    with open('names-of-playlists.json', 'r') as f:
        names_dict = json.load(f)
    with open('stats-per-playlist.json', 'r') as f:
        stats_dict = json.load(f)

    if playlist in names_dict.keys():
        id = names_dict[playlist]

    print(stats_dict[id])



if __name__ == "__main__":
    try:
        print(sys.argv[1] + " has the following stats:")
        search(sys.argv[1])
    except:
        print("Playlist not found.")
        raise
