from pathlib import Path


class PathConfig:
    ROOT_DIR = Path(__file__).parent.parent.parent

    DISCORD_DIR = ROOT_DIR / "discord_bot"
    DISCORD_CONFIG_DIR = DISCORD_DIR / "configs"
    DISCORD_UTIL_DIR = DISCORD_DIR / "utils"
    DISCORD_COG_DIR = DISCORD_DIR / "cogs"

    CONFIG_DIR = ROOT_DIR / "condigs"