import discord
import os

intents = discord.Intents.default()
intents.members = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="for hunry sharks")

from config import server
from config import owner
from config import greet
from config import token

if token == "" or token is None:
    raise ValueError("[FATAL] No token provided. Please set the token in config.py")
else:
    print("[INFO] Token found.")
if owner == "" or owner is None:
    print("[NOTICE ]No owner ID provided, anyone will be able to control your bot")
else:
    print("[INFO] Owner ID Configured.")
if greet == "" or greet is None:
    print("[NOTICE] No greet channel ID provided. Bot will not Greet new members.")
else:
    print("[INFO] Greet channel ID Configured.")
print("[INFO] starting bot..")

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[server],
    status=status,
    activity=activity
)


@bot.event
async def on_ready():
    print(f"[INFO] {bot.user} is Online and Connected to Discord")
    print(f"[INFO] Bot started in {len(bot.guilds)} server(s)")

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

from config import token
bot.run(token)
