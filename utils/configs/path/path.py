from pathlib import Path


# Path configuration class
class PathConfig:
    ROOT_DIR = Path(__file__).parent.parent.parent.parent

    DISCORD_RUN_FILE = "bot_src.run"
    DISCORD_BOT_DIR = ROOT_DIR / "bot_src"
    UTIL_DIR = ROOT_DIR / "utils"
    CONFIG_DIR = UTIL_DIR / "configs"

    DISCORD_COG_DIR = DISCORD_BOT_DIR / "cogs"
    COGS = [
        "bot_src.cogs.attendance.attendance",
        "bot_src.cogs.voice.voice",
        "bot_src.cogs.voice.tts",
        "bot_src.cogs.information.information"
    ]

    DATA_DIR = ROOT_DIR / "data"
    LOG_DIR = DATA_DIR / "logs"
