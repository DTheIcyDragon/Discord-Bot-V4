import discord
from discord.ext import commands
import json


async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
        users[str(user.guild.id)][str(user.id)]['level'] = lvl_end

class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "level", help = "Show's the level and xp of a user.", aliases=['rank', 'lvl'])
    async def level(self, ctx, member: discord.Member = None):

        if not member:
            user = ctx.message.author
            with open('bot_data/data/level.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']
        
            embed = discord.Embed(title=f'Level {lvl}', description=f"{exp} XP ", color=discord.Color.green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed)
        else:
            with open('bot_data/data/level.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(member.id)]['level']
            exp = users[str(ctx.guild.id)][str(member.id)]['experience']
            embed = discord.Embed(title=f'Level {lvl}', description=f"{exp} XP", color=discord.Color.green())
            embed.set_author(name=member, icon_url=member.display_avatar)
        
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open('bot_data/data/level.json', 'r') as f:
                users = json.load(f)
            await update_data(users, message.author, message.guild)
            await add_experience(users, message.author, 4, message.guild)
            await level_up(users, message.author, message.channel, message.guild)

            with open('bot_data/data/level.json', 'w') as f:
                json.dump(users, f, indent=4)

def setup(bot):
    bot.add_cog(Level(bot))
