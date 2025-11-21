import discord


class LevelEmbed:
    @staticmethod
    def create_user_info(user: discord.Member, exp: int, level: int):
        embed = discord.Embed(
            title="유저 정보",
            description="유저 정보를 출력합니다.",
            color=discord.Color.blue(),
        )
        embed.add_field(name="닉네임", value=user.mention, inline=True)
        embed.add_field(name="경험치", value=f"{exp} XP", inline=True)
        embed.add_field(name="레벨", value=level, inline=True)

        return embed

    @staticmethod
    def create_not_found_error(user: discord.Member):
        embed = discord.Embed(
            title="유저를 찾을 수 없습니다.",
            description=f"{user.display_name}님의 정보를 찾을 수 없습니다.",
            color=discord.Color.red(),
        )

        return embed
