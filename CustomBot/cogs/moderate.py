import discord
from discord.ext import commands
from discord.commands import slash_command, Option


class kick(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Kick a User")
    async def kick(self, ctx, member: Option(discord.Member, "Member to kick"), reason: Option(str, "Reason for kick", default="No reason provided")):
        if ctx.author.guild_permissions.kick_members:
            if member.guild_permissions.administrator:
                await ctx.respond("You cannot kick an administrator.")
                return
            try:
                await member.kick(reason=reason)
                await ctx.respond(f"{member.mention} has been kicked for: {reason}")
            except discord.Forbidden:
                await ctx.respond("I do not have permission to kick this user.")
            except Exception as e:
                await ctx.respond(f"An error occurred: {str(e)}")
        else:
            await ctx.respond("You do not have permission to use this command.")
        


def setup(bot: discord.Bot):
    bot.add_cog(kick(bot))
