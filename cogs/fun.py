import asyncio
import random

import discord
from discord.ext import commands

import settings


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name = "punish", description = "Punish someone for anything")
    @commands.has_role(settings.mod_team)
    async def punish_cmd(self, ctx, member: discord.Member, *, reason = "for no reason"):
        em = discord.Embed()
        em.set_author(name = f"{ctx.author.display_name} punished {member} {reason}", icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em)
        
    @commands.command(name = "slap", description = "Slap someone for anything")
    @commands.has_role(settings.mod_team)
    async def slap_cmd(self, ctx, member: discord.Member, *, reason = "for no reason"):
        em = discord.Embed()
        em.set_author(name = f"{ctx.author.display_name} slapped {member} {reason}", icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em)
        
    @commands.command(name = "kill", description = "Kill someone for anything")
    @commands.has_role(settings.mod_team)
    async def kill_cmd(self, ctx, member: discord.Member, *, reason = "for no reason"):
        em = discord.Embed()
        em.set_author(name = f"{ctx.author.display_name} killed {member} {reason}", icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em)
        
    @commands.command(name = "bonk", description = "Bonk someone for anything")
    @commands.has_role(settings.mod_team)
    async def punish_cmd(self, ctx, member: discord.Member):
        em = discord.Embed()
        em.set_author(name = f"{ctx.author.display_name} send {member.display_name} to horny jail", icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em)

    @commands.command(name = "guess", description = "Guess a number game")
    async def guess_cmd(self, ctx):
        rand1 = random.randint(0, 37)
        rand2 = random.randint(63, 100)
        guess_answer = random.randint(rand1, rand2)
        #    print(guess_answer)
        em = discord.Embed(title="Guess",
                           description="Guess a number between " + str(rand1) + " and " + str(rand2) + ".",
                           color=discord.Color.dark_green())
        await ctx.send(embed=em)
    
        def is_correct_guess(m):
            return m.author == ctx.author and m.content.isdigit()
    
        try:
            user_guess = await self.client.wait_for('message', check=is_correct_guess, timeout=10.0)
        except asyncio.TimeoutError:
            em = discord.Embed(title="Timed Out",
                               description=f'Your guess took too long the correct was answer was {guess_answer}',
                               color=discord.Color.dark_green())
            return await ctx.channel.send(embed=em)
    
        if int(user_guess.content) == guess_answer:
            em = discord.Embed(title="Correct", description="You guessed right.", color=0xff0000)
            await ctx.channel.send(embed=em)
    
        else:
            em = discord.Embed(title="You were Wrong", description="Correct was "f'{guess_answer}', color=0xe81717)
            await ctx.channel.send(embed=em)

    @commands.command(name = "8ball", description = "Asks the 8Ball")
    async def _8ball_cmd(self, ctx, *, question):
        ball_choices = [" It is certain.", " It is decidedly so.", " Without a doubt.", " Yes – definitely.",
                        "You may rely on it.",
                        " As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
                        "Reply hazy, try again.",
                        "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                        "Concentrate and ask again.",
                        "Don’t count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                        "Very doubtful."]
    
        ball_choice = random.choice(ball_choices)
        em = discord.Embed(description=f"**Question:** {question}\n **" + ball_choice + "**",
                           color=discord.Color.dark_green())

        await ctx.send(embed=em)

    @commands.command(name = "roll", description = "Rolls a dice", aliases = ["dice"])
    async def roll_cmd(self, ctx, dice_size=6, trows=1):
        answer = []
        for i in range(int(trows)):
            choice = random.randint(1, int(dice_size))
            answer.append(choice)

        em = discord.Embed(description=answer, color=discord.Color.dark_green())
        em.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Fun(client))