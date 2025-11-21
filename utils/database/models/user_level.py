from sqlalchemy import Column, BigInteger, Integer, Date, UniqueConstraint

from ..db_main import Base


class UserLevel(Base):
    __tablename__ = "user_level"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, nullable=False)
    discord_id = Column(BigInteger, nullable=False)
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint("guild_id", "discord_id", name="uq_guild_discord"),
    )
