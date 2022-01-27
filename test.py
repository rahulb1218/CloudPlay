import discord
import os
import sys
import json
import spotipy
import webbrowser
import threading
import time
import spotipy.util as util
from json.decoder import JSONDecodeError
client = discord.Client()
myTrackNames = []
myTracks = []
suggested = []
suggestedNames = []
aCount = 0
bCount = 0
cCount = 0
almostOver = False
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
		
currentSong = spotifyObject.current_user_playing_track()
print(json.dumps(currentSong, sort_keys=True, indent=4))

async def display():
	channel = client.get_channel(935797466547253301)
	print("displaying")
	await channel.send(suggestedNames[winner] + " gained the most votes and has been queued to play next!")
	await channel.send("Suggestions are now open, feel free to suggest some songs.")
	

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	channel = client.get_channel(935797466547253301)
	#await client.get_channel("935797466547253301").send("Hi, I am CloudPlay! I am your personal digital jukebox!")
	await channel.send('Hi, I am CloudPlay, your personal digital jukebox! Suggest up to three songs, one at a time like ths: ')
	await channel.send("suggest song name artist name")
	def checkSong():
		global cCount
		global bCount
		global aCount
		threading.Timer(10.0, checkSong).start()
		currentSong = spotifyObject.current_user_playing_track()
		if currentSong['item']['duration_ms'] - currentSong['progress_ms'] < 30000 and currentSong['item']['duration_ms'] - currentSong['progress_ms'] >= 20000:
			print(currentSong['item']['duration_ms'] - currentSong['progress_ms'])
			print("next song queued")
			counts = [aCount, bCount, cCount]
			winnerVoteCount = 0
			winner = 0
			for i in range(len(counts)):
				if counts[i] > winnerVoteCount:
					winnerVoteCount = counts[i]
					winner = i
				print("winner index: " + str(winner))
			spotifyObject.add_to_queue(suggested[winner], None)
			display()
			
			suggested.clear()
			suggestedNames.clear()
			aCount = 0
			bCount = 0
			cCount = 0
		print("checkSong running")
	checkSong()

@client.event
async def on_message(message):
	global cCount
	global bCount
	global aCount
	starttime = time.time()
	
	
	if message.author == client.user:
		return
	if message.content == "a":
		aCount = aCount + 1
		print("Count: " + str(aCount))
		#spotifyObject.add_to_queue(suggested[0], None)
	if message.content == "b":
		bCount = bCount + 1
		print("Count: " + str(bCount))
	if message.content == "c":
		cCount = cCount + 1
		print("Count: " + str(cCount))

	if message.content.startswith('suggest'):
		myTracks.clear()
		myTrackNames.clear()
		await message.channel.send("What song would you like to play? ")
		print(message.content.split(" ", 1)[1])
		searchQuery = message.content.split(" ", 1)[1]
		myTrack = spotifyObject.search(searchQuery, limit=3)
		
		for i in range(len(myTrack['tracks']['items'])):
			await message.channel.send(str(i) + ": " + myTrack['tracks']['items'][i]['name'] + " by " + myTrack['tracks']['items'][i]['album']['artists'][0]['name'])
			myTracks.append(myTrack['tracks']['items'][i]['uri'])
			myTrackNames.append(myTrack['tracks']['items'][i]['name'] + " by " + myTrack['tracks']['items'][i]['album']['artists'][0]['name'])
		print(myTrackNames)
		print(myTracks)
		await message.channel.send("Is it song 0, 1, or 2? ")
		
	if message.content == "0" or message.content == "1" or message.content == "2":
		songSelection = message.content
		trackSelectionList = []
		print(songSelection)
		trackSelectionList.append(myTracks[(int(songSelection))])
		print(trackSelectionList)
		#spotifyObject.start_playback(deviceID, None, trackSelectionList)
		if len(suggestedNames) < 3:
			suggested.append(myTracks[(int(songSelection))])
			suggestedNames.append(myTrackNames[(int(songSelection))])
			if len(suggestedNames) == 3:
				await message.channel.send("Please vote on next track, a, b, or c.")
				await message.channel.send("a: " + suggestedNames[0])
				await message.channel.send("b: " + suggestedNames[1])
				await message.channel.send("c: " + suggestedNames[2])
				await message.channel.send("React to Vote!")
		else:
			await message.channel.send("Suggestions are full, please wait for next track.")
			await message.channel.send("Please vote on next track, a, b, or c.")
			await message.channel.send("a: " + suggestedNames[0])
			await message.channel.send("b: " + suggestedNames[1])
			await message.channel.send("c: " + suggestedNames[2])
		#spotifyObject.add_to_queue(myTracks[(int(songSelection))], None)
		myTracks.clear()
		myTrackNames.clear()

client.run("OTM1NzU2NzYzNjA3NzM2MzQw.YfDRZQ.z_5tDyTJVWMOEn1TKtf-H4Qu8LQ")
