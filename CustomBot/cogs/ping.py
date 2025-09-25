import discord
from discord.ext import commands
from discord.commands import slash_command
import datetime

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def ping(self, ctx):
        ping = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Pong!",
            description="This is Sharky's ping!",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Ping", 
            value=f"{ping} ms", 
            inline=False
            )
        embed.add_field(
            name="Bot is running on", 
            value="Wollys Laptop", 
            inline=False
            )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Ping(bot))
