from typing import Optional, Any
from datetime import date

from sqlalchemy import select, delete
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
            stmt = select(UserAttendance).where(
                UserAttendance.guild_id == guild_id,
                UserAttendance.discord_id == discord_id,
            )

            user = db_session.scalars(stmt).first()

            if user:
                return {
                    "discord_id": user.discord_id,
                    "date": user.date,
                    "streak": user.streak,
                    "most_streak": user.most_streak,
                }
            return None

    @staticmethod
    def delete_attendance_date(guild_id: int, discord_id: int) -> None:
        with get_db_session() as db_session:
            stmt = delete(UserAttendance).where(
                UserAttendance.guild_id == guild_id,
                UserAttendance.discord_id == discord_id,
            )

            db_session.execute(stmt)
