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
            description="Infos About YouShadeBot",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Version", 
            value="V1.0.0", 
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
            value="[Github Repo](https://github.com/WollyDev24/YouShadeBot/)", 
            inline=False
            )
        embed.add_field(
            name="Newest Update", 
            value=" - Updadet Info Command\n - /changestatus is now /activity\n - Ping Command added\n - Greet channel is now in config.py\n - More options for /activity", 
            inline=False
            )
        embed.set_footer(
            text="You are running the Stable Version of YouShadeBot"
            )

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
