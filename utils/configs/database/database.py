from utils.configs.env import EnvConfig

class DBConfig:
    DB_NAME = EnvConfig.DB_NAME
    DB_USER = EnvConfig.DB_USER
    DB_PASSWORD = EnvConfig.DB_PASSWD
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_CHARSET = "utf8mb4"
    DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
