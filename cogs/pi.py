import discord
import pihole as ph
import asyncio
from threading import Thread
import json
import os
from discord.ext import commands
pihole = ph.PiHole("your host name here")
pihole.authenticate("you password here")
hostname="ip prefered here"
pihole.refresh()
pihole.refreshTop(1)
time=60*5
async def run(ctx, messageb):
    p = await asyncio.create_subprocess_shell(f"ssh root@{hostname} pihole -g", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await p.communicate()
    if stdout:
        embed=discord.Embed(title="Gravity Output", description=f'```{stdout.decode()[-200:]}```', colour=0xFF0000)
        await messageb.edit(embed=embed)
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    beans=stdout.decode()
    await p.wait()

class Pi(commands.Cog):
    

    def __init__(self, bot):
        self.bot=bot

    @commands.command(name="stats")
    async def stats(self, ctx):
        embed=discord.Embed(title="Stats", description=f"```Overall Status: {pihole.status}\nBlocked 😎: {pihole.blocked}\nQueries (Without Blocked 😎): {pihole.queries}\nTotal Queries: {pihole.total_queries}\n\n```", colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Domain Count: {pihole.domain_count}\nUnique Clients/Total Clients: {pihole.unique_clients}/{pihole.total_clients}```")
        await ctx.send(embed=embed)

    @commands.command(name="fliter")
    async def filter(self, ctx, *, adrm, domain):
        if adrm == "add":
            pihole.add("black", f"{domain}")
            embed=discord.Embed(title="Blacklist add", description=f"Domain `{domain}` has been added to the blacklist!", colour=0xFF0000)
            await ctx.send(embed=embed)
        if adrm == "remove":
            pihole.sub("black", f"{domain}")
            embed=discord.Embed(title="Blacklist remove", description=f"Domain `{domain}` has been removed from the blacklist!", colour=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name="topdevice")
    async def topdevice(self, ctx):
        j=pihole.top_devices
        for u in j:
            embed=discord.Embed(title="Top Device", description=f"```{u}```", colour=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='startAuto')
    async def startAuto(self, ctx, ):
        j=pihole.top_devices
        while True:
            for u in j:
                embed=discord.Embed(title="** **", description=f"```Top Device: {u}```", colour=0xFF0000)
                embed.add_field(name="** **", value=f"```Status: {pihole.status}\n```")
                await ctx.send(embed=embed)
                await asyncio.sleep(60*5)
                break

    @commands.command(name="gravity")
    async def gravity(self, ctx, *, ued, **, time):
        if not await self.bot.is_owner(ctx.author):
            return await ctx.send("You can't use that command!")
        if ued == "update":
            embeda=discord.Embed(title="Processing!", description="<a:loading:821989749957853215>", colour=0xFF0000)
            messageb=await ctx.send(embed=embeda)
            await run(ctx, messageb)
        if ued == "disable":
            pihole.disable(300)
            pihole.refresh()
            embed=discord.Embed(title="Gravity Status", description=f"```Gravity Disabled for {time} seconds\n{pihole.status}```", colour=0xFF0000)
            message=await ctx.send(embed=embed)
            asyncio.sleep(300)
            pihole.refresh()
            embed2=discord.Embed(title="Gravity Status", description=f"```Gravity re-enabled!\n{pihole.status}```", colour=0xFF0000)
            await message.edit(content=f"<@{ctx.author.id}>", embed=embed)
        if ued == "enable":
            pihole.enable()
            pihole.refresh()
            embed=discord.Embed(title="Gravity Status", description="```Gravity Enabled!\n{pihole.status}```")
            await ctx.send(embed=emed)


def setup(bot):
    bot.add_cog(Pi(bot))