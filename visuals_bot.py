import discord
import os
from piechart import PieChart, BarChart

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


token = "YOUR-TOKEN-HERE"
if token == "YOUR-TOKEN-HERE": # If no token entered
    token = os.getenv('TOKEN')
client.run(token)
