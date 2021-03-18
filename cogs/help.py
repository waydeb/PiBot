import discord
import asyncio
import json
from discord.ext import commands
from disputils import BotEmbedPaginator

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot=bot

    @commands.command(name="""help""", aliases=["""commands"""])
    async def help(self, ctx, request=None):

        
        if not request:
            embeds=[
                discord.Embed(title='''** **''', description="""**help** - You are here right now.
**stats** - Shows stats from the PiHole server
**startAuto** - Posts updates every 5 minuites""", color=0xFF0000),

                discord.Embed(title='''** **''', description="""**gravity** `<update>, <enable>, <disable>` - Allows you to preform various actions on the PiHole DNS FTL Service.
**topdevice** - Shows the top device on the network
**filter** `<add>, <remove>` - Allows you to add/remove things from the PiHole Blacklist""", color=0xFF0000)
            ]

            paginator=BotEmbedPaginator(ctx, embeds)
            await paginator.run()




def setup(bot):
    bot.add_cog(Help(bot))
