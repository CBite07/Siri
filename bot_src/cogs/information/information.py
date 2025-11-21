import discord
from discord import app_commands
from discord.ext import commands

from utils.embeds import LevelEmbed
from utils.database import LevelDBUtil


class InfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="유저_정보", description="유저의 정보를 확인합니다.")
    @app_commands.describe(user="정보룰 조회할 유저를 지정하시오")
    async def show_user_info(
        self, interaction: discord.Interaction, user: discord.Member
    ):
        try:
            guild = interaction.guild
            level_data = LevelDBUtil.read_level_data(guild.id, user.id)

            if level_data:
                current_exp = level_data.get("exp", 0)
                current_level = level_data.get("level", 0)
                embed = LevelEmbed.return_user_info_embed(
                    user, current_exp, current_level
                )
            else:
                embed = LevelEmbed.return_no_user_info_embed(user)

            return await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)


async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))
