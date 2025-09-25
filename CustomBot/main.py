import discord
import os

intents = discord.Intents.default()
intents.members = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="for hunry sharks")

from config import server

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[server],
    status=status,
    activity=activity
)


@bot.event
async def on_ready():
    print(f"{bot.user} is Online and Connected to Discord!")

if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

from config import token
bot.run(token)
