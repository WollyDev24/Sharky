import discord
import os
import sys
import asyncio
import subprocess
import threading
import random

# === 🟦 Auto Update ===
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

# === 🟦 Discord Setup ===
intents = discord.Intents.default()
intents.members = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="for hungry sharks")

from config import server, owner, greet, token

if not token:
    print("\033[31m[FATAL]\033[0m No token provided. Please set the token in config.py")
    raise ValueError("No token provided")
else:
    print("\033[32m[INFO]\033[0m Token found.")
if not owner:
    print("\033[35m[NOTICE]\033[0m No owner ID provided, anyone could access /auth.")
else:
    print("\033[32m[INFO]\033[0m Owner ID configured.")

if not greet:
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

# === 🟩 Auth System ===
authenticated = False
auth_code = str(random.randint(100000, 999999))

@bot.event
async def on_ready():
    print(f"\033[32m[INFO]\033[0m {bot.user} is Online and Connected to Discord")
    print(f"\033[32m[INFO]\033[0m Running in {len(bot.guilds)} server(s)")
    print(f"🔐 AUTH CODE: \033[36m{auth_code}\033[0m")
    print("💡 Type /auth <code> in Discord (as owner) to unlock terminal control.")

@bot.slash_command(description="Authenticate terminal control (Owner only)")
async def auth(ctx, code: str):
    global authenticated
    user = ctx.author
    result = ""
    
    try:
        # Versuche Owner für DM zu laden
        owner_user = await bot.fetch_user(int(owner))
    except Exception:
        owner_user = None

    if str(user.id) != str(owner):
        await ctx.respond("🚫 You are not authorized to unlock terminal access.", ephemeral=True)
        result = "❌ Unauthorized user tried to authenticate."
    elif code == auth_code:
        authenticated = True
        await ctx.respond("✅ Terminal access granted! You may now use console commands.", ephemeral=True)
        print(f"🔓 Terminal authenticated by {user}.")
        result = "✅ Auth successful."
    else:
        await ctx.respond("❌ Invalid code. Try again.", ephemeral=True)
        result = "❌ Wrong code entered."

    # === 📩 DM-Benachrichtigung an den Owner ===
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
            print("⚠️ Could not send DM to owner (DMs disabled).")
        except Exception as e:
            print(f"⚠️ Failed to send DM: {e}")

# === 🧠 Terminal Command System ===
def terminal_commands():
    global authenticated
    while True:
        if not authenticated:
            print("🔒 Terminal locked. Waiting for /auth command in Discord...")
            # Block input until unlocked
            while not authenticated:
                asyncio.run(asyncio.sleep(2))
            print("✅ Terminal unlocked! You can now control the bot.\n")

        try:
            cmd = input(">> ").strip()
            if cmd == "":
                continue

            if cmd in ["exit", "stop"]:
                print("🟥 Stopping bot...")
                asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
                break

            elif cmd.startswith("say "):
                msg = cmd.split(" ", 1)[1]
                for guild in bot.guilds:
                    if guild.text_channels:
                        channel = guild.text_channels[0]
                        asyncio.run_coroutine_threadsafe(channel.send(msg), bot.loop)
                print(f"💬 Sent message: {msg}")

            elif cmd.startswith("reload "):
                name = cmd.split(" ", 1)[1]
                try:
                    bot.reload_extension(f"cogs.{name}")
                    print(f"🔄 Reloaded cog: {name}")
                except Exception as e:
                    print(f"❌ Failed to reload cog: {e}")

            elif cmd == "servers":
                print("🌍 Connected servers:")
                for guild in bot.guilds:
                    print(f" - {guild.name} ({guild.id})")

            elif cmd == "lock":
                authenticated = False
                print("🔒 Terminal locked again.")

            elif cmd == "help":
                print("\nAvailable commands:")
                print("  help           - Show this message")
                print("  say <text>     - Send a message in the first text channel of all servers")
                print("  reload <cog>   - Reload a cog")
                print("  servers        - List connected servers")
                print("  lock           - Lock terminal access again")
                print("  stop / exit    - Stop the bot\n")

            else:
                print("❓ Unknown command. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\n🟥 Shutting down...")
            asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
            break

# === 🧵 Start terminal command thread ===
threading.Thread(target=terminal_commands, daemon=True).start()

# === 🟢 Load Cogs ===
if __name__ == "__main__":
    cogs_path = "cogs" if os.path.exists("cogs") else "CustomBot/cogs"
    for filename in os.listdir(cogs_path):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

# === 🚀 Run Bot ===
bot.run(token)
