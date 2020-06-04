MIN_MINUTE_A_DAY = 0
MAX_MINUTE_A_DAY = 1440

def five_minutes_intervals_one_day(date):
    """
    create string list for 5 minutes intervals
    :param date: string
    :return: list
    """
    i = 0
    intervals = []
    while i <= MAX_MINUTE_A_DAY:
        intervals.append("{} {}".format(date,time_convert(i)))
        i += 5
    return intervals

def time_convert(number):
    """
    convert number of minutes to time format
    :param number: int of minutes
    :return: time format in string
    """
    if number < MIN_MINUTE_A_DAY or number > MAX_MINUTE_A_DAY:
        return ''
    else:
        hour = 0
        min = 0
        if number >= 60:
            hour = int(number/60)
            min = number - hour * 60
        else:
            min = number
        if min < 10:
            min = '0{}'.format(min)
        result = "{}:{}".format(hour,min)
        return result

def split_list_into_chunks(list,chunksize,label = []):
    """
    break list into small chunks
    :param list: array
    :param chunksize: int
    :param label: array (must size fit with size number of chunks)
    :return: dict of chuck
    """
    if chunksize <= 0 or chunksize > len(list):
        return list
    else:
        new_list = {}
        l = 0
        i = 0
        j = chunksize
        while i < len(list):
            if not label:
                new_list[i] = list[i:j]
            else:
                new_list[label[l]] = list[i:j]
            l += 1
            i += chunksize
            j += chunksize
        return new_list

def round_up_five_minutes(time_string):
    """
    round up time to 5 min intervals
    :param time_string: format 00:00:00-00
    :return: 00:00:00
    """
    hour = time_string[:-8]
    min = int(time_string[-8:-6])
    mod = min % 5
    min = min - mod
    if min < 10:
        min = "0" + str(min)
    return "{}{}".format(hour,min)

#print (round_up_five_minutes('A B C 00:01:00-00'))