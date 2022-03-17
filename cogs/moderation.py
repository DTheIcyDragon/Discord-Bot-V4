import datetime
import json
from typing import Optional

import discord
from discord.ext import commands

import settings


# Defenitionen


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "clear", help = "Clear's messages in channels", aliases = ["purge"])
    @commands.has_any_role(settings.mod_team)
    async def clear_cmd(self, ctx, amount:Optional[int]):
        amount = amount or 100
        await ctx.channel.purge(limit = amount)
        em = discord.Embed(color = discord.Color.nitro_pink())
        em.set_author(name = f"Cleared by {ctx.author.display_name}", icon_url = ctx.author.display_avatar)
        await ctx.send(embed = em, delete_after = 300)

    @clear_cmd.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(settings.error_em(name = ctx.author.display_name,
                                             pfp = ctx.author.display_avatar,
                                             error = "You don't have the Permission to execute this command."))
        else:
            pass


    @commands.group(pass_context = True, case_insensitive = True)
    async def send(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(settings.error_em(name=ctx.author.display_name,
                                              pfp =ctx.author.display_avatar,
                                              error= "Please use 'send Embed' or 'send Message'"))
    
    @send.command(name = "embed", description = "Sends an Embed into a Channel")
    async def embed_cmd(self, ctx, channel:discord.TextChannel, *, message):
        em = discord.Embed(description=message)
        em.set_author(name = ctx.author, icon_url = ctx.author.display_avatar)
        channel = self.client.get_channel(channel.id)
        await channel.send(embed = em)

    @send.command(name = "message", description = "Sends an message into a Channel")
    async def message_cmd(self, ctx, channel:discord.TextChannel, *, message):
        channel = self.client.get_channel(channel.id)
        await channel.send(message)

    @commands.command(name = "kick", help = "Kicks a member from the Guild but sends an invite")
    @commands.has_any_role(settings.mod_team)
    async def kick_cmd(self, ctx, member: discord.Member, *, reason):
        invite_channel = self.client.get_channel(settings.welcome_channel)
        link = await invite_channel.create_invite(max_uses=1, max_age=0)
        try:
            em = discord.Embed(description = f"You were kicked from {ctx.guild.name} because {reason}.\n{link}", color = discord.Color.brand_red())
            await member.send(embed = em)
        except:
            pass
        await member.kick(reason=reason)
        em = discord.Embed(title = "**Kick**", description = f"Reason: **{reason}**", color = discord.Color.brand_red())
        em.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar)
        em.add_field(name = "Moderator", value = ctx.author.mention)
        em.add_field(name = "Member", value = member.mention)
        channel = self.client.get_channel(settings.log_channel)
        await ctx.send(embed = em)
        await channel.send(embed = em)

    @commands.command(name = "ban", help = "Bans a member from the Guild but sends an invite")
    @commands.has_any_role(settings.mod_team)
    async def ban_cmd(self, ctx, member: discord.Member, *, reason):
        await member.kick(reason=reason)
        em = discord.Embed(title = "**Kick**", description = f"Reason: **{reason}**", color = discord.Color.brand_red())
        em.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar)
        em.add_field(name = "Moderator", value = ctx.author.mention)
        em.add_field(name = "Member", value = member.mention)
        channel = self.client.get_channel(settings.log_channel)
        await ctx.send(embed = em)
        await channel.send(embed = em)


    @commands.command(name = "timeout", help = "Timeouts a member")
    @commands.has_any_role(settings.mod_team)
    async def timeout_cmd(self, ctx, member: discord.Member, duration, *, reason):
        try:
            duration = duration.content.replace(",", ".")
        except:
            pass
        if duration.endswith("s"):
            delta = datetime.timedelta(seconds=float(duration[:-1]))
            await member.timeout_for(duration=delta)
        if duration.endswith("m"):
            delta = datetime.timedelta(minutes=float(duration[:-1]))
            await member.timeout_for(duration=delta)
        if duration.endswith("h"):
            delta = datetime.timedelta(hours=float(duration[:-1]))
            await member.timeout_for(duration=delta)
        if duration.endswith("d"):
            delta = datetime.timedelta(days=float(duration[:-1]))
            await member.timeout_for(duration=delta)
        if duration.endswith("w"):
            if float(duration[:-1]) > 4:
                delta = datetime.timedelta(weeks=int(duration[:-1]))
                await member.timeout_for(duration=delta)
    
        em = discord.Embed(title = "**Timeout**", description = f"Reason: **{reason}**", color = discord.Color.brand_red())
        em.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar)
        em.add_field(name = "Moderator", value = ctx.author.mention)
        em.add_field(name = "Member", value = member.mention)
        channel = self.client.get_channel(settings.log_channel)
        await ctx.send(embed = em)
        await channel.send(embed = em)
        
    @commands.command(name="register", help = "Registers the guild to work on.")
    @commands.has_any_role(settings.mod_team)
    async def register_cmd(self, ctx):
        with open("bot_data/data/channel_exceptions.json", "r") as r:
            loads = json.load(r)
        with open("bot_data/data/channel_exceptions.json", "w") as w:
            for channel in ctx.guild.channels:
                if channel.type == discord.ChannelType.text:
                    loads[str(channel.id)] = "0"
            json.dump(loads, w, indent=4)

            em = discord.Embed(color=discord.Color.yellow())
            em.set_author(name=f"{ctx.author.display_name} registered this guild for the lockdown.",
                          icon_url=ctx.author.display_avatar)
            em.add_field(name="Text Channels", value=len(
                [channel for channel in ctx.guild.channels if channel.type == discord.ChannelType.text]))

            await ctx.reply(embed=em)

    @commands.command(name = "exclude_channel", help = "Adds a channel that won't be unlocked")
    @commands.has_any_role(settings.mod_team)
    async def exclude_channel_add_cmd(self, ctx, channel: discord.TextChannel):
        with open("bot_data/data/channel_exceptions.json", "r") as f:
            loads = json.load(f)
        with open("bot_data/data/channel_exceptions.json", "w") as w:
            loads[str(channel.id)] = "1"
            json.dump(loads, w, indent = 4)
            em = discord.Embed(color=discord.Color.yellow())
            em.set_author(name = f"{ctx.author.display_name} removed {channel.name} from the unlock.", icon_url=ctx.author.display_avatar)
            await ctx.reply(embed = em)

    @commands.command(name = "shutdown", help = "Shuts all text channel")
    @commands.has_any_role(settings.mod_team)
    async def lock_cmd(self, ctx):
        role = ctx.guild.get_role(settings.verified)
        lock = []
        for channel in ctx.guild.channels:
            if channel.type == discord.ChannelType.text:
                perms = channel.overwrites_for(role)
                perms.send_messages = False
                await channel.set_permissions(role, overwrite = perms, reason = "🔒 Lockdown")
                lock.append(channel.mention)
        em = discord.Embed(description = f"\n".join(lock), color = discord.Color.green())
        em.set_author(name = f"🔒 Server lockdown by {ctx.author.display_name} 🔒", icon_url = ctx.author.display_avatar)
        await ctx.reply(embed = em)

    @commands.command(name="unlock", help = "Unlocks all text channel")
    @commands.has_any_role(settings.mod_team)
    async def unlock_cmd(self, ctx):
        role = ctx.guild.get_role(settings.verified)
        lock = []
        with open("bot_data/data/channel_exceptions.json", "r") as f:
            loads = json.load(f)
        for channel in ctx.guild.channels:
            if channel.type == discord.ChannelType.text:
                for key, value in loads.items():
                    if value == "1":
                        pass
                    else:
                        perms = channel.overwrites_for(role)
                        perms.send_messages = True
                        await channel.set_permissions(role, overwrite=perms, reason="🔓 Unlock")
                        lock.append(channel.mention)
        em = discord.Embed(description=f"\n".join(lock), color=discord.Color.green())
        em.set_author(name=f"🔓 Server unlocked by {ctx.author.display_name} 🔓",
                      icon_url=ctx.author.display_avatar)
        await ctx.reply(embed=em)

def setup(client):
    client.add_cog(Moderation(client))
