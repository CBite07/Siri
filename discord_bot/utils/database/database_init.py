import sqlite3


def init_db(db_path="database.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_points (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            points INTEGER DEFAULT 1,
            levels INTEGER DEFAULT 2
        )
        """
    )

    conn.commit()
    conn.close()
