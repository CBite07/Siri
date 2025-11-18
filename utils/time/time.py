from datetime import datetime


# get the current date and time
def get_time():
    return datetime.now()


# get the current date and time as a formatted string
def get_formatted_time():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time
