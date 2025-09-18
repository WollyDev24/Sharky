import discord
from discord.ext import commands
from discord.commands import slash_command


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def info(self, ctx):
        embed = discord.Embed(
            title="Bot Information",
            description="Infos About YouShadeBot",
            color=discord.Color.green()
        )

        embed.add_field(name="Version", value="0.3", inline=False)
        embed.add_field(name="Developer", value="[WollyDev24](https://github.com/WollyDev24)", inline=False)
        embed.add_field(name="Github", value="[Github Repo](https://github.com/WollyDev24/YouShadeBot/)", inline=False)
        embed.set_footer(text="YouShadeBot is running in an Alpha State, be sure to check for Beta and Stable Updates!")

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))