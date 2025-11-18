import discord
from discord import app_commands
from discord.ext import commands

from datetime import date

from utils.log import logger
from utils.database import DBUtils


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _is_attendanceable(self, discord_id: int) -> bool:
        from datetime import date

        attendanced_date = DBUtils.get_user_attendanced_date(discord_id, date.today())
        return attendanced_date is None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.strip() == "ㅊㅊ":
            if self._is_attendanceable(message.author.id):
                try:
                    await message.channel.send(
                        f"{message.author.mention}, your attendance has been recorded!"
                    )

                    exp, level = DBUtils.get_user_points(message.author.id)
                    streak = DBUtils.get_user_streak(message.author.id)
                    DBUtils.update_user_points(
                        message.author.id, exp=exp + 10, level=level
                    )
                    DBUtils.update_user_attendance(
                        message.author.id,
                        date.today(),
                        streak=streak + 1 if streak else 1,
                    )
                    reaction = "✅"
                    logger.info(
                        f"Attendance recorded for user: {message.author} (ID: {message.author.id})"
                    )
                except Exception as e:
                    reaction = "❌"
                    logger.error(
                        f"Failed to record attendance for user: {message.author} (ID: {message.author.id}). Error: {e}"
                    )
                await message.add_reaction(reaction)
            else:
                await message.add_reaction("❌")
                await message.channel.send(
                    f"{message.author.mention}, you have already recorded your attendance today."
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(Attendance(bot))
