import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import json
import os

class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "CustomBot/cogs/welcome_channels.json"
        self.welcome_channels = self.load_channels()

    # JSON laden oder erstellen
    def load_channels(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    # JSON speichern
    def save_channels(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.welcome_channels, f, indent=4)

    # Command: Server-spezifischen Welcome-Channel setzen
    @slash_command(description="Set the welcome channel for this server")
    async def setwelcome(
        self,
        ctx,
        channel: Option(discord.TextChannel, "Select the channel for welcome messages") # type: ignore
    ):
        guild_id = str(ctx.guild.id)
        self.welcome_channels[guild_id] = channel.id
        self.save_channels()
        await ctx.respond(f"✅ Welcome channel set to {channel.mention}", ephemeral=True)

    # Command: Test (optional)
    @slash_command(description="Say hello to yourself")
    async def greet(self, ctx):
        await ctx.respond(f"Hey {ctx.author.mention}!")

    # Member Join Event
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id not in self.welcome_channels:
            return  # kein Welcome Channel gesetzt → nichts tun

        channel_id = self.welcome_channels[guild_id]
        channel = member.guild.get_channel(channel_id)
        if channel is None:
            return  # Channel gelöscht oder ungültig

        embed = discord.Embed(
            title="🎉 Welcome!",
            description=(
                f"Welcome to the server, {member.mention}!\n"
                f"Be sure to check the rules and have fun! 😄"
            ),
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Greet(bot))
