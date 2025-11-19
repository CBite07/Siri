import discord
from discord import app_commands
from discord.ext import commands

from datetime import date

from utils.log import logger
from utils.database import LevelDBUtil, AttendanceDBUtil


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _is_attendanceable(self, discord_id: int) -> bool:
        from datetime import date

        attendanced_date = AttendanceDBUtil.read_attendanced_date_record(
            discord_id, date.today()
        )
        return attendanced_date is None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.strip() == "ㅊㅊ":
            if self._is_attendanceable(message.author.id):
                try:
                    exp = LevelDBUtil.read_user_exp_record(message.author.id)
                    streak = AttendanceDBUtil.read_attendance_streak_record(
                        message.author.id
                    )
                    LevelDBUtil.update_user_exp(message.author.id, exp=exp + 10)
                    AttendanceDBUtil.update_attendance_record(
                        message.author.id,
                        date=date.today(),
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Attendance(bot))
