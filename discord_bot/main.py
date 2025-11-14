import discord
from discord.ext import commands
import os

from configs.path import PathConfig
from discord_bot.configs.bot import BotConfig
from discord_bot.utils.log import print_formatted_log

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BotConfig.get_command_prefix, intents=intents)


@bot.event
async def on_ready():
    print_formatted_log("START", __name__, "Bot logged in successfully.")
    await bot.tree.sync()
    print_formatted_log(
        "START", __name__,
        f"Bot synchronized {BotConfig.get_command_count(bot)} commands successfully.",
    )


async def load_cogs():
    for filename in os.listdir(PathConfig.DISCORD_COG_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"discord_bot.cogs.{filename[:-3]}")
            print_formatted_log(
                "START", __name__, f"Bot loaded cogs.{filename} successfully"
            )


async def run_bot():
    await load_cogs()
    await bot.start(BotConfig.get_bot_token())
