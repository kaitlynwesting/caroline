from datetime import datetime, timedelta, timezone
import pytz

# This time converter offers three functions for easy time handling.
# time_to_int: converts time input to seconds for asyncio.sleep, e.g. 1m -> 60
# time_to_string: converts time input to words for ease of reading, e.g. 1m -> 1 minute
# time_to_date: adds time input to current time for reading future date


def channel_message_spanner(
    channel,
    message_limit,
    time_increment,
    message_content
):

    async for message in channel.history(limit=message_limit):

        if message_content in message.content:
            message_time = pytz.utc.localize(message.created_at)
            time_now = datetime.now(pytz.utc)
            time_difference = time_now - message_time

            # if time_difference > timedelta(hours=24):
