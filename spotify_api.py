import base64
import requests
from credentials import CLIENT_ID, CLIENT_SECRET

def get_access_token():
    
    # Step 1: Encode credentials
    url = 'https://accounts.spotify.com/api/token'

    cred_string = CLIENT_ID + ':' + CLIENT_SECRET
    byte_creds = cred_string.encode("utf-8")

    b64_string = base64.b64encode(byte_creds).decode('utf-8')

    headers = {
        'Authorization': 'Basic ' + b64_string
    }

    data = {
        "grant_type": "client_credentials"
    }
    
    # Step 3: Get token
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        data = response.json()
        return data['access_token']
    else:
        print("Ran into an error when fetching token")
    

# print(get_access_token(client_id, client_secret))

def search_song(title):
    """Search a song by title"""
    
    url = f"https://api.spotify.com/v1/search"
    
    params = {
        'q': title,
        'type': 'track',
        'limit': 1
    }
    
    headers = {
        'Authorization': f"Bearer {get_access_token()}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(data['tracks']['items'][0]['artists'][0]['name'])
        print(data['tracks']['items'][0]['album']['name'])
        print(data['tracks']['items'][0]['album']['images'][0]['url'])
        print(data['tracks']['items'][0]['name'])
        
    
def search_artist(artist_name):
    """Search artist by artist name"""
    
    url = f"https://api.spotify.com/v1/search"
    
    params = {
        'q': artist_name,
        "type": "artist",
        "limit": 1
    }
    
    headers = {
        "Authorization": f"Bearer {get_access_token()}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        artist = data['artists']['items'][0]
        return {
            "id": artist['id'],
            "name": artist['name'],
            "genres": artist['genres'],
            "popularity": artist['popularity']
        }

def get_top_tracks(artist_id):
    """Get top tracks by aritist by artist ID"""
    
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    
    params = {
        'market': 'US'
    }
    
    headers = {
        "Authorization": f"Bearer {get_access_token()}"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for track_name in data['tracks']:
            print(track_name['name'])
        return data['tracks']

if __name__ == '__main__':
    # search_song('Lose Yourself')
    
    # search_song('hot boy')
    
    # search_song('diamond')
    
    # search_song('bohemian rhapsody')
    
    new_dict = search_artist('Eminem')
    
    get_top_tracks(new_dict['id'])
    