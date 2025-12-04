import discord
from discord import app_commands
from discord.ext import commands

from utils.UI.embeds import LevelEmbed, StatusEmbed
from utils.database import LevelDBUtil
from utils.log import logger


class LevelInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="유저_정보", description="유저의 레벨 정보를 확인합니다.")
    @app_commands.describe(user="정보룰 조회할 유저를 지정하시오")
    @app_commands.guild_only()
    async def show_user_info(
        self, interaction: discord.Interaction, user: discord.Member
    ):
        try:
            guild = interaction.guild
            level_data = LevelDBUtil.read_level_data(guild.id, user.id)

            if level_data:
                current_exp = level_data.get("exp", 0)
                current_level = level_data.get("level", 0)
                embed = LevelEmbed.create_user_info(user, current_exp, current_level)
            else:
                embed = LevelEmbed.create_not_found_error(user)
            return await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(e)
            embed = StatusEmbed.create_error()
            return await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="내_정보", description="나의 레벨 정보를 확인합니다.")
    @app_commands.guild_only()
    async def show_my_info(
        self, interaction: discord.Interaction
    ):
        user = interaction.user
        try:
            guild = interaction.guild
            level_data = LevelDBUtil.read_level_data(guild.id, user.id)

            if level_data:
                current_exp = level_data.get("exp", 0)
                current_level = level_data.get("level", 0)
                embed = LevelEmbed.create_my_info(user, current_exp, current_level)
            else:
                embed = LevelEmbed.create_my_info(user)
            return await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(e)
            embed = StatusEmbed.create_error()
            return await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(LevelInfoCog(bot))
