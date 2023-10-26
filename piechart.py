import discord
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO


class ActivityChart:
    def __init__(self, channel: discord.TextChannel):
        self.channel = channel
        self.guild = channel.guild
        self._get_guild_data()
        self._create_visual()
        self._im_to_bytesio()

    def _get_guild_data(self):
        """Get the data we'll be using for the visual."""
        self.activities = {'None': [], }
        for member in self.guild.members:
            if member.bot:
                continue
            # If member has activity, add the activity to the dict or add their name to the users in that category
            if member.activity:
                if member.activity.name in self.activities:
                    self.activities[member.activity.name].append(member.name)
                else:
                    self.activities[member.activity.name] = [member.name]
            else:
                self.activities['None'].append(member.name)
        self.members_in_each = [len(members) for members in self.activities.values()]

    def _create_visual(self):
        """Create a visual representation of the data gathered. Left empty in parent class, this is the only method
        that must be added in a child class to define the type of chart created."""
        ...

    def _im_to_bytesio(self):
        """Turn the fig created into a BytesIO object, for passing into discord.File()"""
        self.image = BytesIO(self.fig.to_image(format='PNG'))


class PieChart(ActivityChart):
    """Represents a Pie Chart for a given discord guild's activity. Use the image attribute to access a bytesIO object or .fig for the plotly figure"""
    def __init__(self, channel: discord.TextChannel):
        super().__init__(channel)

    def _create_visual(self):
        """Create a pie chart representing what the members of a guild are playing. Make an annotation to show
                people who aren't playing anything"""
        self.members_with_no_activity = self.activities['None']
        del self.members_in_each[0]
        del self.activities['None']
        self.fig = px.pie(names=self.activities.keys(),
                          values=self.members_in_each,
                          title=f"Whats being played in {self.guild.name}?",
                          template='plotly_dark',
                          color_discrete_sequence=px.colors.sequential.Purples_r)
        self.fig.update_traces(textposition='inside', textinfo='value+label', textfont=dict(color='white'))
        self.fig.update_layout(uniformtext_minsize=14,
                               uniformtext_mode='show',
                               showlegend=False,
                               title_x=0.5,
                               titlefont_size=18,
                               margin=dict(l=20, r=20, t=80, b=60))
        self.fig.add_annotation(dict(font=dict(color='White', size=15),
                                     x=0,
                                     y=-0.12,
                                     showarrow=False,
                                     text=f"Members doing nothing: {len(self.members_with_no_activity)}",
                                     textangle=0,
                                     xanchor='left',
                                     xref="paper",
                                     yref="paper"))


class BarChart(ActivityChart):
    """Create a pie chart representing what the members of a guild are playing. Make an annotation to show
            people who aren't playing anything"""
    def __init__(self, channel):
        super().__init__(channel)

    def _create_visual(self):
        """Create a pie chart representing what the members of a guild are playing. Make an annotation to show
                people who aren't playing anything"""
        self.members_with_no_activity = self.activities['None']
        del self.members_in_each[0]
        del self.activities['None']
        self.fig = px.bar(x=self.activities.keys(),
                          y=self.members_in_each,
                          title=f"Whats being played in {self.guild.name}?",
                          template='plotly_dark',
                          color_discrete_sequence=px.colors.sequential.Purples_r)
        self.fig.update_layout(uniformtext_minsize=14,
                               uniformtext_mode='show',
                               showlegend=False,
                               title_x=0.5,
                               titlefont_size=18,
                               margin=dict(l=20, r=20, t=80, b=100))
        self.fig.add_annotation(dict(font=dict(color='White', size=15),
                                     x=0,
                                     y=-0.4,
                                     showarrow=False,
                                     text=f"Members doing nothing: {len(self.members_with_no_activity)}",
                                     textangle=0,
                                     xanchor='left',
                                     xref="paper",
                                     yref="paper"))
