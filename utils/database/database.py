import sqlite3


class DBManager:
    def __init__(self, db_path="database.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def fetch_points(self, user_id):
        self.cursor.execute(
            "SELECT points FROM user_points WHERE user_id = ?", (user_id,)
        )
        row = self.cursor.fetchall()
        return row[0] if row else -1

    def fetch_levels(self, user_id):
        self.cursor.execute(
            "SELECT levels FROM user_points WHERE user_id = ?", (user_id,)
        )
        row = self.cursor.fetchall()
        return row[0] if row else -1

    def add_user(self, user_id, points=0, level=1):
        self.cursor.execute(
            "INSERT OR IGNORE INTO user_points (user_id, points, levels) VALUES (?, ?, ?)",
            (user_id, points, level),
        )
        self.conn.commit()


db = DBManager()
