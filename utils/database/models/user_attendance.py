from sqlalchemy import Column, BigInteger, Date, Integer

from ..db import Base


class UserAttendance(Base):
    __tablename__ = "user_attendance"

    discord_id = Column(BigInteger, primary_key=True)
    date = Column(Date, nullable=False)
    streak = Column(Integer, default=0)
    most_streak = Column(Integer, default=0)
