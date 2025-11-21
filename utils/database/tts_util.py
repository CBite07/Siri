from typing import Generator, List, Dict, Any

from sqlalchemy.dialects.mysql import insert
from sqlalchemy import select, delete

from .db_main import get_db_session
from .models.guild_tts_channel import GuildTTSChannel


class TTSDBUtil:
    @staticmethod
    def upsert_tts_channel(guild_id: int, channel_id: int, channel_lang: str) -> None:
        with get_db_session() as db_session:
            insert_stmt = insert(GuildTTSChannel).values(
                guild_id=guild_id,
                channel_id=channel_id,
                channel_lang=channel_lang,
            )

            upsert_stmt = insert_stmt.on_duplicate_key_update(channel_lang=channel_lang)

            db_session.execute(upsert_stmt)

    @staticmethod
    def read_tts_data(guild_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db_session:
            stmt = select(GuildTTSChannel).where(GuildTTSChannel.guild_id == guild_id)

            channels = db_session.scalars(stmt).all()

            if channels:
                return [
                    {
                        "channel_id": channel.channel_id,
                        "channel_lang": channel.channel_lang,
                    }
                    for channel in channels
                ]
            return []

    @staticmethod
    def delete_guild_tts_channel(guild_id: int, channel_id: int) -> None:
        with get_db_session() as db_session:
            stmt = db_session.delete(GuildTTSChannel).where(
                GuildTTSChannel.guild_id == guild_id,
                GuildTTSChannel.channel_id == channel_id,
            )
            db_session.execute(stmt)
