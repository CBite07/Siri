from datetime import datetime


def get_time():
    return datetime.now()


def get_formatted_time():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time
