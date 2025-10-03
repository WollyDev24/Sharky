import discord
from discord.ext import commands
from discord.commands import slash_command


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Get info about the bot")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Information",
            description="Infos about Sharky",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Website",
            value="[Sharky Website](https://wollydev24.github.io/sharky.html)", 
            inline=False
        )
        embed.add_field(
            name="Version", 
            value="V1.4.0", 
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
            value=" - Website is now Listed in /info\n - if no Owner ID is configured the Bot will still work\n - if no Greet Channel is Configured your bot will still work, just doesnt greet people\n - New Greet Message\n - Bot displays the number of servers it is in when starting and New style for Startup messages", 
            inline=False
            )
        embed.add_field(
            name="Remove restrictions", 
            value="if you want to remove the restrictions (e.g. /activity can only be executed by the bot owner) build the bot yourself from [GitHub](https://github.com/wollydev24/sharky)", 
            inline=False
            )


        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
