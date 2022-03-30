import secrets
import string
import time

import discord
from discord.ext import commands


# Defenitionen
import settings


class Utilitie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "userinfo", help = "Displays information about a user", aliases=["uinfo"])
    async def userinfo_cmd(self,ctx , member : discord.Member):

        joined_at = member.joined_at
        joined_at.timestamp()
        joined_at = (time.mktime(joined_at.timetuple()))

        created_at = member.created_at
        created_at.timestamp()
        created_at = (time.mktime(created_at.timetuple()))

        em = discord.Embed(title=f"Userinfo für {member.display_name}", color=discord.Color.from_rgb(235, 73, 238))
        em.add_field(name=f"Name", value=f"{member.name}", inline=False)
        em.add_field(name=f"ID", value=f"{member.id}", inline=False)
        em.add_field(name=f"Erstellungsdatum", value=f"<t:{int(created_at)}:F>", inline=False)
        em.add_field(name="Beigetreten", value=f"<t:{int(joined_at)}:F>")
        em.add_field(name=f"Bot", value=f"{'Ja' if member.bot else 'Nein'}", inline=False)
        em.set_thumbnail(url=member.display_avatar)
        await ctx.send(embed=em)

    @commands.command(name = "password", description = "generates a 'safe' password", aliases=["pwd"])
    async def password_cmd(self, ctx):
        (secrets.choice("ab"))
        (secrets.token_bytes())
        (secrets.token_urlsafe())
        chars = string.digits + string.ascii_letters
        (len(chars))
        gen_password = (''.join(secrets.choice(chars) for _ in range(40)))

        em = discord.Embed(
            description=gen_password + "\n [You can check it strength here](http://rumkin.com/tools/password/passchk.php)\n"
                                       "[Or here](https://checkdeinpasswort.de/)\n Non of these Websites are affiliated with me in any way",
            color=discord.colour.Color.greyple())
        await ctx.author.send(embed=em)

    @commands.command(aliases=["vorschlag", "suggest"])
    @commands.has_role(settings.verified)
    async def suggestion(self, ctx, *, message):
        em = discord.Embed(title = f"Suggestion from {ctx.author.display_name}\n{ctx.author.id}",
                           description=f"{message}",
                           color= discord.Color.dark_blue())
        channel = self.client.get_channel(settings.dm_output_channel)
        await channel.send(embed = em)
        em = discord.Embed(title="Your suggestion has been sent to get viewed by the team!")
        await ctx.author.send(embed = em)

def setup(client):
    client.add_cog(Utilitie(client))
