import datetime, pytz


def get_utc_datetime():
    return datetime.datetime.now(tz=pytz.utc)
