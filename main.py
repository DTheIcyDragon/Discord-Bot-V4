import os
import discord
import psutil as psutil
from discord.ext import commands, tasks
import settings
import time
import json
import asyncio


# definitions
def options_():
    modules = []
    
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            modules.append(discord.SelectOption(label=str(file.capitalize()[:-3])))
    
    return modules


# classes
class LoadSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Choose the cog to load",
            min_values=1,
            max_values=1,
            options=options_(),
        )
    
    async def callback(self, interaction: discord.Interaction):
        client.load_extension(f"cogs.{self.values[0].lower()}")
        
        with open("bot_data/loads.json", "r") as f:
            loads = json.load(f)
        
        loads["cogs"][self.values[0].lower()] = "1"
        
        with open("bot_data/loads.json", "w") as f:
            json.dump(loads, f, indent=4)
        
        await interaction.response.send_message(
            f"Loaded {self.values[0]}",
            ephemeral=True
        )


class LoadView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(LoadSelect())


class UnLoadSelect(discord.ui.Select):
    def __init__(self):
        options = options_()
        
        super().__init__(
            placeholder="Choose the cog to unload",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        client.unload_extension(f"cogs.{self.values[0].lower()}")
        
        with open("bot_data/loads.json", "r") as f:
            loads = json.load(f)
        
        loads["cogs"][self.values[0].lower()] = "0"
        
        with open("bot_data/loads.json", "w") as f:
            json.dump(loads, f, indent=4)
        
        await interaction.response.send_message(
            f"Unloaded {self.values[0]}",
            ephemeral=True
        )


class UnLoadView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(UnLoadSelect())


class ReLoadSelect(discord.ui.Select):
    def __init__(self):
        options = options_()
        
        super().__init__(
            placeholder="Choose the cog to Reload",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        client.unload_extension(f"cogs.{self.values[0].lower()}")
        client.load_extension(f"cogs.{self.values[0].lower()}")
        
        await interaction.response.send_message(
            f"Reloaded {self.values[0]}",
            ephemeral=True
        )


class ReLoadView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ReLoadSelect())


start_time = time.time()

client = commands.Bot(command_prefix=commands.when_mentioned_or(settings.bot_prefix),
                      intents=discord.Intents.all(),
                      strip_after_prefix=True,
                      case_insensitive=True)
client.remove_command("help")


@client.event
async def on_ready():
    print(f"""
{settings.console_colors.OKBLUE}
________________________________________________________________________________________________________________
░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░  ███╗░░░███╗░█████╗░███╗░░██╗░█████╗░░██████╗░███████╗██████╗░
██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗  ████╗░████║██╔══██╗████╗░██║██╔══██╗██╔════╝░██╔════╝██╔══██╗
╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝  ██╔████╔██║███████║██╔██╗██║███████║██║░░██╗░█████╗░░██████╔╝
░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗  ██║╚██╔╝██║██╔══██║██║╚████║██╔══██║██║░░╚██╗██╔══╝░░██╔══██╗
██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║  ██║░╚═╝░██║██║░░██║██║░╚███║██║░░██║╚██████╔╝███████╗██║░░██║
╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝  ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚═╝
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
{settings.console_colors.ENDC}
{settings.console_colors.OKGREEN}Bot's Name:{settings.console_colors.HEADER} {client.user.name}
{settings.console_colors.OKGREEN}Bot's Discriminator:{settings.console_colors.HEADER} {client.user.discriminator}
{settings.console_colors.OKGREEN}Bot's ID:{settings.console_colors.HEADER} {client.user.id}
{settings.console_colors.OKGREEN}Bot's Prefix:{settings.console_colors.HEADER} {settings.bot_prefix}
{settings.console_colors.ENDC}""")
    
    with open("bot_data/loads.json", "r") as f:
        loads = json.load(f)
    
    loads = loads["cogs"]
    # cogs to load
    for key, value in loads.items():
        if value == "1":
            client.load_extension(f"cogs.{key}")
            print(f"{settings.console_colors.OKBLUE}Loaded {key}{settings.console_colors.ENDC}")


# tasks
@tasks.loop(minutes=1)
async def change_presence():
    await client.wait_until_ready()
    while not client.is_closed():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="mit dir"))
        
        await asyncio.sleep(20)
        
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} Server"))
        
        await asyncio.sleep(20)
        
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=f"{settings.bot_prefix}help"))
        
        await asyncio.sleep(20)


change_presence.start()


@tasks.loop(minutes=1)
async def update_stats():
    await client.wait_until_ready()
    guild = client.get_guild(settings.main_guild)
    humans = client.get_channel(settings.human_count_channel)
    bots = client.get_channel(settings.bot_count_channel)
    
    await humans.edit(name=f"😃 User: {len([member for member in guild.members if not member.bot])}")
    await bots.edit(name=f"🤖 Bots: {len([member for member in guild.members if member.bot])}")


update_stats.start()


# commands
@client.command(name="cogs", help="Shows wich Cogs are loaded")
async def cogs_cmd(ctx):
    with open("bot_data/loads.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    embed = discord.Embed(title="Cog Board",
                          description="Shows wich Modules are loaded",
                          color=discord.Color.dark_red())
    for key, value in loads.items():
        embed.add_field(name=key.capitalize(), value=f'{"🟢" if value == "1" else "🔴"}')
    await ctx.reply(embed=embed)


@client.command(name="load", description="Loads a cog")
@commands.has_role(settings.mod_team)
async def load_cmd(ctx):
    await ctx.reply("Pick the cog to load:", view=LoadView())


@client.command(name="unload", description="Unloads a cog")
@commands.has_role(settings.mod_team)
async def unload_cmd(ctx):
    await ctx.reply("Pick the cog to unload:", view=UnLoadView())


@client.command(name="reload", description="Reloads a cog")
@commands.has_role(settings.mod_team)
async def unload_cmd(ctx):
    await ctx.reply("Pick the cog to reload:", view=ReLoadView())
    
    
if __name__ == "__main__":
    client.run(settings.bot_token)
