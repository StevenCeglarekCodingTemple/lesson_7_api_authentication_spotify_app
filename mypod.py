import requests
import base64
from credentials import CLIENT_ID, CLIENT_SECRET
from authentication import Authentication

class MyPod:
    def __init__(self, name):
        self.name = name
        self.songs = []
        
    def get_access_token(self):
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
        
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return data['access_token']
        else:
            print("Ran into an error when fetching token")
            
    def search_song(self, title):
        """Search a song by title"""
    
        url = f"https://api.spotify.com/v1/search"
        
        params = {
            'q': title,
            'type': 'track',
            'limit': 1
        }
        
        headers = {
            'Authorization': f"Bearer {self.get_access_token()}"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            song = {
                'artist': data['tracks']['items'][0]['artists'][0]['name'], #Unpacking the data
                'album': data['tracks']['items'][0]['album']['name'],
                'cover_image': data['tracks']['items'][0]['album']['images'][0]['url'],
                'title': data['tracks']['items'][0]['name']
            }
            self.add_song(song)
            
    def add_song(self, song):
        print("========================")
        choice = input("Would you like to add this song to your mypod: (y/n)")
        
        if choice == 'y':
            self.songs.append(song)
            print(f"Successfully added {song['title']} to playlist")
        else:
            print(f"Song Skipped. Did not add {song['title']} to playlist")
            
    def view_songs(self):
        print("================ My Playlist ===============")
        for song in self.songs:
            print(song['title'] + " - " + song['artist'])


def main():
    my_pod = MyPod("Steven's MyPod")

    while True:
        print(f"""
              {my_pod.name}
              1. Search Song
              2. View my songs
              3. Quit
              """)
        
    
        choice = input("\nPlease make a selection: ")
        if choice == '1':
            song_choice = input("Please provide the title of a song you want to search: ")
            my_pod.search_song(song_choice)
        elif choice == '2':
            my_pod.view_songs()
        elif choice == '3':
            break
    
if __name__ == '__main__':
    main()