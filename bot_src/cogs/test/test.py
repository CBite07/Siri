import discord
from discord import app_commands
from discord.ext import commands
import inspect

from utils.log import print_log, print_error_log
from utils.database import db

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
            print_error_log(__name__, function_name, e)

    @app_commands.command(name="pong", description="ping")
    async def pong(self, interaction: discord.Interaction):
        try:
            await send_message(interaction, "ping!")
        except Exception as e:
            function_name = inspect.currentframe().f_code.co_name
            print_error_log(__name__, function_name, e)

    @app_commands.command(name="db_test", description="db test")
    async def db_test(self, interaction: discord.Interaction):
        try:
            db.add_user(interaction.user.id)
            points = db.fetch_points(interaction.user.id)
            levels = db.fetch_levels(interaction.user.id)
            await send_message(interaction, f"Points: {points}, Levels: {levels}")
        except Exception as e:
            function_name = inspect.currentframe().f_code.co_name
            print_error_log(__name__, function_name, e)


async def setup(bot: commands.Bot):
    await bot.add_cog(TestCog(bot))
