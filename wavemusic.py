import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify

import settings


def sec_to_min(time):
    hours, seconds = divmod(time, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    return str(hours) + "h " + str(minutes) + "m " + str(int(seconds)) + "s"
    
class Wavemusic(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.client.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.client,
                                            host='lavalink.cobaltonline.net',
                                            port=443,
                                            password='cobaltlavanode23@',
                                            https=True,
                                            spotify_client=spotify.SpotifyClient(client_id=settings.spotify_id,
                                                                                 client_secret=settings.spotify_secret))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')
            

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason):
        if not player.queue.is_empty:

            new = player.queue.get()
            await player.play(new)
        else:
            await player.stop()

    @commands.command()
    async def yplay(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        
        embed = discord.Embed(title = f"<a:spinningdisk:946162435432251442> Searching track",
                              color = discord.Color.blue())
        msg = await ctx.reply(embed = embed)
        
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.set_volume(10)
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            playing_em = discord.Embed(title=search.title,
                                       url=search.uri,
                                       description=f"Author: {search.author}\nDuration: {sec_to_min(search.duration)}",
                                       color=discord.Color.fuchsia())
            playing_em.set_author(name="Now playing")
            playing_em.set_image(url=search.thumbnail)
            await msg.edit(embed=playing_em)
        else:
            await vc.queue.put_wait(search)
            playing_em = discord.Embed(title=search.title,
                                       url=search.uri,
                                       description=f"Author: {search.author}\nDuration: {sec_to_min(search.duration)}",
                                       color=discord.Color.fuchsia())
            playing_em.set_author(name="Queued")
            playing_em.set_image(url=search.thumbnail)
            await msg.edit(embed=playing_em)

    @commands.command()
    async def splay(self, ctx: commands.Context, *, search: spotify.SpotifySearchType.track):
    
        embed = discord.Embed(title=f"<a:spinningdisk:946162435432251442> Searching track",
                              color=discord.Color.blue())
        msg = await ctx.reply(embed=embed)
    
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
    
        await vc.set_volume(10)
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            playing_em = discord.Embed(title=search.title,
                                       url=search.uri,
                                       description=f"Author: {search.author}\nDuration: {sec_to_min(search.duration)}",
                                       color=discord.Color.fuchsia())
            playing_em.set_author(name="Now playing")
            playing_em.set_image(url=search.thumbnail)
            await msg.edit(embed=playing_em)
        else:
            await vc.queue.put_wait(search)
            playing_em = discord.Embed(title=search.title,
                                       url=search.uri,
                                       description=f"Author: {search.author}\nDuration: {sec_to_min(search.duration)}",
                                       color=discord.Color.fuchsia())
            playing_em.set_author(name="Queued")
            playing_em.set_image(url=search.thumbnail)
            await msg.edit(embed=playing_em)

    @commands.command()
    async def disconnect(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        em = discord.Embed(description = f"Disconnected from <#{ctx.author.voice.channel.id}>")
        await ctx.reply(embed=em)
        
    @commands.command()
    async def volume(self, ctx, volume: int):
        vc: wavelink.Player = ctx.voice_client
        if volume < 1 or volume > 100:
            await ctx.reply(settings.error_em(name=ctx.author.display_name,
                                              pfp=ctx.author.display_avatar,
                                              error="Volume can't be below 1 or over 100"))
        else:
            await vc.set_volume(volume)

def setup(bot):
    bot.add_cog(Wavemusic(bot))
