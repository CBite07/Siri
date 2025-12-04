import discord
from discord.ext import commands

class StatusEmbed:
    def create_bot_status(latency: float, mem_usage_mb: int, guilds: int) -> discord.Embed:
        embed = discord.Embed(
            title="봇 정보",
            description="봇의 현재 정보를 출력합니다.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="지연시간",
            value=f"{int(format * 1000)}ms"
        )
        embed.add_field(
            name="메모리 사용량",
            value=f"{mem_usage_mb}MB"
        )
        embed.add_field(
            name="서버 수",
            value=f"{guilds}개"
        )

        return embed

    def create_error() -> discord.Embed:
        embed = discord.Embed(
            title="오류 발생",
            description="알 수 없는 오류가 발생했습니다.",
            color=discord.Color.red()
        )

        return embed
