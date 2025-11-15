from configs.path import PathConfig


class LogFileConfig:
    FILE_NAME = "log-data.log"
    FILE_ADDRESS = PathConfig.LOG_DIR / FILE_NAME
    FILE_ENCODING = "utf-8"
