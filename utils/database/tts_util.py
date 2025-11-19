# import db session, table model module
from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from contextlib import contextmanager
from typing import Generator, Optional
from datetime import date
from .db import SessionLocal
from .models.guild_tts_channel import GuildTTSChannel


# DB util class
class TTSDBUtil:
    # Provides a SQLAlchemy Session object and automatically closes it upon exit.
    @staticmethod
    @contextmanager
    def _get_session() -> Generator[Session, None, None]:
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    @staticmethod
    def create_guild_tts_channel(guild_id: int, channel_id: int) -> None:
        with TTSDBUtil._get_session() as db_session:
            new_channel_record = GuildTTSChannel(
                guild_id=guild_id, channel_id=channel_id
            )
            try:
                db_session.add(new_channel_record)
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise

    @staticmethod
    def read_guild_tts_channel(guild_id: int) -> Optional[int]:
        with TTSDBUtil._get_session() as db_session:
            existing_channel_id = (
                db_session.query(GuildTTSChannel.channel_id)
                .filter(GuildTTSChannel.guild_id == guild_id)
                .all()
            )
            return existing_channel_id

    @staticmethod
    def update_channel_tts_lang(guild_id: int, channel_id: int, lang: str) -> None:
        with TTSDBUtil._get_session() as db_session:
            try:
                db_session.query(GuildTTSChannel)\
                    .filter(
                    GuildTTSChannel.guild_id == guild_id,
                    GuildTTSChannel.channel_id == channel_id
                )\
                .update({GuildTTSChannel.channel_lang: lang})
                db_session.commit()
            except Exception:
                db_session.rollback()

    @staticmethod
    def delete_guild_tts_channel(guild_id: int, channel_id: int) -> None:
        with TTSDBUtil._get_session() as db_session:
            channel_to_delete = (
                db_session.query(GuildTTSChannel)
                .filter(
                    GuildTTSChannel.guild_id == guild_id,
                    GuildTTSChannel.channel_id == channel_id,
                )
                .all()
            )
            if channel_to_delete:
                try:
                    db_session.delete(channel_to_delete)
                    db_session.commit()
                except Exception:
                    db_session.rollback()
