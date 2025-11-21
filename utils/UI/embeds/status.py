import discord


class StatusEmbed:
    def create_error():
        embed = discord.Embed(
            title="오류 발생",
            description="알 수 없는 오류가 발생했습니다.",
            color=discord.Color.red(),
        )

        return embed
