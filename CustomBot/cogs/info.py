import discord
from discord.ext import commands
from discord.commands import slash_command


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Information and Changelog")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Info and Changelog",
            description="",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Website",
            value="[Sharky Website](https://wollydev24.github.io/sharky)", 
            inline=False
        )
        embed.add_field(
            name="Version", 
            value="V2.7.1", 
            inline=True
            )
        embed.add_field(
            name="Relase Type", 
            value="Stable", 
            inline=True
            )
        embed.add_field(
            name="Developer", 
            value="[WollyDev24](https://github.com/WollyDev24)", 
            inline=False
            )
        embed.add_field(
            name="Github", 
            value="[Github Repo](https://github.com/WollyDev24/Sharky/)", 
            inline=False
            )
        embed.add_field(
            name="Newest Update", 
            value=" - Update check got better and now forces one if it doesnt succed at first\n - Bot now restarts automatically after an update", 
            inline=False
            )
        embed.add_field(
            name="Remove restrictions", 
            value="if you want to remove the restrictions (e.g. /activity can only be executed by the bot owner) build the bot yourself from [GitHub](https://wolldev24.github.io/sharky)", 
            inline=False
            )


        await ctx.respond(embed=embed)

def setup(bot):

    bot.add_cog(Info(bot))










