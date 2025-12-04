import discord

from utils.level import LevelUtil
from utils.UI.visualization import VisualUtil

class LevelEmbed:
    def create_user_info(user: discord.Member, exp: int, level: int):
        next_level_total_exp = LevelUtil.level_to_exp(level + 1)
        remaining_exp_precent = LevelUtil.percent_of_remaining_exp(exp)
        graph = VisualUtil.create_progress_bar(remaining_exp_precent, 20)
        
        embed = discord.Embed(
            title="유저 레벨 정보",
            description="유저 레벨 정보를 출력합니다.",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="닉네임", value=user.mention)
        embed.add_field(name="경험치", value=f"{exp} XP")
        embed.add_field(name="레벨", value=level)
        embed.add_field(
            name="남은 경험치",
            value=f"{exp} / {next_level_total_exp} \n{graph}"
        )

        return embed

    def create_my_info(user: discord.Member, exp: int, level: int):
        next_level_total_exp = LevelUtil.level_to_exp(level + 1)
        remaining_exp_precent = LevelUtil.percent_of_remaining_exp(exp)
        graph = VisualUtil.create_progress_bar(remaining_exp_precent, 20)
        
        embed = discord.Embed(
            title="내 레벨 정보",
            description="나의 레벨 정보를 출력합니다.",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="닉네임", value=user.mention)
        embed.add_field(name="경험치", value=f"{exp} XP")
        embed.add_field(name="레벨", value=level)
        embed.add_field(
            name="남은 경험치",
            value=f"{exp} / {next_level_total_exp} \n{graph}"
        )

        return embed

    def create_not_found_error(user: discord.Member):
        embed = discord.Embed(
            title="정보를 찾을 수 없습니다.",
            description=f"{user.display_name}님의 정보를 찾을 수 없습니다.",
            color=discord.Color.red(),
        )

        return embed
    
