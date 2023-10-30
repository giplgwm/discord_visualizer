import discord
import os
from piechart import PieChart

"""This module defines a Discord bot that will read guild data and send back a visual representation."""


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/Activity'):
        visual = PieChart(message.channel).image
        await message.channel.send(file=discord.File(fp=visual, filename=f'{message.guild.name}.png'))


TOKEN = "YOUR-TOKEN-HERE"
if TOKEN == "YOUR-TOKEN-HERE":  # If no token entered
    TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
