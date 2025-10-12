import discord
import os
import asyncio

intents = discord.Intents.default()
intents.members = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="for hunry sharks")

from config import server
from config import owner
from config import greet
from config import token

if token == "" or token is None:
    print("\033[31m[FATAL]\033[0m No token provided. Please set the token in config.py")
    raise ValueError("No token provided")
else:
    print("\033[32m[INFO]\033[0m Token found.")
if owner == "" or owner is None:
    print("\033[35m[NOTICE]\033[0m No owner ID provided, anyone will be able to control your bot")
else:
    print("\033[32m[INFO]\033[0m Owner ID Configured.")
if greet == "" or greet is None:
    print("\033[35m[NOTICE]\033[0m No greet channel ID provided. Bot will not Greet new members.")
else:
    print("\033[32m[INFO]\033[0m Greet channel ID Configured.")
print("\033[32m[INFO]\033[0m starting bot..")

asyncio.set_event_loop(asyncio.new_event_loop())

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[server],
    status=status,
    activity=activity
)


@bot.event
async def on_ready():
    print(f"\033[32m[INFO]\033[0m {bot.user} is Online and Connected to Discord")
    print(f"\033[32m[INFO]\033[0m Bot is curently running in {len(bot.guilds)} server(s)")

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

import subprocess

print("🔍 Checking for updates...")
subprocess.run(["git", "fetch"])
status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
if "Your branch is behind" in status.stdout:
    print("⚙️ Update found! Pulling changes...")
    subprocess.run(["git", "pull"])

bot.run(token)
