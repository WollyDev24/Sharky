from sys import prefix
import discord
from discord.ext import commands
from discord.commands import slash_command, Option

from config import owner

class ActivityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Change the status of the bot")
    async def activity(
        self, 
        ctx, 
        type: Option(str, "Type of activity", choices=["streaming", "watching", "playing", "listening", "Reset"]), 
        name: Option(str, "Name of the activity") 
    ): 
        if ctx.author.id == owner: 
            embed = discord.Embed(
                title="❌ Permission Denied",
                description="Only the owner of the bot can run this command.",
                color=discord.Color.red()
            )    
            embed.add_field(
                name="Want to remove this restriction?", 
                value="Build the bot yourself from [GitHub](https://github.com/wollydev24/sharky)", 
                inline=True
            )
            await ctx.respond(embed=embed)
            return

        if type == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
            color = discord.Color.blue()
        elif type == "streaming":
            activity = discord.Activity(type=discord.ActivityType.streaming, name=name, url="https://www.twitch.tv/wollywoll8844")
            color = discord.Color.purple()
        elif type == "playing":
            activity = discord.Activity(type=discord.ActivityType.playing, name=name)
            color = discord.Color.green()
        elif type == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
            color = discord.Color.orange()
        elif type == "Reset":
            activity = discord.Activity(type=discord.ActivityType.watching, name="for hunry sharks")
            color = discord.Color.default()

        await self.bot.change_presence(activity=activity)

        if type == "Reset":
            description = "Activity reset to default."
        else:
            description = f"{type}: **{name}**"

        embed = discord.Embed(
            title="✅ Activity Updated",
            description=description,
            color=color
        )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(ActivityCog(bot))
