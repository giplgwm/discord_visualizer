"""This module defines a Discord bot that will read guild data and send back a visual representation."""
import os
import discord
from piechart import PieChart


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Will be called when the bot logs in."""
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """Will be called when a message is sent to a guild the bot is a member in."""
    if message.author == client.user:
        return

    if message.content.startswith('/Activity'):
        visual = PieChart(message.channel).image
        await message.channel.send(file=discord.File(fp=visual, filename=f'{message.guild.name}.png'))


TOKEN = "YOUR-TOKEN-HERE"
if TOKEN == "YOUR-TOKEN-HERE":  # If no token entered
    TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
