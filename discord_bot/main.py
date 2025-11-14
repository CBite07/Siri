import discord
from discord.ext import commands
import os
import sys

from configs.path import PathConfig
from discord_bot.configs.bot import BotConfig
from discord_bot.utils.time import get_formatted_time
from discord_bot.utils.log import get_formatted_log

if str(PathConfig.ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(PathConfig.ROOT_DIR))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=BotConfig.get_command_prefix, intents=intents)


@bot.event
async def on_ready():
    print(get_formatted_log("START", __name__, "Bot logged in successfully."))

    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)

    print(
        get_formatted_log(
            "START",
            __name__,
            f"Bot synchronized {BotConfig.get_command_count(bot)} commands successfully.",
        )
    )


for filename in os.listdir(PathConfig.DISCORD_COG_DIR):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")  # .py 제거
        print(
            get_formatted_log(
                "START", __name__, f"Bot loaded cogs.{filename} successfully"
            )
        )


def run_bot():
    bot.run(BotConfig.get_bot_token())
