from sqlalchemy import Column, BigInteger, Integer, String
from ..db import Base


class GuildTTSChannel(Base):
    __tablename__ = "guild_tts_channel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    channel_lang = Column(String(5), nullable=False, default="ko")
