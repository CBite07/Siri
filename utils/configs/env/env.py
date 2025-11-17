import os
from dotenv import load_dotenv

load_dotenv()

class EnvConfig:
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    BOT_COMMAND_PREFIX = os.getenv("DISCORD_COMMAND_PREFIX")
