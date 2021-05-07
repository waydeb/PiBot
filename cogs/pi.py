import discord
from discord_slash import cog_ext, SlashContext
import pihole as ph
import asyncio
import os
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
from .modules import sshCmd as sshModule

pihole = ph.PiHole("a")
pihole.authenticate("a")
pihole.refresh()
ip="a"

class Pi(commands.Cog):

    def __init__(self, bot):
        self.bot=bot

    @cog_ext.cog_slash(name="stats", guild_ids=[your serverid], description="Pihole Stats")
    async def stats(self, ctx):
        pihole.refresh()
        osbuild=os.popen("uname -a").read()
        pibuild=os.popen(f"ssh root@{ip} 'uname -a'").read()
        embed=discord.Embed(title="Stats", description=f"```Overall Status: {pihole.status}\nBlocked 😎: {pihole.blocked}\nQueries (Without Blocked 😎): {pihole.queries}\nTotal Queries: {pihole.total_queries}\n\n```", colour=0xFF0000)
        embed.add_field(name="** **", value=f"```Domain Count: {pihole.domain_count}\nUnique Clients/Total Clients: {pihole.unique_clients}/{pihole.total_clients}\n\n```")
        embed.add_field(name="** **", value=f"```Host Build: {osbuild}\nPi Build: {pibuild}```", inline=False)
        await ctx.send(embed=embed)


    @cog_ext.cog_subcommand(base="filter", name="add", guild_ids=[your serverid], description="Adds a domain to the blacklist")
    async def filter_add(self, ctx, domain):
        pihole.add("black", f"{domain}")
        embed=discord.Embed(title="Blacklist add", description=f"Domain `{domain}` has been added to the blacklist!", colour=0xFF0000)
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="filter", name="remove", guild_ids=[your serverid], description="Removes a domain from the blacklist")
    async def filter_remove(self, ctx, domain):
        pihole.sub("black", f"{domain}")
        embed=discord.Embed(title="Blacklist remove", description=f"Domain `{domain}` has been removed from the blacklist!", colour=0xFF0000)
        await ctx.send(embed=embed)


    @cog_ext.cog_slash(name="topdevice", guild_ids=[your serverid], description="Top device")
    async def topdevice(self, ctx):
        j=pihole.top_devices
        for u in j:
            embed=discord.Embed(title="Top Device", description=f"```{u}```", colour=0xFF0000)
            await ctx.send(embed=embed)
            break

    @cog_ext.cog_slash(name="startAuto", guild_ids=[your serverid], description="Auto posting")
    async def start_auto(self, ctx):
        j=pihole.top_devices
        while True:
            for u in j:
                embed=discord.Embed(title="** **", description=f"```Top Device: {u}```", colour=0xFF0000)
                embed.add_field(name="** **", value=f"```Status: {pihole.status}\n```")
                await ctx.send(embed=embed)
                await asyncio.sleep(60*5)
                break

    @cog_ext.cog_subcommand(base="gravity", name="update", guild_ids=[your serverid], description="Pihole Graivty Update")
    async def gravity_update(self, ctx):
        embeda=discord.Embed(title="Processing!", description="<a:loading:821989749957853215>", colour=0xFF0000)
        messageb=await ctx.send(embed=embeda)
        await sshModule.run(ctx, messageb, user=ctx.author.id)

    @cog_ext.cog_subcommand(base="gravity", name="disable", guild_ids=[your serverid], description="Pihole Gravity Disable")
    async def gravity_disable(self, ctx):
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

    @cog_ext.cog_subcommand(base="gravity", name="enable", guild_ids=[your serverid], description="Pihole Gravity Enable")
    async def gravity_enable(self, ctx):
        pihole.enable()
        pihole.refresh()
        embed=discord.Embed(title="Gravity Status", description=f"```Gravity Enabled!\n{pihole.status}```")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Pi(bot))