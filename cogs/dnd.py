import discord
from discord.ext import commands



class DnD(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_any_role(881569276396470303)
    async def panel(self,ctx):

        em = discord.Embed(title=f"Mute Panel",
                           color=discord.Color.from_rgb(178, 54, 95))

        react = await ctx.send(embed=em)
        
        await react.add_reaction("<:DTheShadowDragon:868926034463035434>")
        await react.add_reaction("<:DTheRainbowDragon:868926034358198283>")
        await react.add_reaction("<:DTheJulezDragon:868926034475647026>")
        await react.add_reaction("<:DTheIcyDragon:868926411266719784>")
        await react.add_reaction("<:DTheDragonFire:868926034509176853>")
        await react.add_reaction("<:BTheBeginning:868926034102345829>")
        await react.add_reaction("<:natalie:921494468031557663>")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.user_id == self.client.user.id:
            pass
        else:
            if payload.guild_id == 578446945425555464 and payload.user_id == 579395061222080563:

                guild = self.client.get_guild(578446945425555464)

                if str(payload.emoji) == "<:DTheShadowDragon:868926034463035434>":
                    Anton = guild.get_member(566667355837562881)
                    await Anton.edit(mute=True)

                if str(payload.emoji) == "<:DTheRainbowDragon:868926034358198283>":
                    Ben = guild.get_member(449922603579342858)
                    await Ben.edit(mute=True)

                if str(payload.emoji) == "<:DTheJulezDragon:868926034475647026>":
                    Julez = guild.get_member(336144182915891211)
                    await Julez.edit(mute=True)

                if str(payload.emoji) == "<:DTheIcyDragon:868926411266719784>":
                    Paul = guild.get_member(511219492332896266)
                    await Paul.edit(mute=True)

                if str(payload.emoji) == "<:DTheDragonFire:868926034509176853>":
                    Nick = guild.get_member(622130169657688074)
                    await Nick.edit(mute=True)

                if str(payload.emoji) == "<:BTheBeginning:868926034102345829>":
                    Hendrik = guild.get_member(305029907333775363)
                    await Hendrik.edit(mute=True)
                
                if str(payload.emoji) == "<:natalie:921494468031557663>":
                    Hendrik = guild.get_member(305029907333775363)
                    await Hendrik.edit(mute=True)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):

        if payload.user_id == self.client.user.id:
            pass
        else:

            if payload.guild_id == 578446945425555464 and payload.user_id == 579395061222080563:

                guild = self.client.get_guild(578446945425555464)

                if str(payload.emoji) == "<:DTheShadowDragon:868926034463035434>":
                    Anton = guild.get_member(566667355837562881)
                    await Anton.edit(mute=False)

                if str(payload.emoji) == "<:DTheRainbowDragon:868926034358198283>":
                    Ben = guild.get_member(449922603579342858)
                    await Ben.edit(mute=False)

                if str(payload.emoji) == "<:DTheJulezDragon:868926034475647026>":
                    Julez = guild.get_member(336144182915891211)
                    await Julez.edit(mute=False)

                if str(payload.emoji) == "<:DTheIcyDragon:868926411266719784>":
                    Paul = guild.get_member(511219492332896266)
                    await Paul.edit(mute=False)

                if str(payload.emoji) == "<:DTheDragonFire:868926034509176853>":
                    Nick = guild.get_member(622130169657688074)
                    await Nick.edit(mute=False)

                if str(payload.emoji) == "<:BTheBeginning:868926034102345829>":
                    Hendrik = guild.get_member(305029907333775363)
                    await Hendrik.edit(mute=False)
                    
                if str(payload.emoji) == "<:natalie:921494468031557663>":
                    Hendrik = guild.get_member(305029907333775363)
                    await Hendrik.edit(mute=False)


def setup(client):
    client.add_cog(DnD(client))