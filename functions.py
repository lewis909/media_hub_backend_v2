import xml.etree.cElementTree as ET
import os
import datetime

from xml.dom import minidom

# import Metadata Profile files


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

# start of the Dynamic FFMPEG conform function


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
def find_seg_in_point(dur_string, seg_number, conform_path, file_name):
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
            file_num = conform_path + 'C_%d_' % (i + 1) + file_name
            c_file_list.append(file_num)
        break
    in_point_and_dur = list(zip(seg_start_list, seg_duration_list, c_file_list))
    return in_point_and_dur


# The container for find_seg_in_in_point and seg element.
def parse_xml(file_input, conform_path, base_file_name):
    tree = ET.parse(file_input)
    root = tree.getroot()
    segments_no = int(root.find('file_info/number_of_segments').text)
    segments = []
    for i in range(segments_no):
        path = 'file_info/segment_%d' % (i+1)
        segments.append(seg_element(root, path))

    pre_s = find_seg_in_point(str(segments), segments_no, conform_path, base_file_name)

    ffmpeg_cmd = 'ffmpeg -i INPUT_FILE ' + str(pre_s)[3:-2].replace("'", '').replace(',', '')\
        .replace('(', '').replace(')', '')
    return ffmpeg_cmd, segments_no

# end of the Dynamic FFMPEG conform function

# Metadata creation functions


def get_metadata(core_metadata_xml, file_data, target_path):
    # Mapping from Core_metadata.xml
    core_tree = ET.parse(core_metadata_xml)
    core_root = core_tree.getroot()
    task_id = core_root.get('task_id')
    mat_id = core_root.find('asset_metadata/material_id').text
    series_title = core_root.find('asset_metadata/series_title').text
    season_title = core_root.find('asset_metadata/season_title').text
    season_number = core_root.find('asset_metadata/season_number').text
    episode_title = core_root.find('asset_metadata/episode_title').text
    episode_number = core_root.find('asset_metadata/episode_number').text
    start_date = core_root.find('asset_metadata/start_date').text
    end_date = core_root.find('asset_metadata/end_date').text
    rating = core_root.find('asset_metadata/ratings').text
    synopsis = core_root.find('asset_metadata/synopsis').text

    # Mapping of Naming Conventions
    profile = core_root.find('file_info/transcode_profile').attrib['profile_name']
    video_file_naming_convention = core_root.find('file_info/video_file_naming_convention').text
    image_file_naming_convention = core_root.find('file_info/image_file_naming_convention').text
    package_naming_convention = core_root.find('file_info/package_naming_convention').text

    # Mapping from file_data.xml
    fd_tree = ET.parse(file_data)
    fd_root = fd_tree.getroot()
    vid_file_name = fd_root.find('video_file/file_name').text
    vid_file_size = fd_root.find('video_file/file_size').text
    vid_md5_checksum = fd_root.find('video_file/md5_checksum').text
    image_file_name = fd_root.find('image_1/file_name').text
    image_file_size = fd_root.find('image_1/file_size').text
    image_md5_checksum = fd_root.find('image_1/md5_checksum').text

    return task_id,\
           mat_id,\
           series_title,\
           season_title,\
           season_number,\
           episode_title,\
           episode_number,\
           start_date,\
           end_date,\
           rating,\
           synopsis,\
           vid_file_name,\
           vid_file_size,\
           vid_md5_checksum,\
           image_file_name,\
           image_file_size,\
           image_md5_checksum,\
           target_path,\
           profile,\
           video_file_naming_convention,\
           image_file_naming_convention,\
           package_naming_convention


# Creates the profiles bespoke naming convention
def naming_convention(task_id, mat_id, series_title, season_title, season_number, episode_title,
                      episode_number, start_date, end_date, rating, synopsis, vid_file_name, vid_file_size,
                      vid_md5_checksum, image_file_name, image_file_size, image_md5_checksum, target_path, profile,
                      video_file_naming_convention, image_file_naming_convention, package_naming_convention):

        target_video_file_name = video_file_naming_convention.replace('PROFILE', profile).replace('MATID', mat_id)
        target_metadata_name = video_file_naming_convention.replace('PROFILE', profile).replace('MATID', mat_id)
        target_image_file_name = image_file_naming_convention.replace('PROFILE', profile).replace('MATID', mat_id)
        target_package_name = package_naming_convention.replace('PROFILE', profile).replace('MATID', mat_id).replace('SERIESTITLE', series_title).replace('SEASONNUMBER', season_number).replace(' ', '_').replace('TASKID', task_id)

        return target_video_file_name, target_metadata_name, target_image_file_name, target_package_name


def timestamp():
    return str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
