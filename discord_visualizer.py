import discord
import os
import plotly.express as px
import pandas as pd

intents = discord.Intents.all()

client = discord.Client(intents=intents)


async def get_user_activities(guild):
    activities = {}
    for member in guild.members:
        if member.bot:
            continue
        if member.activity:
            if member.activity.name in activities:
                activities[member.activity.name].append(member.name)
            else:
                activities[member.activity.name] = [member.name]
        else:
            if 'None' in activities:
                activities['None'].append(member.name)
            else:
                activities['None'] = [member.name]
    members_in_each = [len(members) for act, members in activities.items()]
    fig = px.pie(names=activities.keys(), values=members_in_each,
                 title=f"Whats being played in {guild.name}?", labels={'values':'Members Playing'}, template='plotly_dark')
    fig.update_traces(textposition='inside', textinfo='value+label', textfont_size=20, hoverinfo='label+percent')
    fig.update_layout(showlegend=True, title_x=0.5, titlefont_size=24)
    fig.write_image(f"images/{guild.id}.png")


async def send_visual(channel):
    await channel.send(file=discord.File(f"images/{channel.guild.id}.png"))
    os.unlink(f"images/{channel.guild.id}.png")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/Activity'):
        await get_user_activities(message.guild)
        await send_visual(message.channel)


token = os.getenv("TOKEN") or ""
if token == "":
    raise Exception("Please add your token to the Secrets pane.")
client.run(token)
