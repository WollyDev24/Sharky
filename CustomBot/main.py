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
    raise ValueError("No token provided. Please set the token in config.py")
else:
    print("Token found.")
if owner == "" or owner is None:
    raise ValueError("No owner ID provided. Please set the owner ID in config.py")
else:
    print("Owner ID found.")
if greet == "" or greet is None:
    raise ValueError("No greet channel ID provided. Please set the greet channel ID in config.py")
else:
    print("Greet channel ID found.")

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[server],
    status=status,
    activity=activity
)


@bot.event
async def on_ready():
    print(f"{bot.user} is Online and Connected to Discord")

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

from config import token
bot.run(token)
