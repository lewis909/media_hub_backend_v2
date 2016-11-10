# Turns timecode into seconds, e.g 01:20:30.000 = 4830.0.
def timecode_to_secs(hours, mins, seconds):
    return int(hours) * 3600 + int(mins) * 60 + float(seconds)


# Creates file containing target assets final duration in seconds.
def progress_seconds(path, filename, duration):
    log_name = 'c_' + filename
    file_input = str(duration)

    temp_log = open(path + log_name, 'w')
    temp_log.write(file_input)
    temp_log.close()


# Creates conform list txt file.
def conform_list(path, conform_parts):

    c_list = open(path, 'w')
    for i in conform_parts:
        item = str(i).replace('\\', '\\\\')
        c_list.write('file ' + item + '\n')
    c_list.close()
