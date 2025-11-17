import discord
from discord.ext import commands
import os

from utils.configs.bot import BotConfig
from utils.configs.path import PathConfig
from utils.log import print_log

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BotConfig.get_command_prefix, intents=intents)


@bot.event
async def on_ready():
    print_log("start", __name__, "Bot logged in successfully.")
    await bot.tree.sync()
    print_log(
        "start",
        __name__,
        f"Bot synchronized {await BotConfig.get_command_count(bot)} commands successfully.",
    )


async def load_cogs():
    for cog in PathConfig.COGS:
        await bot.load_extension(cog)
        print_log("start", __name__, f"Bot loaded {cog} successfully")


async def run_bot():
    await load_cogs()
    await bot.start(BotConfig.get_bot_token())
