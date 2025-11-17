# import logging module, path config for file path
import logging
from utils.configs.path import PathConfig

# create log file system path
# /logs/siri_bot.log
log_file_path = PathConfig.LOG_DIR / "siri_bot.log"

# configure logger
logger = logging.getLogger("siri_logger")
logger.setLevel(logging.DEBUG)

# create console, file handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")

# set formatter
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# set console, file handlers to formatter
console_handler.setFormatter(format)
file_handler.setFormatter(format)

# file write everything, console only warning and above
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
