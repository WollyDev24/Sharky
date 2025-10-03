import discord
from discord.ext import commands
from discord.commands import slash_command
import os

from config import greet

class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def greet(self, ctx):
        await ctx.respond(f"Hey {ctx.author.mention}!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="Welcome!",
            description=f"Welcome to the server, {member.mention}, Be sure to check the <#1400528778509422633>, look for giveaways in <#1400527952290123828>", # replace the channel ids with your own
            color=discord.Color.blue()
        )
    
        channel = await self.bot.fetch_channel(greet)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Greet(bot))
