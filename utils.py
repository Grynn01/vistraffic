from datetime import timedelta


def seconds_to_minutes(seconds):
    return seconds / 60


def minutes_to_seconds(minutes):
    return minutes * 60


def adjust_to_server_datetime(datetime):
    return datetime + timedelta(hours=4)


def add_one_day(datetime):
    return datetime + timedelta(days=1)
