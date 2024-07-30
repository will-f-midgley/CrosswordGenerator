def time_convert(time_value):
    minutes = time_value // 60
    hours = minutes // 60

    if minutes > 0:
        if hours > 0:
            converted = (str(hours) + "h, " + str(minutes % 60) + "m, " + str(time_value % 60) + "s")
        else:
            converted = (str(minutes) + "m, " + str(time_value % 60) + "s")
    else:
        converted = (str(time_value) + "s")

    return converted
