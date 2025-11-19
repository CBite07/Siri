# import db session, table model module
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from contextlib import contextmanager
from typing import Generator, Optional
from datetime import date
from .db import SessionLocal
from .models.user_points import UserPoints
from .models.user_attendance import UserAttendance


# DB util class
class DBUtils:
    # Provides a SQLAlchemy Session object and automatically closes it upon exit.
    @staticmethod
    @contextmanager
    def _get_session() -> Generator[Session, None, None]:
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    # Creates and adds a new UserPoints record for the given Discord ID.
    @staticmethod
    def create_user_point_record(discord_id: int) -> None:
        with DBUtils._get_session() as db_session:
            new_user_record = UserPoints(discord_id=discord_id)
            db_session.add(new_user_record)
            try:
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise

    # Retrieves the experience (exp) of a user by Discord ID.
    @staticmethod
    def read_user_exp_record(discord_id: int) -> Optional[int]:
        with DBUtils._get_session() as db_session:
            user_exp = (
                db_session.query(UserPoints.exp)
                .filter(UserPoints.discord_id == discord_id)
                .scalar()
            )
            return user_exp

    # Retrieves the level of a user by Discord ID.
    @staticmethod
    def read_user_level_record(discord_id: int) -> Optional[int]:
        with DBUtils._get_session() as db_session:
            user_level = (
                db_session.query(UserPoints.level)
                .filter(UserPoints.discord_id == discord_id)
                .scalar()
            )
            return user_level

    # Updates the experience (exp) information for a user.
    @staticmethod
    def update_user_exp(discord_id: int, *, exp: int) -> None:
        with DBUtils._get_session() as db_session:
            user_to_update = (
                db_session.query(UserPoints)
                .filter(UserPoints.discord_id == discord_id)
                .first()
            )
            if user_to_update:
                try:
                    user_to_update.exp = exp
                    db_session.commit()
                except Exception:
                    db_session.rollback()
                    raise

    # Updates the level information for a user.
    @staticmethod
    def update_user_level(discord_id: int, *, level: int) -> None:
        with DBUtils._get_session() as db_session:
            user_to_update = (
                db_session.query(UserPoints)
                .filter(UserPoints.discord_id == discord_id)
                .first()
            )
            if user_to_update:
                try:
                    user_to_update.level = level
                    db_session.commit()
                except Exception:
                    db_session.rollback()
                    raise

    # Deletes a UserPoints record by Discord ID.
    @staticmethod
    def delete_user_point_record(discord_id: int) -> None:
        with DBUtils._get_session() as db_session:
            user_to_delete = (
                db_session.query(UserPoints)
                .filter(UserPoints.discord_id == discord_id)
                .first()
            )
            if user_to_delete:
                try:
                    db_session.delete(user_to_delete)
                    db_session.commit()
                except Exception:
                    db_session.rollback()
                    raise

    # Checks if an attendance record exists for the given Discord ID and date.
    @staticmethod
    def read_attendanced_date_record(discord_id: int, date: date) -> Optional[date]:
        with DBUtils._get_session() as db_session:
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
        with DBUtils._get_session() as db_session:
            streak_value = (
                db_session.query(UserAttendance.streak)
                .filter(UserAttendance.discord_id == discord_id)
                .scalar()
            )
            return streak_value

    # Inserts an attendance record or updates the streak if a record already exists (Upsert).
    @staticmethod
    def update_attendance_record(discord_id: int, *, date: date, streak: int) -> None:
        with DBUtils._get_session() as db_session:
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
