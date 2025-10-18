import discord
import random
from discord.ext import commands
from discord.commands import slash_command, Option

class RPS(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Play Rock Paper Scissors")
    async def rps(self, ctx, choice: Option(str, "What do you choose?", choices=["rock", "paper", "scissor"])): # type: ignore
        bot_choice = random.choice(["rock", "paper", "scissor"])

        # Regeln
        if choice == bot_choice:
            result = "It's a tie! 🤝"
        elif (
            (choice == "scissor" and bot_choice == "paper") or
            (choice == "rock" and bot_choice == "scissor") or
            (choice == "paper" and bot_choice == "rock")
        ):
            result = "You won! 🎉"
        else:
            result = "You lost! 😢"

        await ctx.respond(
            f"🪨 **Rock Paper Scissors!** ✂️\n\n"
            f"**You:** {choice}\n"
            f"**Bot:** {bot_choice}\n\n"
            f"**{result}**"
        )

def setup(bot: discord.Bot):
    bot.add_cog(RPS(bot))