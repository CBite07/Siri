import logging

from utils.configs.path import PathConfig

log_file_path = PathConfig.LOG_DIR / "siri_bot.log" 

logger = logging.getLogger("siri_logger")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")

format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(format)
file_handler.setFormatter(format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)