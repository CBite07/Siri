from contextlib import contextmanager
from typing import Generator, Optional, Any
from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from .db import SessionLocal
from .models.user_attendance import UserAttendance


class AttendanceDBUtil:
    @staticmethod
    @contextmanager
    def _get_session() -> Generator[Session, None, None]:
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    @staticmethod
    def upsert_attendance_data(discord_id: int, date: date, streak: int, most_streak: int) -> None:
        with AttendanceDBUtil._get_session() as db_session:
            insert_statement = (
                insert(UserAttendance)
                .values(
                    discord_id=discord_id,
                    date=date,
                    streak=streak,
                    most_streak=most_streak
                )
            )
            
            upsert_statement = (
                insert_statement.on_duplicate_key_update(
                    discord_id=discord_id,
                    date=date,
                    streak=streak,
                    most_streak=most_streak
                )
            )

            try:
                db_session.execute(upsert_statement)
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise

    @staticmethod
    def read_attendance_data(discord_id: int) -> Optional[dict[str, Any]]:
        with AttendanceDBUtil._get_session() as db_session:
            user_to_read = (
                db_session.query(UserAttendance)
                .filter(UserAttendance.discord_id == discord_id)
                .first()
            )

            if user_to_read:
                return {
                    "discord_id": user_to_read.discord_id,
                    "date": user_to_read.date,
                    "streak": user_to_read.streak,
                    "most_streak": user_to_read.most_streak
                }
            return None

    @staticmethod
    def delete_attendance_date(discord_id: int) -> Optional[dict[str, Any]]:
        with AttendanceDBUtil._get_session() as db_sesion:
            user_to_delete = (
                db_sesion.query(UserAttendance)
                .filter(UserAttendance.discord_id == discord_id)
                .first()
            )

            if user_to_delete:
                try:
                    db_sesion.delete(user_to_delete)
                    db_sesion.commit()
                except Exception:
                    db_sesion.rollback()
                    raise