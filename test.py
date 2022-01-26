import discord
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
client = discord.Client()
myTrackNames = []
myTracks = []
suggested = []
suggestedNames = []
username = "Rahul1218"
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

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	
	if message.author == client.user:
		return
	

	if message.content.startswith('suggest'):
		myTracks.clear()
		myTrackNames.clear()
		await message.channel.send("What song would you like to play? ")
		print(message.content.split(" ", 1)[1])
		searchQuery = message.content.split(" ", 1)[1]
		myTrack = spotifyObject.search(searchQuery, limit=3)
		
		for i in range(len(myTrack['tracks']['items'])):
			await message.channel.send(str(i) + ": " + myTrack['tracks']['items'][i]['album']['name'] + " by " + myTrack['tracks']['items'][i]['album']['artists'][0]['name'])
			myTracks.append(myTrack['tracks']['items'][i]['uri'])
			myTrackNames.append(myTrack['tracks']['items'][i]['album']['name'] + " by " + myTrack['tracks']['items'][i]['album']['artists'][0]['name'])
		await message.channel.send("Is it song 0, 1, or 2? ")
		
	if message.content == "0" or message.content == "1" or message.content == "2":
		songSelection = message.content
		trackSelectionList = []
		print(songSelection)
		trackSelectionList.append(myTracks[(int(songSelection))])
		print(trackSelectionList)
		#spotifyObject.start_playback(deviceID, None, trackSelectionList)
		if len(suggestedNames) < 4:
			suggested.append(myTracks[(int(songSelection))])
			suggestedNames.append(myTrackNames[(int(songSelection))])
			if len(suggestedNames) == 3:
				await message.channel.send("Please vote on next track.")
				print(suggestedNames)
		else:
			await message.channel.send("Suggestions are full, please wait for next track.")
		spotifyObject.add_to_queue(myTracks[(int(songSelection))], None)
		myTracks.clear()
		myTrackNames.clear()
	if message.content == "pause":
		spotifyObject.stop_playback(deviceID, None)

client.run("OTM1NzU2NzYzNjA3NzM2MzQw.YfDRZQ.z_5tDyTJVWMOEn1TKtf-H4Qu8LQ")
