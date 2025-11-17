# import discord module
import discord
from discord.ext import commands

# import os module
import os

# import util modules
from utils.configs.bot import BotConfig
from utils.configs.path import PathConfig
from utils.log import logger

# create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BotConfig.COMMAND_PREFIX, intents=intents)


# define on_ready event
@bot.event
async def on_ready():
    logger.info(f"Bot logged in as {bot.user} (ID: {bot.user.id})")
    await bot.tree.sync()
    logger.info("Bot command tree synced successfully")


# load cogs
async def load_cogs():
    for cog in PathConfig.COGS:
        await bot.load_extension(cog)
        logger.info(f"Loaded cog: {cog}")


# run the bot
async def run_bot():
    await load_cogs()
    await bot.start(BotConfig.TOKEN)
