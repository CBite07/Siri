# import db session, table model module
from .db import SessionLocal
from .models.user_points import UserPoints
from .models.user_attendance import UserAttendance

from sqlalchemy.dialects.mysql import insert


# DB util class
class DBUtils:
    # get user by discord ID
    @staticmethod
    def get_user(discord_it: int):
        db = SessionLocal()
        try:
            user = (
                db.query(UserPoints).filter(UserPoints.discord_id == discord_it).first()
            )
            return user
        finally:
            db.close()

    # delete row by discord ID
    @staticmethod
    def delete_user(discord_id: int):
        db = SessionLocal()
        try:
            user = (
                db.query(UserPoints).filter(UserPoints.discord_id == discord_id).first()
            )
            if user:
                db.delete(user)
                db.commit()
            return user
        finally:
            db.close()

    # add new user by discord ID
    @staticmethod
    def add_user(discord_id: int):
        db = SessionLocal()
        try:
            new_user = UserPoints(discord_id=discord_id)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        finally:
            db.close()

    @staticmethod
    def get_user_points(discord_id: int):
        db = SessionLocal()
        try:
            user = (
                db.query(UserPoints).filter(UserPoints.discord_id == discord_id).first()
            )
            if user:
                return user.exp, user.level
            return None
        finally:
            db.close()

    # update user points by discord ID(Also add if there's no such user. but not nessecary)
    @staticmethod
    def update_user_points(discord_id: int, exp: int, level: int):
        db = SessionLocal()
        try:
            user = (
                db.query(UserPoints).filter(UserPoints.discord_id == discord_id).first()
            )
            if user:
                user.exp = exp
                user.level = level
                db.commit()
                db.refresh(user)
            return user
        finally:
            db.close()

    @staticmethod
    def get_user_attendanced_date(discord_id: int, date):
        db = SessionLocal()
        try:
            attendanced_date = (
                db.query(UserAttendance.date)
                .filter(
                    UserAttendance.discord_id == discord_id,
                    UserAttendance.date == date,
                )
                .first()
            )
            return attendanced_date
        finally:
            db.close()

    @staticmethod
    def get_user_streak(discord_id: int):
        db = SessionLocal()
        try:
            attendance = (
                db.query(UserAttendance.streak)
                .filter(
                    UserAttendance.discord_id == discord_id,
                )
                .first()
            )
            return attendance
        finally:
            db.close()

    @staticmethod
    def update_user_attendance(discord_id: int, date, streak: int):
        db = SessionLocal()
        try:
            stmt = (
                insert(UserAttendance)
                .values(discord_id=discord_id, date=date, streak=streak)
                .on_duplicate_key_update(streak=streak)
            )
            db.execute(stmt)
            db.commit()
        finally:
            db.close()
