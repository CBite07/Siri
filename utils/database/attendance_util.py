from typing import Optional, Any
from datetime import date

from sqlalchemy import delete
from sqlalchemy.dialects.mysql import insert

from .db_main import get_db_session
from .models.user_attendance import UserAttendance


class AttendanceDBUtil:
    @staticmethod
    def upsert_attendance_data(
        guild_id: int,
        discord_id: int,
        attendance_date: date,
        streak: int,
        most_streak: int,
    ) -> None:
        with get_db_session() as db_session:
            insert_stmt = insert(UserAttendance).values(
                guild_id=guild_id,
                discord_id=discord_id,
                date=attendance_date,
                streak=streak,
                most_streak=most_streak,
            )

            upsert_stmt = insert_stmt.on_duplicate_key_update(
                discord_id=discord_id,
                date=attendance_date,
                streak=streak,
                most_streak=most_streak,
            )

            db_session.execute(upsert_stmt)

    @staticmethod
    def read_attendance_data(
        guild_id: int, discord_id: int
    ) -> Optional[dict[str, Any]]:
        with get_db_session() as db_session:
            user_to_read = (
                db_session.query(UserAttendance)
                .filter(
                    UserAttendance.guild_id == guild_id,
                    UserAttendance.discord_id == discord_id,
                )
                .first()
            )

            if user_to_read:
                return {
                    "discord_id": user_to_read.discord_id,
                    "date": user_to_read.date,
                    "streak": user_to_read.streak,
                    "most_streak": user_to_read.most_streak,
                }
            return None

    @staticmethod
    def delete_attendance_date(guild_id: int, discord_id: int) -> None:
        with get_db_session() as db_session:
            delete_stmt = delete(UserAttendance).where(
                UserAttendance.guild_id == guild_id,
                UserAttendance.discord_id == discord_id,
            )

            db_session.execute(delete_stmt)
