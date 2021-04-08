import discord
import pihole as ph
import asyncio
import json
import os
from datetime import datetime
from discord.ext import commands
from .modules import sshCmd as sshModule
pihole = ph.PiHole("ip")
pihole.authenticate("password")
pihole.refresh()

class Pi(commands.Cog):

    def __init__(self, bot):
        self.bot=bot

    @commands.command(name="stats")
    async def stats(self, ctx):
        pihole.refresh()
        osbuild=await sshModule.hostbuild()
        pibuild=await sshModule.pibuild()
        embed=discord.Embed(title="Stats", description=f"```Overall Status: {pihole.status}\nBlocked 😎: {pihole.blocked}\nQueries (Without Blocked 😎): {pihole.queries}\nTotal Queries: {pihole.total_queries}\n\n```", colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Domain Count: {pihole.domain_count}\nUnique Clients/Total Clients: {pihole.unique_clients}/{pihole.total_clients}\n\n```")
        embed.add_field(name="** **", value=f"```Host Build: {osbuild}\nPi Build: {pibuild}```", inline=False)
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
            break

    @commands.command(name='startAuto')
    async def startAuto(self, ctx):
        j=pihole.top_devices
        while True:
            for u in j:
                embed=discord.Embed(title="** **", description=f"```Top Device: {u}```", colour=0xFF0000)
                embed.add_field(name="** **", value=f"```Status: {pihole.status}\n```")
                await ctx.send(embed=embed)
                await asyncio.sleep(60*5)
                break

    @commands.command(name="gravity")
    async def gravity(self, ctx, *, ued):
        if not await self.bot.is_owner(ctx.author):
            return await ctx.send("You can't use that command!")
        if ued == "-update":
            embeda=discord.Embed(title="Processing!", description="<a:loading:821989749957853215>", colour=0xFF0000)
            messageb=await ctx.send(embed=embeda)
            await sshModule.run(ctx, messageb, user=ctx.author.id)
        if ued == "-disable":
            pihole.disable(300)
            pihole.refresh()
            embed=discord.Embed(title="Gravity Status", description=f"```Gravity Disabled for 300 seconds\n{pihole.status}```", colour=0xFF0000)
            message=await ctx.send(embed=embed)
            await asyncio.sleep(300)
            pihole.enable()
            pihole.refresh()
            embed2=discord.Embed(title="Gravity Status", description=f"```Gravity re-enabled!\n{pihole.status}```", colour=0xFF0000)
            await message.edit(embed=embed)
            await ctx.send(f"<@{ctx.author.id}>")
        if ued == "-enable":
            pihole.enable()
            pihole.refresh()
            embed=discord.Embed(title="Gravity Status", description="```Gravity Enabled!\n{pihole.status}```")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Pi(bot))
