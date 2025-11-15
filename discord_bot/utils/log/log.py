from discord_bot.configs.log import LogStatusConfig 
from discord_bot.utils.time import get_formatted_time

status_keymap = LogStatusConfig.STATUS_KEYMAP
status_length = LogStatusConfig.STATUS_LENGTH

def print_formatted_log(status: str, module: str, message: str):
    current_time = get_formatted_time()
    try:
        status_str = f"{status_keymap[status]:<{status_length}}"
    except KeyError:
        status_str = f"{'NO KEYMAP':<{status_length}}"
    print(f"{current_time} {status_str} {module} {message}")


def print_cog_error_log(module: str, function: str, error: Exception):
    current_time = get_formatted_time()
    try:   
        status = "error"
        status_str = f"{status_keymap[status]:<{status_length}}"
    except KeyError:
        status_str = f"{'NO KEYMAP':<{status_length}}"
    message = f"'{function}' has raised an error: {str(error)}"
    print(f"{current_time} {status_str} {module} {message}")