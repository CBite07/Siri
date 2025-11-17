from pathlib import Path


class PathConfig:
    ROOT_DIR = Path(__file__).parent.parent.parent

    DISCORD_BOT_DIR = ROOT_DIR / "bot_src"
    DISCORD_COG_DIR = DISCORD_BOT_DIR / "cogs"
    CONFIG_DIR = DISCORD_BOT_DIR / "configs"
    UTIL_DIR = DISCORD_BOT_DIR / "utils"
    DISCORD_RUN_FILE = "bot_src.run"
    COGS = ["bot_src.cogs.test.test"]

    CONFIG_DIR = ROOT_DIR / "configs"

    LOG_DIR = ROOT_DIR / "logs"
