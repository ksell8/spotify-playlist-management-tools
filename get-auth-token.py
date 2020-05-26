import requests, json, os

def get_creds():

    #fill in client id and secret here!
    client_id = ''
    client_secret = ''

    grant_type = 'client_credentials'

    url = 'https://accounts.spotify.com/api/token'

    params = {'grant_type':grant_type}

    response=requests.post(url, data=params, auth=(client_id, client_secret))

    data = response.json()

    print(data["access_token"])

    return data["access_token"]

if __name__ == "__main__":
    get_creds()
