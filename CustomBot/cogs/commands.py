import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Change the status of the bot (testing purposes)")
    async def changestatus(
            self, ctx, 
            type: Option(str, "Type of activity", choices=["streaming", "watching", "Online"]),
            name: Option(str, "Name of the activity")
    ): 
        if type == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
        if type == "Streaming":
            activity = discord.Activity(type=discord.ActivityType.streaming, name=name, url="https://www.twitch.tv/wollywoll8844") # set to your twitch channel

        await self.bot.change_presence(activity=activity, status=status)
        await ctx.respond(f"Status changed to {type} {name}")

def setup(bot):
    bot.add_cog(commands(bot))