import discord
import os
import plotly.express as px


async def get_user_activities(guild):
    """Get a list of activities being done by non-bot members in a guild."""
    activities = {}
    for member in guild.members:
        if member.bot:
            continue
        # If member has activity, add the activity to the dict or add their name to the users in that category
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
    members_in_each = [len(members) for members in activities.values()]
    return activities, members_in_each


def create_pie_chart(activities, guild, members_in_each):
    """Create a pie chart representing what the members of a guild are playing."""
    fig = px.pie(names=activities.keys(), values=members_in_each,
                 title=f"Whats being played in {guild.name}?", labels={'values': 'Members Playing'},
                 template='plotly_dark')
    fig.update_traces(textposition='inside', textinfo='value+label', textfont_size=20, hoverinfo='label+percent')
    fig.update_layout(showlegend=True, title_x=0.5, titlefont_size=24)
    fig.write_image(f"images/{guild.id}.png")


async def send_visual(channel):
    """Send generated visual to the channel the bot was called in."""
    await channel.send(file=discord.File(f"images/{channel.guild.id}.png"))
    os.unlink(f"images/{channel.guild.id}.png")
