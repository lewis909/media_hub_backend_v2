import xml.etree.cElementTree as ET

# Turns timecode into seconds, e.g 01:20:30.000 = 4830.0.
from xml.dom import minidom


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


# Create file_data.xml
def create_file_data(video_filename, video_file_size, video_checksum, image_filename, image_file_size, image_checksum, path):
    file_data = ET.Element('file_data')
    video_file = ET.SubElement(file_data, 'video_file')
    image_file = ET.SubElement(file_data, 'image_file')

    ET.SubElement(video_file, 'file_name',).text = str(video_filename)
    ET.SubElement(video_file, 'file_size',).text = str(video_file_size)
    ET.SubElement(video_file, 'file_checksum',).text = str(video_checksum)
    
    ET.SubElement(image_file, 'file_name',).text = str(image_filename)
    ET.SubElement(image_file, 'file_size',).text = str(image_file_size)
    ET.SubElement(image_file, 'file_checksum',).text = str(image_checksum)

    xmlstr = minidom.parseString(ET.tostring(file_data)).toprettyxml(indent="   ")
    with open(path + 'core_xml.xml', "w") as f:
        f.write(xmlstr)
