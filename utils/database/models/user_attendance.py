from sqlalchemy import Column, BigInteger, Date, Integer
from utils.database.db import Base


class UserAttendance(Base):
    __tablename__ = "user_attendance"

    discord_id = Column(BigInteger, primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    streak = Column(Integer, default=0)


"""
+---------+------------+------+-----+---------+-------+
| Field   | Type       | Null | Key | Default | Extra |
+---------+------------+------+-----+---------+-------+
| user_id | bigint(20) | NO   | PRI | NULL    |       |
| date    | date       | NO   | PRI | NULL    |       |
| streaks | int(11)    | YES  |     | NULL    |       |
+---------+------------+------+-----+---------+-------+
"""
