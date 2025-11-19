import os
from dotenv import load_dotenv

load_dotenv()


# Environment configuration class
class EnvConfig:
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    BOT_COMMAND_PREFIX = os.getenv("DISCORD_COMMAND_PREFIX")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWD = os.getenv("DB_PASSWORD")
