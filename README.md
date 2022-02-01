# CloudPlay
## Description
A jukebox for the 21st century. For use in cafes and small to medium social gatherings. Users gain equal control over the music being played. Per song playing, three new songs can be suggested. Once three songs have been suggested, users are asked to vote which of the three songs they would like played. As the current song playing nears the end, the song with most votes is added to the queue. Once the current song ends, suggestions are reset and three new songs can be suggested and voted on. User input is done via a Discord server. The music is handled on Spotify. Both Discord and Spotify APIs implemented using Python, Spotipy and Discord.py.
## Setup and Usage
There are a couple of prerequisites for setting up CloudPlay. A Discord server and Spotify account. Then, you need to add bot to your Discord. This will help: https://discordpy.readthedocs.io/en/stable/discord.html. You then need to create a Spotify app. This can be done here: https://developer.spotify.com/dashboard/applications. Set your callback url to google.com.

Then, you need to edit a few lines in your code to match your bot and app. 
1. Line 145, replace the bot ID with your own that you get from Discord. 
2. Line 20, the username must be replaced with your own Spotify username.

Before running the bot, run the following lines in Terminal:
export SPOTIPY_CLIENT_ID="Enter your client ID here"
export SPOTIPY_CLIENT_SECRET="Enter your client secret here"
export SPOTIPY_REDIRECT_URI="Enter your redirect URL here"

That's it! Setup is complete.

The bot will give users directions on how to use it.
