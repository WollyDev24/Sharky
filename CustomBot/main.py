import discord
import os
import sys
import asyncio
import subprocess
import threading
import random
import time

# Update system
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

auto_update()

intents = discord.Intents.default()
intents.members = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="for hungry sharks :3")

from config import server, owner, greet, token

if not token or token == "123456789010.ABCDEFGHIJK.KLMNOPQ.RSTUVWXYZ":
    print("\033[31m[FATAL]\033[0m No token provided. Please set the token in config.py")
    raise ValueError("No token provided")
else:
    print("\033[32m[INFO]\033[0m Token found.")
if not owner or owner == "123456789":
    print("\033[35m[NOTICE]\033[0m No owner ID provided, anyone could access /auth.")
else:
    print("\033[32m[INFO]\033[0m Owner ID configured.")
if not greet or greet == "123456789":
    print("\033[35m[NOTICE]\033[0m No greet channel ID provided.")
else:
    print("\033[32m[INFO]\033[0m Greet channel ID configured.")

print("\033[32m[INFO]\033[0m Starting bot...")

asyncio.set_event_loop(asyncio.new_event_loop())

bot = discord.Bot(
    intents=intents,
    debug_guilds=[server],
    status=status,
    activity=activity
)

# Auth Framework
authenticated = False
auth_code = str(random.randint(100000, 999999)) if not authenticated else None

@bot.event
async def on_ready():
    print(f"\033[32m[INFO]\033[0m {bot.user} is Online and Connected to Discord")
    print(f"\033[32m[INFO]\033[0m Running in {len(bot.guilds)} server(s)")
    time.sleep(0.5)
    if not authenticated:
        print(f"\033[35m[AUTH]\033[0m AUTH CODE: \033[36m{auth_code}\033[0m")
        print("\033[35m[AUTH]\033[0m Type /auth <code> in Discord (as owner) to unlock terminal control.")
    else:
        print("\033[35m[AUTH]\033[0m Terminal is already unlocked (authenticated = True).")

@bot.slash_command(description="Authenticate terminal control (Owner only)")
async def auth(ctx, code: str):
    global authenticated
    user = ctx.author
    result = ""

    try:
        owner_user = await bot.fetch_user(int(owner))
    except Exception:
        owner_user = None

    if str(user.id) != str(owner):
        await ctx.respond("🚫 You are not authorized to unlock terminal access.", ephemeral=True)
        result = "❌ Unauthorized user tried to authenticate."
    elif authenticated:
        await ctx.respond("✅ Terminal is already unlocked.", ephemeral=True)
        result = "✅ Already authenticated."
    elif code == auth_code:
        authenticated = True
        await ctx.respond("✅ Terminal access granted! Terminal commands can now be used.", ephemeral=True)
        print(f"\033[33m[AUTH]\033[0m Terminal authenticated by {user}.")
        result = "✅ Auth successful."
    else:
        await ctx.respond("❌ Invalid code. Try again.", ephemeral=True)
        result = "❌ Wrong code entered."

    if owner_user:
        try:
            embed = discord.Embed(
                title="🔐 Authentication Attempt Detected",
                color=discord.Color.blurple()
            )
            embed.add_field(name="User", value=f"{user} (`{user.id}`)", inline=False)
            embed.add_field(name="Entered Code", value=code, inline=False)
            embed.add_field(name="Result", value=result, inline=False)
            embed.set_footer(text=f"Server: {ctx.guild.name if ctx.guild else 'Direct Message'}")
            await owner_user.send(embed=embed)
        except discord.Forbidden:
            print("\033[31m[ERROR]\033[0m Could not send DM to owner (DMs disabled).")
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m Failed to send DM: {e}")

# Terminal Command Handler
def terminal_commands():
    global authenticated

    while True:
        if not authenticated:
            print("\033[31m[AUTH]\033[0m Terminal locked. Generating code for /auth command...")
            while not authenticated:
                asyncio.run(asyncio.sleep(2))
            print("\033[33m[AUTH]\033[0m Terminal unlocked! You can now control the bot.\n")

        try:
            cmd = input(">> ").strip()
            if cmd == "":
                continue

            if cmd in ["exit", "stop"]:
                print("\033[33m[INFO]\033[0m Stopping bot...")
                asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
                break

            elif cmd == "reload":
                cogs_path = "cogs" if os.path.exists("cogs") else "CustomBot/cogs"
                for filename in os.listdir(cogs_path):
                    if filename.endswith(".py"):
                        bot.reload_extension(f"cogs.{filename[:-3]}")
                print(f"\033[32m[COGS]\033[0m Reloaded config.")
                time.sleep(0.1)

            elif cmd == "servers":
                print("\033[33m[INFO]\033[0m Connected servers:")
                for guild in bot.guilds:
                    print(f" - {guild.name} ({guild.id})")

            elif cmd == "lock":
                authenticated = False
                print("\033[33m[AUTH]\033[0m Terminal locked.")

            elif cmd == "help":
                print("""
\033[36mAvailable Terminal Commands:\033[0m
  help         → Show this message
  say <msg>    → Send message (choose server & channel)
  servers      → List connected servers
  reload       → Reload bot cogs
  lock         → Lock terminal again
  exit / stop  → Stop the bot
""")
                
            elif cmd.startswith("say "):
                msg = cmd.split(" ", 1)[1]

                print("\n\033[33m[TERMINAL]\033[0m Select a server:")
                for i, guild in enumerate(bot.guilds, start=1):
                    print(f"  {i}. {guild.name} ({guild.id})")

                try:
                    choice = int(input("\nServer number: "))
                    guild = bot.guilds[choice - 1]
                except (ValueError, IndexError):
                    print("\033[31m[ERROR]\033[0m Invalid server number.")
                    continue

                text_channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]
                if not text_channels:
                    print("\033[31m[ERROR]\033[0m No writable text channels in this server.")
                    continue

                print("\n\033[33m[TERMINAL]\033[0m Select a channel:")
                for i, ch in enumerate(text_channels, start=1):
                    print(f"  {i}. #{ch.name}")

                try:
                    ch_choice = int(input("\nChannel number: "))
                    channel = text_channels[ch_choice - 1]
                except (ValueError, IndexError):
                    print("\033[31m[ERROR]\033[0m Invalid channel number.")
                    continue

                asyncio.run_coroutine_threadsafe(channel.send(msg), bot.loop)
                print(f"\033[32m[TERMINAL]\033[0m Sent message to {guild.name} → #{channel.name}: {msg}")

            else:
                print(f"\033[31m[ERROR]\033[0m Unknown command '{cmd}'. Type 'help' for options.")

        except KeyboardInterrupt:
            print("\n\033[33m[TERMINAL]\033[0m Shutting down...")
            asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
            break
        except Exception as e:
            print(f"\033[31m[ERROR]\033[0m {e}")


threading.Thread(target=terminal_commands, daemon=True).start()

if __name__ == "__main__":
    cogs_path = "cogs" if os.path.exists("cogs") else "CustomBot/cogs"
    for filename in os.listdir(cogs_path):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(token)