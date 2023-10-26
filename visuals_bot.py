import discord
import os
from visual_generator import *

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
        activities, members = await get_user_activities(message.guild)
        create_pie_chart(activities, message.guild, members)
        await send_visual(message.channel)


token = os.getenv("TOKEN")
client.run(token)
