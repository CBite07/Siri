from sqlalchemy.orm import Session
from sqlalchemy.dialects.mysql import insert
from contextlib import contextmanager
from typing import Generator, Optional, List, Dict, Any
from .db import SessionLocal
from .models.guild_tts_channel import GuildTTSChannel


class TTSDBUtil:
    @staticmethod
    @contextmanager
    def _get_session() -> Generator[Session, None, None]:
        db_session = SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    @staticmethod
    def read_tts_data(guild_id: int) -> List[Dict[str, Any]]:
        with TTSDBUtil._get_session() as db_session:
            records = (
                db_session.query(GuildTTSChannel)
                .filter(GuildTTSChannel.guild_id == guild_id)
                .all()
            )
            if records:
                return [
                    {"channel_id": r.channel_id, "channel_lang": r.channel_lang}
                    for r in records
                ]
            return []

    @staticmethod
    def upsert_tts_channel(guild_id: int, channel_id: int, lang: str) -> None:
        insert_stmt = insert(GuildTTSChannel).values(
            guild_id=guild_id,
            channel_id=channel_id,
            channel_lang=lang,
        )
        upsert_stmt = insert_stmt.on_duplicate_key_update(channel_lang=lang)
        with TTSDBUtil._get_session() as db_session:
            try:
                db_session.execute(upsert_stmt)
                db_session.commit()
            except Exception:
                db_session.rollback()
                raise

    @staticmethod
    def delete_guild_tts_channel(guild_id: int, channel_id: int) -> None:
        with TTSDBUtil._get_session() as db_session:
            channel_to_delete = (
                db_session.query(GuildTTSChannel)
                .filter(
                    GuildTTSChannel.guild_id == guild_id,
                    GuildTTSChannel.channel_id == channel_id,
                )
                .first()
            )
            if channel_to_delete:
                try:
                    db_session.delete(channel_to_delete)
                    db_session.commit()
                except Exception:
                    db_session.rollback()
                    raise
