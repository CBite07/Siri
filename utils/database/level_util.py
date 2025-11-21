from datetime import date
from typing import Optional, Dict, Any

from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select, delete

from .db_main import get_db_session
from .models.user_level import UserLevel


class LevelDBUtil:
    @staticmethod
    def upsert_level_data(
        guild_id: int, discord_id: int, exp: int, level: int, created_at: date
    ) -> None:
        with get_db_session() as db_session:
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

            db_session.execute(upsert_statement)

    @staticmethod
    def read_level_data(guild_id: int, discord_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db_session:
            stmt = select(UserLevel).where(
                UserLevel.guild_id == guild_id, UserLevel.discord_id == discord_id
            )

            user = db_session.scalars(stmt).first()

            if user:
                return {
                    "guild_id": user.guild_id,
                    "discord_id": user.discord_id,
                    "exp": user.exp,
                    "level": user.level,
                    "created_at": user.created_at,
                }
            return None

    @staticmethod
    def delete_level_data(guild_id: int, discord_id: int) -> None:
        with get_db_session() as db_session:
            stmt = delete(UserLevel).where(
                UserLevel.guild_id == guild_id, UserLevel.discord_id == discord_id
            )
            db_session.execute(stmt)
