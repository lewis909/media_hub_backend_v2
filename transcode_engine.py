import os.path
import time
import config
import subprocess
# from config import cursor as dbc
from functions import timecode_to_secs as tc_to_secs
import shutil
import xml.dom.minidom as dom
from glob import glob


def transcoder():

    # mp4 = glob('F:\\Transcoder\\staging\\node_1\\*.mp4')
    xml = glob('F:\\Transcoder\\staging\\node_1\\*.xml')

    for file in xml:
        node = config.node_1
        core_xml = dom.parse(file)

        # Core XML values
        root_element = core_xml.getElementsByTagName("manifest")
        task_id = root_element[0].attributes['task_id'].value
        get_num_of_seg = core_xml.getElementsByTagName('number_of_segments')
        num_of_seg = get_num_of_seg[0].firstChild.nodeValue
        conform = core_xml.getElementsByTagName('conform_profile')
        conform_get = conform[0].firstChild.nodeValue
        seg_1 = core_xml.getElementsByTagName("segment_1")
        seg_2 = core_xml.getElementsByTagName("segment_2")
        seg_3 = core_xml.getElementsByTagName("segment_3")
        seg_4 = core_xml.getElementsByTagName("segment_4")
        move_time = time.ctime()

        print(num_of_seg)

        base = os.path.splitext(os.path.basename(file))[0]
        processing_temp_full = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\temp\\'
        processing_temp_root = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\'
        processing_temp_conform = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\'
        base_xml = base + '.xml'
        base_mp4 = base + '.mp4'
        s1_conform_target = processing_temp_conform + 's1_' + base_mp4
        s2_conform_target = processing_temp_conform + 's2_' + base_mp4
        s3_conform_target = processing_temp_conform + 's3_' + base_mp4
        s4_conform_target = processing_temp_conform + 's4_' + base_mp4
        conform_source = processing_temp_root
        conform_log = 'F:\\Transcoder\\logs\\transcode_logs\\' + 'c_' + task_id + '.txt'

        print(move_time + ': Starting Task ' + task_id)

        if not os.path.exists(processing_temp_full):
            print(move_time + ': Creating path: ' + processing_temp_full)
            os.makedirs(processing_temp_full)
            print(move_time + ': Moving files to ' + processing_temp_root)
            shutil.move(node + base_mp4, processing_temp_root)
            shutil.move(node + base_xml, processing_temp_root + '\\core_metadata.xml')
        else:
            print(move_time + ': Folder structure already exists, moving files to ' + processing_temp_root)
            shutil.move(node + base_mp4, processing_temp_root)
            shutil.move(node + base_xml, processing_temp_root + '\\core_metadata.xml')

        if int(num_of_seg) == 1:

            seg_1_in = seg_1[0].attributes['seg_1_in'].value
            seg_1_dur = seg_1[0].attributes['seg_1_dur'].value
            conform_seg_1_dur = str(seg_1_dur).split(':')
            seg_1_secs = tc_to_secs(*conform_seg_1_dur)

            total_dur = seg_1_secs
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target

        elif int(num_of_seg) == 2:

            seg_1_in = seg_1[0].attributes['seg_1_in'].value
            seg_1_dur = seg_1[0].attributes['seg_1_dur'].value
            seg_2_in = seg_2[0].attributes['seg_2_in'].value
            seg_2_dur = seg_2[0].attributes['seg_2_dur'].value
            conform_seg_1_dur = str(seg_1_dur).split(':')
            conform_seg_2_dur = str(seg_2_dur).split(':')
            seg_1_secs = tc_to_secs(*conform_seg_1_dur)
            seg_2_secs = tc_to_secs(*conform_seg_2_dur)

            total_dur = seg_1_secs + seg_2_secs
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target + ' -ss ' + seg_2_in + ' -t ' + seg_2_dur + ' ' + s2_conform_target

        elif int(num_of_seg) == 3:

            seg_1_in = seg_1[0].attributes['seg_1_in'].value
            seg_1_dur = seg_1[0].attributes['seg_1_dur'].value
            seg_2_in = seg_2[0].attributes['seg_2_in'].value
            seg_2_dur = seg_2[0].attributes['seg_2_dur'].value
            seg_3_in = seg_3[0].attributes['seg_3_in'].value
            seg_3_dur = seg_3[0].attributes['seg_3_dur'].value

            conform_seg_1_dur = str(seg_1_dur).split(':')
            conform_seg_2_dur = str(seg_2_dur).split(':')
            conform_seg_3_dur = str(seg_3_dur).split(':')

            seg_1_secs = tc_to_secs(*conform_seg_1_dur)
            seg_2_secs = tc_to_secs(*conform_seg_2_dur)
            seg_3_secs = tc_to_secs(*conform_seg_3_dur)

            total_dur = seg_1_secs + seg_2_secs + seg_3_secs
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target + ' -ss ' + seg_2_in + ' -t ' + seg_2_dur + ' ' + s2_conform_target + ' -ss ' + seg_3_in + ' -t ' + seg_3_dur + ' ' + s3_conform_target

        elif int(num_of_seg) == 4:

            seg_1_in = seg_1[0].attributes['seg_1_in'].value
            seg_1_dur = seg_1[0].attributes['seg_1_dur'].value
            seg_2_in = seg_2[0].attributes['seg_2_in'].value
            seg_2_dur = seg_2[0].attributes['seg_2_dur'].value
            seg_3_in = seg_3[0].attributes['seg_3_in'].value
            seg_3_dur = seg_3[0].attributes['seg_3_dur'].value
            seg_4_in = seg_4[0].attributes['seg_4_in'].value
            seg_4_dur = seg_4[0].attributes['seg_4_dur'].value

            conform_seg_1_dur = str(seg_1_dur).split(':')
            conform_seg_2_dur = str(seg_2_dur).split(':')
            conform_seg_3_dur = str(seg_3_dur).split(':')
            conform_seg_4_dur = str(seg_4_dur).split(':')

            seg_1_secs = tc_to_secs(*conform_seg_1_dur)
            seg_2_secs = tc_to_secs(*conform_seg_2_dur)
            seg_3_secs = tc_to_secs(*conform_seg_3_dur)
            seg_4_secs = tc_to_secs(*conform_seg_4_dur)

            total_dur = seg_1_secs + seg_2_secs + seg_3_secs + seg_4_secs
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target + ' -ss ' + seg_2_in + ' -t ' + seg_2_dur + ' ' + s2_conform_target + ' -ss ' + seg_3_in + ' -t ' + seg_3_dur + ' ' + s3_conform_target + ' -ss ' + seg_4_in + ' -t ' + seg_4_dur + ' ' + s4_conform_target

        ffmpeg_conform = str(conform_get).replace('S_PATH/', conform_source).replace('F_NAME.mp4', base_mp4).replace('SEG_CONFORM', seg_conform).replace('LOG_FILE.txt', conform_log)
        print(ffmpeg_conform)
        subprocess.call(ffmpeg_conform)

transcoder()
