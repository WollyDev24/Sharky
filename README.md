![Banner](https://github.com/WollyDev24/Sharky/blob/main/resources/Sharky.png?raw=true)

# - Development of this bot stopped, thx for almost nothing

![GitHub Repo stars](https://img.shields.io/github/stars/WollyDev24/Sharky?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/WollyDev24/Sharky?style=for-the-badge)

### YouShadeBot got a Rebranding and is now Sharky!

# Sharky
Code for an cool in development Discord bot with a few cool features. 
- This project is licensed under an GPL-3.0 License

## Support and Server
[![Join our Discord](https://img.shields.io/badge/Discord-Join%20Chat-5865F2?logo=discord&logoColor=white&style=for-the-badge)](https://discord.gg/bapB8zz7VY)
[![Join Telegram](https://img.shields.io/badge/Telegram-Join%20Channel-26A5E4?logo=telegram&logoColor=white&style=for-the-badge)](https://t.me/SharkyUpdates)

## 💻 Features Available
- 🙍 Greet user via Command
- 👋 Automatic Greet Message
- ℹ️ Info Command
- 🎮 Bot Activity Changer
- ⌛ Ping Comamnd
- 🛑 Moderate (only kick as of now)
- 🎮 Play Rock-Paper-Scissor
- 💻 Control your bot over terminal (eg. shutdown, see servers, reload cogs and more)

## 💾 Planned Features
- 📣 Announcements
- 🤫 Whisper Messages
- 📒 Notes 

## 📌 Add the bot to your server
[![Add Bot to Server](https://img.shields.io/badge/Add%20Bot-Invite-blue?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1410735946374053918&permissions=8&integration_type=0&scope=bot)
- Note that some things are restricted like the /activity command if you want to use these commands built the bot yourself from the tutorial below

## 🚀 Setup Guide

1️⃣ **Clone**  
```
git clone https://github.com/wollydev24/sharky
```


2️⃣ **Create a Discord Application**  
Go to the [Discord Developer Portal](https://discord.com/developers/applications) → Create a new application → Add a name + icon.

3️⃣ **Insert your Bot Token**  
- Rename `config_example.py` to `config.py`  
- Replace `token` with your bot token

4️⃣ **Set all IDs**  
- `server` → your server ID  
- `greet` → the ID of your welcome channel  
- `owner` → your Discord ID  

5️⃣ **Restrict bot to one server (Optional)**
- Change this line to include ``debug_guilds=server,``

```python
bot = discord.Bot(
    intents=intents,
    debug_guilds=server,
    status=status,
    activity=activity
)
```

6️⃣ **Invite the Bot**  
- Invite the bot to your server

7️⃣ **Start the Bot**
```bash
py main.py
```

## Contribute to Development
if you want to help me or Support my Work
- Make Pull Requests
- Star the Repo
- Join the `Support Server` or `Telegram Channel`
