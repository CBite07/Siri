from sqlalchemy import Column, BigInteger, String, UniqueConstraint
from ..db import Base


class GuildTTSChannel(Base):
    __tablename__ = "guild_tts_channel"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    channel_lang = Column(String(5), nullable=False, default="ko")

    __table_args__ = (
        UniqueConstraint("guild_id", "channel_id", name="uq_guild_channel_pair"),
    )
