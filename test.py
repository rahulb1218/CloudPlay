import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('fuck me daddy ;)')

client.run("OTM1NzU2NzYzNjA3NzM2MzQw.YfDRZQ.z_5tDyTJVWMOEn1TKtf-H4Qu8LQ")