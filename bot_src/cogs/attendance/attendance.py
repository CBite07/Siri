import discord
from discord import app_commands
from discord.ext import commands

from datetime import date, timedelta
from typing import Optional, Dict, Any
from random import randint

from utils.log import logger
from utils.database import LevelDBUtil, AttendanceDBUtil
from utils.level import LevelUtil


class Attendance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_attendance_data(
        self, guild_id: int, discord_id: int
    ) -> Optional[Dict[str, Any]]:
        return AttendanceDBUtil.read_attendance_data(guild_id, discord_id)

    def _is_attendanceable(self, guild_id: int, discord_id: int) -> bool:
        attendance_data = self._get_attendance_data(guild_id, discord_id)

        if attendance_data is None:
            return True

        last_date: date = attendance_data["date"]
        return last_date < date.today()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user and not message.guild:
            return

        if message.content.strip() == "ㅊㅊ":
            if self._is_attendanceable(message.guild.id, message.author.id):
                guild = message.guild
                user = message.author

                yesterday = date.today() - timedelta(days=1)

                attendance_data = AttendanceDBUtil.read_attendance_data(
                    guild.id, user.id
                )
                level_data = LevelDBUtil.read_level_data(guild.id, user.id)

                current_exp = level_data.get("exp", 0) if level_data else 0
                current_streak = (
                    attendance_data.get("streak", 0) if attendance_data else 0
                )
                current_most_streak = (
                    attendance_data.get("most_streak", 0) if attendance_data else 0
                )
                current_attendance_date = (
                    attendance_data.get("date", 0) if attendance_data else 0
                )

                new_exp = current_exp + randint(700, 1000)
                new_level = LevelUtil.exp_to_level(new_exp)
                new_streak = (
                    current_streak + 1 if current_attendance_date == yesterday else 1
                )
                new_most_streak = max(current_most_streak, new_streak)

                try:
                    LevelDBUtil.upsert_level_data(
                        guild_id=guild.id,
                        discord_id=user.id,
                        exp=new_exp,
                        level=new_level,
                        created_at=(
                            level_data.get("created_at", date.today())
                            if level_data
                            else date.today()
                        ),
                    )

                    AttendanceDBUtil.upsert_attendance_data(
                        guild_id=guild.id,
                        discord_id=user.id,
                        attendance_date=date.today(),
                        streak=new_streak,
                        most_streak=new_most_streak,
                    )

                    reaction = "✅"
                    logger.info(
                        f"Attendance recorded for user: {message.author} (ID: {message.author.id}). New Streak: {new_streak}"
                    )
                except Exception as e:
                    reaction = "❌"
                    logger.error(
                        f"Failed to record attendance for user: {message.author} (ID: {message.author.id}). Error: {e}"
                    )
                await message.add_reaction(reaction)
            else:
                print("x")
                await message.add_reaction("❌")


async def setup(bot: commands.Bot):
    await bot.add_cog(Attendance(bot))
