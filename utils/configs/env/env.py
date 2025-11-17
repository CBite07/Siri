import os
from dotenv import load_dotenv

load_dotenv()


# Environment configuration class
# code review result: good use of dotenv to manage env variables.
class EnvConfig:
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    BOT_COMMAND_PREFIX = os.getenv("DISCORD_COMMAND_PREFIX")
