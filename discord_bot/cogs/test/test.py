import discord
from discord import app_commands
from discord.ext import commands
import inspect

from discord_bot.utils.log import print_formatted_log, print_cog_error_log

from .send_message import send_message


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="pong")
    async def ping(self, interaction: discord.Interaction):
        try:
            await send_message(interaction, "pong!")
        except Exception as e:
            function_name = inspect.currentframe().f_code.co_name
            print_cog_error_log(__name__, function_name, e)

    @app_commands.command(name="pong", description="ping")
    async def pong(self, interaction: discord.Interaction):
        try:
            await send_message(interaction, "ping!")
        except Exception as e:
            function_name = inspect.currentframe().f_code.co_name
            print_cog_error_log(__name__, function_name, e)


async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))
