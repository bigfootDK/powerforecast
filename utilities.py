import datetime

today = datetime.date.today()


def parse_time(time_string):
    """
    format: yyyy:mm:dd hh:mm:ss.000000
    """
    if time_string[5] == '0':
        month = time_string[6]
    else:
        month = time_string[5:7]
    if time_string[8] == '0':
        day = time_string[9]
    else:
        day = time_string[8:10]

    return [int(time_string[:4]), int(month), int(day)]


def date2delta(date):
    """
    date: list - [year, month, day]
    """
    timedelta = today - datetime.date(date[0], date[1], date[2])
    return timedelta.days


def delta2date(delta):
    return today - datetime.timedelta(delta)
