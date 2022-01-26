# Import libraries
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

try:
	token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)

# Create Spotify object
spotifyObject = spotipy.Spotify(auth=token)

devices = spotifyObject.devices()
for i in range(len(devices['devices'])):
	if  devices['devices'][i]['name'] == "iPad":
		deviceID = devices['devices'][i]['id']

while True:
	print()
	searchQuery = input("What song would you like to play? ")
	print()
	myTrack = spotifyObject.search(searchQuery, limit=3)
	myTracks = []


	for i in range(len(myTrack['tracks']['items'])):
		print(str(i) + ": " + myTrack['tracks']['items'][i]['album']['name'] + " by " + myTrack['tracks']['items'][i]['album']['artists'][0]['name'])
		myTracks.append(myTrack['tracks']['items'][i]['uri'])
	songSelection = input("Is it song 0, 1, or 2? ")
	trackSelectionList = []
	trackSelectionList.append(myTracks[(int(songSelection))])
	spotifyObject.start_playback(deviceID, None, trackSelectionList)
