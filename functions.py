# Turns timecode into seconds, e.g 01:20:30.000 = 4830.0
def timecode_to_secs(hours, mins, seconds):
    return int(hours) * 3600 + int(mins) * 60 + float(seconds)
