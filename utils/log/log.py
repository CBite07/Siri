import logging
from logging.handlers import RotatingFileHandler
from utils.configs.log import LogConfig

formatter = logging.Formatter(LogConfig.LOG_FORMAT)

logger = logging.getLogger(LogConfig.LOGGER_NAME)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()

file_handler = RotatingFileHandler(
    filename=LogConfig.LOG_FILE_PATH,
    maxBytes=LogConfig.BACKUP_FILE_SIZE,
    backupCount=LogConfig.BACKUP_FILE_COUNT,
    encoding=LogConfig.BACKUP_FILE_ENCODING,
)

console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
