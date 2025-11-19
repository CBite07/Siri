# import db session, table model module
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from contextlib import contextmanager
from typing import Generator, Optional
from datetime import date
from .db import SessionLocal
from .models.user_attendance import UserAttendance


# DB util class
class AttendanceDBUtil:
    # Provides a SQLAlchemy Session object and automatically closes it upon exit.
    @staticmethod
    @contextmanager
    def _get_session() -> Generator[Session, None, None]:
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    # Checks if an attendance record exists for the given Discord ID and date.
    @staticmethod
    def read_attendanced_date_record(discord_id: int, date: date) -> Optional[date]:
        with AttendanceDBUtil._get_session() as db_session:
            existing_date = (
                db_session.query(UserAttendance.date)
                .filter(
                    UserAttendance.discord_id == discord_id,
                    UserAttendance.date == date,
                )
                .scalar()
            )
            return existing_date

    # Retrieves the current attendance streak value for a user.
    @staticmethod
    def read_attendance_streak_record(discord_id: int) -> Optional[int]:
        with AttendanceDBUtil._get_session() as db_session:
            streak_value = (
                db_session.query(UserAttendance.streak)
                .filter(UserAttendance.discord_id == discord_id)
                .scalar()
            )
            return streak_value

    # Inserts an attendance record or updates the streak if a record already exists (Upsert).
    @staticmethod
    def update_attendance_record(discord_id: int, *, date: date, streak: int) -> None:
        with AttendanceDBUtil._get_session() as db_session:
            upsert_stmt = (
                insert(UserAttendance)
                .values(discord_id=discord_id, date=date, streak=streak)
                .on_duplicate_key_update(streak=streak)
            )
            try:
                db_session.execute(upsert_stmt)
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise
