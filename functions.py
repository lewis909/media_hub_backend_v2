# Turns timecode into seconds, e.g 01:20:30.000 = 4830.0
def timecode_to_secs(hours, mins, seconds):
    return int(hours) * 3600 + int(mins) * 60 + float(seconds)


def progress_seconds(path, filename, duration):
    log_name = 'c_' + filename
    file_input = str(duration)

    temp_log = open(path + log_name, 'w')
    temp_log.write(file_input)
    temp_log.close()


def conform_list(path, log_name, list):

    c_list = open(path + log_name, 'w')
    c_list.write(list)
    c_list.close()
