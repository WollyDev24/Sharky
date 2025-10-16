import subprocess
import os
import sys
from discord.ext import commands
from discord.commands import slash_command

# ANSI-Farben für Terminalausgabe
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔹 Check for updates
    def check_for_updates(self):
        print(f"{BLUE}[UPDATE]{RESET} Checking for updates...")
        subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(
            ["git", "status", "-uno"], capture_output=True, text=True
        )
        if "Your branch is behind" in status.stdout:
            print(f"{YELLOW}[UPDATE]{RESET} Updates available.")
            return True
        print(f"{GREEN}[UPDATE]{RESET} No updates found.")
        return False

    # 🔹 Pull latest changes
    def pull_updates(self):
        print(f"{BLUE}[GIT]{RESET} Pulling latest changes...")
        subprocess.run(["git", "pull"], check=True)
        print(f"{GREEN}[GIT]{RESET} Pull completed successfully!")

    # 🔹 Restart the bot
    def restart_bot(self):
        print(f"{YELLOW}[SYSTEM]{RESET} Restarting bot...")
        python = sys.executable
        subprocess.Popen([python] + sys.argv)
        print(f"{GREEN}[SYSTEM]{RESET} New process started. Exiting old one.")
        sys.exit(0)

    # 🔹 Slash command: /update
    @slash_command(description="Check for and apply bot updates")
    async def update(self, ctx):
        msg = await ctx.respond("🔍 Checking for updates...", ephemeral=True)
        message = await msg.original_response()

        try:
            if self.check_for_updates():
                await message.edit(content="⚙️ Update found! Pulling latest changes...")
                self.pull_updates()
                await message.edit(content="✅ Update complete! Restarting bot...")
                self.restart_bot()
            else:
                await message.edit(content="✅ No updates found. Bot is up to date!")
        except Exception as e:
            print(f"{RED}[ERROR]{RESET} {e}")
            await message.edit(content=f"❌ Update failed:\n```{e}```")

def setup(bot):
    bot.add_cog(Update(bot))
