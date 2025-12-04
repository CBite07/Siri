import discord
from discord import app_commands
from discord.ext import commands

from utils.UI.embeds import StatusEmbed
from utils.log import logger

class BotInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="봇_상태", description="봇의 상태를 확인합니다.")
    async def show_bot_status(self, interaction: discord.Interaction):
        try:
            embed = StatusEmbed.create_bot_status(self.bot)
            return await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(e)
            embed =  StatusEmbed.create_error()
            return await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(BotInfoCog(bot))