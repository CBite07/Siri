from sqlalchemy import Column, BigInteger, String

from ..db import Base


class GuildTTSChannel(Base):
    __tablename__ = "guild_tts_channel"

    guild_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, nullable=False)
    channel_lang = Column(String(5), nullable=False, default="ko")
