from .db import SessionLocal
from .models.user_points import UserPoints


class DBUtils:
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

    @staticmethod
    def update_point(discord_id: int):
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
