from datetime import datetime
import asyncio
import discord


hostname = "a"


async def run(ctx, messageb, user):
    start_time = datetime.now()
    p = await asyncio.create_subprocess_shell(f"ssh root@{hostname} 'pihole -g'", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await p.communicate()
    if stdout:
        embed=discord.Embed(title="Gravity Output", description=f'```{stdout.decode()[-250:]}\n\n```', colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Time Started: {start_time.replace(microsecond=0)}\nTime Ended: {datetime.now().replace(microsecond=0)}\nTime Taken: {datetime.now().replace(microsecond=0) - startTime.replace(microsecond=0)}```", inline=False)
        await messageb.edit(embed=embed)
        await messageb.reply(f'<@{user}> done!', mention_author=True)
    if stderr:
        embed=discord.Embed(title="Gravity Output", description=f'```{stderr.decode()[-250:]}\n\n```', colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Time Started: {start_time.replace(microsecond=0)}\nTime Ended: {datetime.now().replace(microsecond=0)}\nTime Taken: {datetime.now().replace(microsecond=0) - startTime.replace(microsecond=0)}```", inline=False)
        await messageb.edit(embed=embed)
        await messageb.reply(f'<@{user}> done!', mention_author=True)
    await p.wait()
