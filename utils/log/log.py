from utils.configs.log import LogStatusConfig, LogFileConfig
from utils.time import get_formatted_time

status_keymap = LogStatusConfig.STATUS_KEYMAP
status_length = LogStatusConfig.STATUS_LENGTH
file_address = LogFileConfig.FILE_ADDRESS
file_encoding = LogFileConfig.FILE_ENCODING


def _write_to_file(log: str):
    file_address.parent.mkdir(parents=True, exist_ok=True)
    with open(file_address, "a", encoding=file_encoding) as f:
        f.write(f"{log}\n")


def _format_status(status: str, length: int) -> str:
    return f"{status:<{length}}"


def print_log(status: str, module: str, message: str):
    current_time = get_formatted_time()
    try:
        status_str = _format_status(status_keymap[status], status_length)
    except KeyError:
        status_str = _format_status("NO KEYMAP", status_length)

    log = f"{current_time} {status_str} {module} {message}"
    print(log)
    _write_to_file(log)


def print_error_log(module: str, function: str, error: Exception):
    current_time = get_formatted_time()
    try:
        status = "error"
        status_str = _format_status(status_keymap[status], status_length)
    except KeyError:
        status_str = _format_status("NO KEYMAP", status_length)
    message = f"'{function}' has raised an error: {str(error)}"

    log = f"{current_time} {status_str} {module} {message}"
    print(log)
    _write_to_file(log)


def print_db_success_log(module: str, table_name: str, id: int):
    current_time = get_formatted_time()
    try:
        status = "success"
        status_str = _format_status(status_keymap[status], status_length)
    except KeyError:
        status_str = _format_status("NO KEYMAP", status_length)
    message = f"data writed successfully at {table_name}:{id}"

    log = f"{current_time} {status_str} {module} {message}"
    print(log)
    _write_to_file(log)
