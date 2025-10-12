import subprocess
import os
import sys
from discord.ext import commands
from discord.commands import slash_command

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_for_updates(self):
        subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(
            ["git", "status", "-uno"], capture_output=True, text=True
        )
        return "Your branch is behind" in status.stdout

    def pull_updates(self):
        subprocess.run(["git", "pull"], check=True)

    @slash_command(description="Check for and apply bot updates")
    async def update(self, ctx):
        # First Respond (ephemeral)
        msg = await ctx.respond("🔍 Checking for updates...", ephemeral=True)
        message = await msg.original_response()

        try:
            if self.check_for_updates():
                await message.edit(content="⚙️ Update found! Pulling latest changes...")
                self.pull_updates()
                await message.edit(content="✅ Update complete! Restarting bot...")
                os.execv(sys.executable, ["python"] + sys.argv)
            else:
                await message.edit(content="✅ No updates found. Bot is up to date!")
        except Exception as e:
            await message.edit(content=f"❌ Update failed:\n```{e}```")

def setup(bot):
    bot.add_cog(Update(bot))
