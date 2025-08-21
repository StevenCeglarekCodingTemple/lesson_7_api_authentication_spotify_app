import requests
import base64
from credentials import CLIENT_ID, CLIENT_SECRET

class Authentication:
    def __init__(self):
        self.access_token = ''
        
    def get_access_token(self):
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
            
    def set_access_token(self):
        self.access_token = get_access_token()