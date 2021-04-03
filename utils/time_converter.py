from datetime import datetime, timedelta, timezone


# This time converter offers three functions for easy time handling.
# time_to_int: converts time input to seconds for asyncio.sleep, e.g. 1m -> 60
# time_to_string: converts time input to words for ease of reading, e.g. 1m -> 1 minute
# time_to_date: adds time input to current time for reading future date


def time_to_int(
        time: str
) -> int:

    time_to_seconds = {"s": 1, "m": 60, "h": 3600, "d": 86400}

    return int(time[:-1]) * time_to_seconds[time[-1]]


def time_to_string(
        time: str
) -> str:

    time_to_words = {"s": "second", "m": "minute", "h": "hour", "d": "day"}

    if int(time[:-1]) != 1:
        return f"{time[:-1]} {time_to_words[time[-1]]}s"
    else:
        return f"{time[:-1]} {time_to_words[time[-1]]}"


def time_to_date(
        time: str
):

    time_increment = timedelta(seconds=time_to_int(time))

    time_future = datetime.now(tz=timezone.utc) + time_increment

    return time_future.strftime('%Y-%m-%d %H:%M:%S')
