import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(
    intents=intents, 
    debug_guilds=[1400527951329759412]
) # Optional: Replace with your server ID (Recommend) or Leave blank to make it work on every server


@bot.event
async def on_ready():
    print(f"{bot.user} is Online and Connected to Discord!")

if __name__ == "__main__":
    	for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("Your Token")