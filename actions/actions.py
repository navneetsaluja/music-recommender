from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import random

cid = 'ENTER CLIENT ID'
secret = 'ENTER SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song(mood):
    happy = ['happy', 'joy']
    fear_or_angry = ['fear', 'anger']
    if any(x in mood for x in happy):
        playlist_id = 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC'

    elif (mood == 'sad'):
        playlist_id = 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0'

    elif (mood == 'disgust'):
        playlist_id = 'https://open.spotify.com/playlist/37i9dQZF1DX3YSRoSdA634'

    elif any(x in mood for x in fear_or_angry):
        playlist_id = 'https://open.spotify.com/playlist/37i9dQZF1DX1s9knjP51Oa'

    elif (mood == 'surprise'):
        playlist_id = 'https://open.spotify.com/playlist/37i9dQZF1DX2pSTOxoPbx9'
        
    else:
        playlist_id = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'

    res = sp.playlist(playlist_id)
    total_tracks = res['tracks']['total']
    rand = random.randint(0,total_tracks - 1)
    song_url = res['tracks']['items'][rand]['track']['external_urls']['spotify'] 
    singer_name = res['tracks']['items'][rand]['track']['artists'][0]['name']
    song_name = res['tracks']['items'][rand]['track']['name']

    song = song_name + " by " + singer_name + " available on Spotify at " + song_url
    return song

class ActionGetSong(Action):

    def name(self) -> Text:
        return "action_get_song"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message = tracker.latest_message
        mood = message["entities"][0]["value"]
        song = get_song(mood)

        return [SlotSet("song", song)]

