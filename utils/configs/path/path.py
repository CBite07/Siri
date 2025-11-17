from pathlib import Path


# Path configuration class
# code review result: there was two CONFIG_DIR definitons.
class PathConfig:
    ROOT_DIR = Path(__file__).parent.parent.parent.parent

    DISCORD_RUN_FILE = "bot_src.run"
    DISCORD_BOT_DIR = ROOT_DIR / "bot_src"
    CONFIG_DIR = DISCORD_BOT_DIR / "configs"
    UTIL_DIR = DISCORD_BOT_DIR / "utils"

    DISCORD_COG_DIR = DISCORD_BOT_DIR / "cogs"
    COGS = [
        "bot_src.cogs.db_tester",
    ]  # list of cog module paths

    DATA_DIR = ROOT_DIR / "data"
    LOG_DIR = DATA_DIR / "logs"
