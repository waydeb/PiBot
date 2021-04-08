from datetime import datetime
import asyncio
import os
import discord
hostname="ip"

async def run(ctx, messageb, user):
    startTime=datetime.now()
    p = await asyncio.create_subprocess_shell(f"ssh root@{hostname} 'pihole -g'", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await p.communicate()
    if stdout:
        embed=discord.Embed(title="Gravity Output", description=f'```{stdout.decode()[-250:]}\n\n```', colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Time Started: {startTime.replace(microsecond=0)}\nTime Ended: {datetime.now().replace(microsecond=0)}\nTime Taken: {datetime.now().replace(microsecond=0) - startTime.replace(microsecond=0)}```", inline=False)
        await messageb.edit(embed=embed)
        await messageb.reply(f'<@{user}> done!', mention_author=True)
    if stderr:
        embed=discord.Embed(title="Gravity Output", description=f'```{stderr.decode()[-250:]}\n\n```', colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Time Started: {startTime.replace(microsecond=0)}\nTime Ended: {datetime.now().replace(microsecond=0)}\nTime Taken: {datetime.now().replace(microsecond=0) - startTime.replace(microsecond=0)}```", inline=False)
        await messageb.edit(embed=embed)
        await messageb.reply(f'<@{user}> done!', mention_author=True)
    await p.wait()

async def pibuild():
    pibuild = os.popen(f"ssh root@{hostname} 'uname -a'").read()

async def hostbuild():
    osbuild = os.popen("uname -a").read()