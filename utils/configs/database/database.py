class DBConfig:
    DB_USER = "siri_db_manager"
    DB_PASSWORD = "siri_db_manager"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_DB_NAME = "siri_db"
    DB_CHARSET = "utf8mb4"
    DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB_NAME}?charset={DB_CHARSET}"
