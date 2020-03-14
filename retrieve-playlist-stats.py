import json, sys, argparse, os

def search(playlist):
    if not os.path.exists("names-of-playlists.json"):
        raise Exception("`python3 get-playlist-data.py names` must be run before this program can execute.")
    if not os.path.exists("stats-per-playlist.json"):
        raise Exception("`python3 get-playlist-data.py stats` must be run before this program can execute.")
    with open('names-of-playlists.json', 'r') as f:
        names_dict = json.load(f)
    with open('stats-per-playlist.json', 'r') as f:
        stats_dict = json.load(f)

    if playlist in names_dict.keys():
        id = names_dict[playlist]
        if id in stats_dict.keys():
            print(stats_dict[id])
            return
        print("Playlist not in stats JSON.  Try rerunning `python3 get-playlist-data.py stats`")
        return
    print("Playlist not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query for the average statistics per playlist.")
    parser.add_argument('playlist')
    args = parser.parse_args()

    print(args.playlist + " has the following stats:")
    search(args.playlist)
