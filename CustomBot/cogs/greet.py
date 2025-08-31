import discord
from discord.ext import commands
from discord.commands import slash_command


class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def greet(self, ctx):
        await ctx.respond(f"Hey {ctx.author.mention}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="Welcome!",
            description=f"Welcome to the server, {member.mention}!",
            color=discord.Color.blue()
        )
    
        channel = await self.bot.fetch_channel(1400531849008386170) # Replace with our own channel id
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Greet(bot))