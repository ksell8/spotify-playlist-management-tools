import json, sys, click, os

@click.command()
@click.argument('playlist')
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
        print(playlist+ " has the following stats:")
        id = names_dict[playlist]
        if id in stats_dict.keys():
            print(stats_dict[id])
            return 0
        print("Playlist not in stats JSON.  Try rerunning `python3 get-playlist-data.py stats`")
        return 1
    print("Playlist not found.")
    return 1

if __name__ == "__main__":
    search()
