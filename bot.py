import datetime
import os
import psutil as psutil
import json
import asyncio
import logging
import platform
import subprocess
import time
import discord
from discord.ext import commands, tasks
import settings

def ping(host_or_ip, packets=1, timeout=1000):

    if platform.system().lower() == 'windows':
        command = ['ping', '-n', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=0x08000000)
        return result.returncode == 0 and b'TTL=' in result.stdout
    else:
        command = ['ping', '-c', str(packets), '-w', str(timeout), host_or_ip]
        result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0

logging.basicConfig(format="%(process)d %(levelname)s %(message)s",
                    filename="bot_data/bot.log",
                    filemode="w",
                    datefmt='%d-%b-%y %H:%M:%S'
                    )

# definitions
def options_():
    modules = []
    
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            modules.append(discord.SelectOption(label=str(file.capitalize()[:-3])))
    
    return modules
def get_prefix(client, message):
    with open("bot_data/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

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

client = commands.Bot(command_prefix = get_prefix,
                      intents = discord.Intents.all(),
                      strip_after_prefix = True,
                      case_insensitive = True)
client.remove_command("help")


@client.event
async def on_ready():
    print(f"""
{settings.console_colors.BLUE}

{settings.console_colors.RESET}
{settings.console_colors.GREEN}Bot's Name:{settings.console_colors.PURPLE} {client.user.name}
{settings.console_colors.GREEN}Bot's Discriminator:{settings.console_colors.PURPLE} {client.user.discriminator}
{settings.console_colors.GREEN}Bot's ID:{settings.console_colors.PURPLE} {client.user.id}
{settings.console_colors.GREEN}Bot's Prefix:{settings.console_colors.PURPLE} {settings.bot_prefix}
{settings.console_colors.RESET}""")
    print("It's Guilds")
    async for guild in client.fetch_guilds(limit=150):
        print(f"{settings.console_colors.YELLOW}{guild.name}{settings.console_colors.RESET}")

    with open("bot_data/loads.json", "r") as f:
        loads = json.load(f)
    
    loads = loads["cogs"]
    # cogs to load
    for key, value in loads.items():
        if value == "1":
            client.load_extension(f"cogs.{key}")
            print(f"{settings.console_colors.BLUE}Loaded {key}{settings.console_colors.RESET}")

# tasks
@tasks.loop(minutes = 1)
async def change_presence():
    await client.wait_until_ready()
    while not client.is_closed():
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "mit dir"))
        
        await asyncio.sleep(20)
        
        await client.change_presence(
            activity = discord.Activity(type = discord.ActivityType.watching, name = f"{len(client.guilds)} Server"))
        
        await asyncio.sleep(20)
        
        await client.change_presence(
            activity = discord.Activity(type = discord.ActivityType.listening, name = f"{settings.bot_prefix}help"))
        
        await asyncio.sleep(20)

change_presence.start()


@tasks.loop(minutes = 1)
async def update_stats():
    await client.wait_until_ready()
    guild = client.get_guild(settings.main_guild)
    humans = client.get_channel(settings.human_count_channel)
    bots = client.get_channel(settings.bot_count_channel)

    await humans.edit(name = f"😃 User: {len([member for member in guild.members if not member.bot])}")
    await bots.edit(name = f"🤖 Bots: {len([member for member in guild.members if member.bot])}")

update_stats.start()

@client.event
async def on_guild_join(guild):
    with open("bot_data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "//"
    with open("bot_data/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_message(msg):
    if msg.content == f"<@!{client.user.id}>":
        await msg.reply(f"My prefix is `{get_prefix(client = client, message = msg)}`")
    await client.process_commands(msg)

# commands
@client.command(name = "cogs", help = "Shows wich Cogs are loaded")
async def cogs_cmd(ctx):
    with open("bot_data/loads.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    embed = discord.Embed(title = "Cog Board",
                          description = "Shows wich Modules are loaded",
                          color = discord.Color.dark_red())
    for key, value in loads.items():
        embed.add_field(name = key.capitalize(), value = f'{"🟢" if value == "1" else "🔴"}')
    await ctx.reply(embed = embed)


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


@client.command(name = "stats", help = "Shows stats for the bot")
async def stat_cmd(ctx):
    em = discord.Embed(title = "Stats", color = discord.Color.from_rgb(18, 72, 152))
    em.add_field(name = "Ping", value = f"Latency: {round(client.latency * 1000)}ms", inline = False)
    em.add_field(name = "Uptime", value = f'Exact: <t:{int(start_time)}:f>\nRelative: <t:{int(start_time)}:R>',
                 inline = False)
    em.add_field(name = "CPU", value = f"Usage: {psutil.cpu_percent()}%", inline = False)
    em.add_field(name = "RAM", value = f"Usage: {psutil.virtual_memory()[2]}%", inline = False)
    
    await ctx.reply(embed=em)

@client.command(name = "help", description = "Help command...")
async def help_cmd(ctx):
    em = discord.Embed(title = f"Help for {ctx.author.name}")
    em.set_author(name = f"{client.user.display_name}'s help", icon_url = client.user.display_avatar)
    for command in client.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description available."
        em.add_field(name = f"`{settings.bot_prefix}{command.name}{command.signature if command.signature is not None else ''}`", value = description)
    await ctx.reply(embed=em)

@client.command(name = "test", description = "Is here for debugging/testing purposes")
@commands.has_role(901758032889929728)
async def test_cmd(ctx):
    await ctx.reply(f"I work {ctx.author.mention}")


if __name__ == "__main__":
    client.run(settings.bot_token)
