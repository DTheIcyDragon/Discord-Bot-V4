"""
_______________________________________________________________
░██████╗███████╗████████╗████████╗██╗███╗░░██╗░██████╗░░██████╗
██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗░██║██╔════╝░██╔════╝
╚█████╗░█████╗░░░░░██║░░░░░░██║░░░██║██╔██╗██║██║░░██╗░╚█████╗░
░╚═══██╗██╔══╝░░░░░██║░░░░░░██║░░░██║██║╚████║██║░░╚██╗░╚═══██╗
██████╔╝███████╗░░░██║░░░░░░██║░░░██║██║░╚███║╚██████╔╝██████╔╝
╚═════╝░╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░╚══╝░╚═════╝░╚═════╝░
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
"""
#tokens

bot_prefix = "!"
bot_token = ""
spotify_id = ""
spotify_secret = ""
# roles
mod_team = 876927201390522429                       #mod roll (general team role)
verified = 876927534904803398                       #roll for the basic role

# channel
dm_output_channel = 876921062602985533              #where should all direct messages of the bot be received
log_channel = 911216017433325578                    #channel for logging of mod actions
welcome_channel = 705800487517028493                #rules or any channel everyone can see.

human_count_channel = 878401877715329064            #stats channel
bot_count_channel = 878401060069339207

# guilds
main_guild = 578446945425555464                     #guild where your bot is located


# ignore
class console_colors:
    PURPLE = '\033[95m'  # purple
    BLUE = '\033[94m'  # blue
    GREEN = '\033[92m'  # green
    YELLOW = '\033[93m'  # light_yellow
    RED = '\033[91m'  # light_red
    RESET = '\033[0m'  # "Normal" color
    BOLD = '\033[1m'  # Bold
    UNDERLINE = '\033[4m'  # Underline

import discord
def error_em(name, pfp, error):
    error_em = discord.Embed(description = error, color = discord.Color.dark_red())
    error_em.set_author(name = name)
    error_em.set_thumbnail(url = pfp)
    return error_em
