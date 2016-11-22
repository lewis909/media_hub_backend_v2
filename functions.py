import xml.etree.cElementTree as ET
import os
from xml.dom import minidom

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


# Create file_data.xml
def create_file_data(video_filename, video_file_size, video_checksum,
                     image_filename, image_file_size, image_checksum, path):
    video_base = os.path.splitext(os.path.basename(video_filename))[0]
    video_ext = os.path.splitext(os.path.basename(video_filename))[1]
    file_data = ET.Element('file_data')
    video_file = ET.SubElement(file_data, 'video_file')
    image_1 = ET.SubElement(file_data, 'image_1')

    ET.SubElement(video_file, 'file_name',).text = str(video_base) + str(video_ext)
    ET.SubElement(video_file, 'file_size',).text = str(video_file_size)
    ET.SubElement(video_file, 'md5_checksum',).text = str(video_checksum)
    
    ET.SubElement(image_1, 'file_name',).text = str(image_filename)
    ET.SubElement(image_1, 'file_size',).text = str(image_file_size)
    ET.SubElement(image_1, 'md5_checksum',).text = str(image_checksum)

    xmlstr = minidom.parseString(ET.tostring(file_data)).toprettyxml(indent="   ")
    with open(path + 'file_data.xml', "w") as f:
        f.write(xmlstr)


# Dynamic ffmpeg conform command function
# Takes result Element attribute dictionary and merges each entry into a list
def seg_element(xml_root, element_path):
    list_a = []
    for elem in xml_root.iterfind(element_path):
        a = elem.attrib
        for i in a:
            list_a.append([i + ' = ' + a[i]])
        return list_a


# This does all the heavy lifting for parse_xml.
# The segment in-point and duration are picked out of the output from seg_element.
# A list of conform parts is created, all 3 lists are zipped and the FFMPEG command is formatted.
def find_seg_in_point(dur_string, seg_number):
    seg_start_list = []
    seg_duration_list = []
    c_file_list = []
    while True:
        for i in range(seg_number):
            seg = 'seg_%d_in =' % (i+1)
            seg_in_s = str(dur_string).find(seg)
            if seg_in_s > 0:
                seg_in_e = str(dur_string).find(']', seg_in_s)
                seg_in = str(dur_string)[seg_in_s:seg_in_e - 1]
                seg_start_list.append(str(seg_in).replace(seg, '-ss'))
        for i in range(seg_number):
            seg = 'seg_%d_dur =' % (i + 1)
            seg_dur_s = str(dur_string).find(seg)
            if seg_dur_s > 0:
                seg_dur_e = str(dur_string).find(']', seg_dur_s)
                seg_dur = str(dur_string)[seg_dur_s:seg_dur_e - 1]
                seg_duration_list.append(str(seg_dur).replace(seg, '-t'))
        for i in range(seg_number):
            file_num ='C_%d_FILE.MP4' % (i + 1)
            c_file_list.append(file_num)
        break

    in_point_and_dur = list(zip(seg_start_list, seg_duration_list, c_file_list))

    return in_point_and_dur


# The container for find_seg_in_in_point and seg element.
def parse_xml(file_input):
    tree = ET.parse(file_input)
    root = tree.getroot()
    segments_no = int(root.find('file_info/number_of_segments').text)
    segments = []

    for i in range(segments_no):
        path = 'file_info/segment_%d' % (i+1)
        segments.append(seg_element(root, path))

    pre_s = find_seg_in_point(str(segments), segments_no)

    ffmpeg_cmd = 'ffmpeg -progress LOGFILE -i INPUT_FILE ' + str(pre_s)[3:-2].replace("'", '').replace(',', '').replace('(', '').replace(')', '')
    return ffmpeg_cmd, segments_no
