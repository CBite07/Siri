from sqlalchemy import Column, BigInteger, Integer, Date

from ..db import Base


class UserLevel(Base):
    __tablename__ = "user_level"

    discord_id = Column(BigInteger, primary_key=True)
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(Date, nullable=False)
