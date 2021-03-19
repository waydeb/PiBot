import discord
import os
from discord.ext import commands, tasks
import json
import pihole as ph
import asyncio

bot=commands.Bot(command_prefix="pi-", case_insentitive=True)
bot.remove_command('help')

with open("config.json", "r", encoding='utf-8-sig') as ff:
    conf=json.load(ff)

token=conf["token"]
@bot.event
async def on_ready():
 
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension("cogs." + filename[:-3])

    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Pi-hole on host name loler (ip loler)"))

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(bot.start(token, reconnect=True))
except KeyboardInterrupt:
    loop.run_until_complete(bot.logout())
    # cancel all tasks lingering
finally:
    loop.close()
