import discord
import os
import plotly.express as px
import plotly.graph_objects as go


class PieChart():
    def __init__(self, channel: discord.TextChannel):
        self.channel = channel
        self.guild = channel.guild
        self._get_user_activities()
        self._create_pie_chart()
        self._send_and_delete_visual()

    def _get_user_activities(self):
        """Get a list of activities being done by non-bot members in a guild."""
        activities = {'None': [], }
        for member in self.guild.members:
            if member.bot:
                continue
            # If member has activity, add the activity to the dict or add their name to the users in that category
            if member.activity:
                if member.activity.name in activities:
                    activities[member.activity.name].append(member.name)
                else:
                    activities[member.activity.name] = [member.name]
            else:
                activities['None'].append(member.name)
        members_in_each = [len(members) for members in activities.values()]
        self.activities = activities
        self.members_in_each = members_in_each

    def _create_pie_chart(self):
        """Create a pie chart representing what the members of a guild are playing. Make an annotation to show
        people who aren't playing anything"""
        members_with_no_activity = self.activities['None']
        del self.members_in_each[0]
        del self.activities['None']
        fig = px.pie(names=self.activities.keys(), values=self.members_in_each,
                     title=f"Whats being played in {self.guild.name}?", labels={'values': 'Members Playing'},
                     template='plotly_dark', color_discrete_sequence=px.colors.sequential.Purples_r)
        fig.update_traces(textposition='inside', textinfo='value+label', textfont=dict(color='white'))
        fig.update_layout(uniformtext_minsize=14, uniformtext_mode='show')
        fig.update_layout(showlegend=False, title_x=0.5, titlefont_size=18)
        fig.update_layout(margin=dict(l=20, r=20, t=80, b=60))
        fig.add_annotation(dict(font=dict(color='White', size=15),
                                x=0,
                                y=-0.12,
                                showarrow=False,
                                text=f"Members doing nothing: {len(members_with_no_activity)}",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))
        fig.write_image(f"images/{self.guild.id}.png")

    async def _send_and_delete_visual(self):
        """Send generated visual to the channel the bot was called in."""
        await self.channel.send(file=discord.File(f"images/{self.guild.id}.png"))
        os.unlink(f"images/{self.guild.id}.png")