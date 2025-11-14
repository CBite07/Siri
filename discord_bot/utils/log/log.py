from discord_bot.utils.time import get_formatted_time


def print_formatted_log(status: str, module: str, message: str) -> str:
    current_time = get_formatted_time()
    status_str = f"{status:<8}"  # 8칸 왼쪽 정렬
    print(f"{current_time} {status_str} {module} {message}")
