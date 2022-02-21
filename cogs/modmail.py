import discord
from discord.ext import commands

#Defenitionen
import settings


class modmail(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_message(self, msg):
        if isinstance(msg.channel, discord.DMChannel):
            if msg.author.id != self.client.user.id:
                channel = self.client.get_channel(settings.dm_output_channel)
                if len(msg.attachments) == 0:
                    em = discord.Embed(description=msg.content, color = discord.Color.dark_purple())
                    em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                    em.set_footer(text=msg.author.id)
                    em.set_thumbnail(url = msg.author.display_avatar)
                    await channel.send(embed = em)

                if len(msg.attachments) > 0:
                    for attachment in msg.attachments:
                        picture_em = discord.Embed(description = msg.content, color = discord.Color.dark_purple())
                        picture_em.set_author(name = msg.author, icon_url = msg.author.display_avatar)
                        picture_em.set_image(url = attachment.url)
                        await channel.send(embed = picture_em)


    @commands.command(name = "message", description = "Messages a given member", aliases = ["msg"])
    @commands.has_any_role(settings.mod_team)
    async def message_cmd(self, ctx, member: discord.Member, *, msg):
        #sends a dm to a member
        guild = self.client.get_guild(ctx.guild.id)
        member = guild.get_member(member.id)

        em = discord.Embed(description=msg, color=discord.Color.dark_purple())
        em.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}")
        em.set_footer(text=ctx.author.id)
        em.set_thumbnail(url=ctx.author.display_avatar)

        await member.send(embed = em)
        success_em = discord.Embed(title = f"Successfully delivered this message to {member.display_name}", description = msg, color= discord.Color.from_rgb(232, 23, 230))
        await ctx.reply(embed = success_em)


    @commands.command(name = "Tagesprophet", description = "Schickt den Tagespropheten in <#883967458497691658>")
    @commands.is_owner()
    async def news_cmd(self, ctx, content):
        channel = await self.client.get_channel(883967458497691658)
        webhook = discord.Webhook.from_url("https://discord.com/api/webhooks/941403876064653342/dJxx4YGqgQa_I-yA-u4pN-KHXtFe1hPvni5bsz0qO2aNzvejJWBV_Wu9wu8dwUUaSaZy")
        msg = await webhook.send(content)
        await ctx.reply(f"[Done]({msg.jump_url})")
        
def setup(client):
    client.add_cog(modmail(client))
