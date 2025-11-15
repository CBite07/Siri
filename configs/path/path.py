from pathlib import Path


class PathConfig:
    ROOT_DIR = Path(__file__).parent.parent.parent

    DISCORD_DIR = ROOT_DIR / "discord_bot"
    DISCORD_CONFIG_DIR = DISCORD_DIR / "configs"
    DISCORD_UTIL_DIR = DISCORD_DIR / "utils"
    DISCORD_COG_DIR = DISCORD_DIR / "cogs"
    DISCORD_RUN_FILE = "discord_bot.run"
    COGS = ["discord_bot.cogs.test.test"]

    CONFIG_DIR = ROOT_DIR / "configs"

    LOG_DIR = ROOT_DIR / "logs"
