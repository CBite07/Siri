from utils.configs.path import PathConfig


class LogConfig:
    LOGGER_NAME = "siri_logger"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE_PATH = PathConfig.LOG_DIR / "siri_bot.log"
    BACKUP_FILE_SIZE = 10 * 10 * 1024
    BACKUP_FILE_COUNT = 5
    BACKUP_FILE_ENCODING = "utf-8"
