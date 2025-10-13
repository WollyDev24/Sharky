import discord
import os
import sys
import asyncio
import subprocess

# === 🟦 Auto-Update at Startup ===
def auto_update():
    print("\033[34m[UPDATE]\033[0m Checking for updates...")
    try:
        subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)

        if "Your branch is behind" in status.stdout:
            print("\033[34m[UPDATE]\033[0m Update found! Pulling changes...")
            try:
                subprocess.run(["git", "pull"], check=True)
            except subprocess.CalledProcessError:
                print("\033[33m[UPDATE WARN]\033[0m Local changes detected! Forcing update...")
                subprocess.run(["git", "reset", "--hard", "HEAD"], check=True)
                subprocess.run(["git", "clean", "-fd"], check=True)
                subprocess.run(["git", "pull"], check=True)
            
            print("\033[34m[UPDATE]\033[0m Update applied successfully. Restarting bot...")
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            print("\033[34m[UPDATE]\033[0m Bot is up to date!")

    except Exception as e:
        print(f"\033[31m[UPDATE ERROR]\033[0m {e}")

# Run Update check
auto_update()

# === 🟩 Discord Setup ===
intents = discord.Intents.default()
intents.members = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="for hungry sharks")

from config import server, owner, greet, token

# === 🟨 Config Checks ===
if not token:
    print("\033[31m[FATAL]\033[0m No token provided. Please set the token in config.py")
    raise ValueError("No token provided")
else:
    print("\033[32m[INFO]\033[0m Token found.")
if not owner:
    print("\033[35m[NOTICE]\033[0m No owner ID provided, anyone will be able to control your bot")
else:
    print("\033[32m[INFO]\033[0m Owner ID Configured.")
if not greet:
    print("\033[35m[NOTICE]\033[0m No greet channel ID provided. Bot will not greet new members.")
else:
    print("\033[32m[INFO]\033[0m Greet channel ID Configured.")

print("\033[32m[INFO]\033[0m Starting bot...")

# === 🟪 Iniate bot ===
asyncio.set_event_loop(asyncio.new_event_loop())

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[server],
    status=status,
    activity=activity
)

# === 🟧 Events ===
@bot.event
async def on_ready():
    print(f"\033[32m[INFO]\033[0m {bot.user} is Online and Connected to Discord")
    print(f"\033[32m[INFO]\033[0m Bot is currently running in {len(bot.guilds)} server(s)")

# === 🟦 Load cogs ===
if __name__ == "__main__":
    if os.path.exists("cogs"):
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                bot.load_extension(f"cogs.{filename[:-3]}")
    else:
        for filename in os.listdir("CustomBot/cogs"):
            if filename.endswith(".py"):
                bot.load_extension(f"cogs.{filename[:-3]}")

# === 🟩 Start ===
bot.run(token)
