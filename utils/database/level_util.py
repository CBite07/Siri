from datetime import date
from typing import Generator, Optional, Dict, Any
from contextlib import contextmanager

from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert

from .db_main import SessionLocal
from .models.user_level import UserLevel


class LevelDBUtil:

    @staticmethod
    @contextmanager
    def _get_session() -> Generator[Session, None, None]:
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    @staticmethod
    def upsert_level_data(
        guild_id: int, discord_id: int, exp: int, level: int, created_at: date
    ) -> None:
        with LevelDBUtil._get_session() as db_session:
            insert_statement = insert(UserLevel).values(
                guild_id=guild_id,
                discord_id=discord_id,
                exp=exp,
                level=level,
                created_at=created_at,
            )

            upsert_statement = insert_statement.on_duplicate_key_update(
                exp=exp, level=level
            )

            try:
                db_session.execute(upsert_statement)
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise

    @staticmethod
    def read_level_data(guild_id: int, discord_id: int) -> Optional[Dict[str, Any]]:
        with LevelDBUtil._get_session() as db_session:
            user_to_read = (
                db_session.query(UserLevel)
                .filter(
                    UserLevel.guild_id == guild_id, UserLevel.discord_id == discord_id
                )
                .first()
            )

            if user_to_read:
                return {
                    "guild_id": user_to_read.guild_id,
                    "discord_id": user_to_read.discord_id,
                    "exp": user_to_read.exp,
                    "level": user_to_read.level,
                    "created_at": user_to_read.created_at,
                }
            return None

    @staticmethod
    def delete_level_data(guild_id: int, discord_id: int) -> None:
        with LevelDBUtil._get_session() as db_session:
            user_to_delete = (
                db_session.query(UserLevel)
                .filter(
                    UserLevel.guild_id == guild_id, UserLevel.discord_id == discord_id
                )
                .first()
            )

            if user_to_delete:
                try:
                    db_session.delete(user_to_delete)
                    db_session.commit()
                except Exception:
                    db_session.rollback()
                    raise
