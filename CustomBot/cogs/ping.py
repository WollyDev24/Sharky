import discord
from discord.ext import commands
from discord.commands import slash_command
import datetime

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
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

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = ctx.command.get_cooldown_retry_after(ctx)

            await ctx.respond(f"Hey i love that you want to see the ping but please wait {seconds:.2f} seconds.", ephemeral=True)


def setup(bot):
    bot.add_cog(Ping(bot))
