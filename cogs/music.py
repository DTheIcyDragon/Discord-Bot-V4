import discord
from discord.ext import commands

# Defenitionen
import settings


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    


def setup(client):
    client.add_cog(Music(client))