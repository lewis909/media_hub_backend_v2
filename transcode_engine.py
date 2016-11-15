import os.path
import time
import config
import subprocess
from config import cursor as dbc
from functions import timecode_to_secs as tc_to_secs
import functions
import shutil
import xml.dom.minidom as dom
from glob import glob
import hashlib


def transcoder():
    xml = glob('F:\\Transcoder\\staging\\node_1\\*.xml')

    for file in xml:
        node = config.node_1
        core_xml = dom.parse(file)

        # Core XML values
        root_element = core_xml.getElementsByTagName("manifest")
        task_id = root_element[0].attributes['task_id'].value
        get_num_of_seg = core_xml.getElementsByTagName('number_of_segments')
        target_profile_path = core_xml.getElementsByTagName('target_path')
        num_of_seg = get_num_of_seg[0].firstChild.nodeValue
        target_end_dir = target_profile_path[0].firstChild.nodeValue
        conform = core_xml.getElementsByTagName('conform_profile')
        transcode_profile = core_xml.getElementsByTagName('transcode_profile')
        package_type = transcode_profile[0].attributes['package_type'].value
        xslt_profile = transcode_profile[0].attributes['profile_name'].value
        conform_get = conform[0].firstChild.nodeValue
        transcode_get = transcode_profile[0].firstChild.nodeValue
        seg_1 = core_xml.getElementsByTagName("segment_1")
        seg_2 = core_xml.getElementsByTagName("segment_2")
        seg_3 = core_xml.getElementsByTagName("segment_3")
        seg_4 = core_xml.getElementsByTagName("segment_4")
        move_time = time.ctime()
        seg_conform = ''
        total_dur = ''

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
        transcode_log = 'F:\\Transcoder\\logs\\transcode_logs\\' + 't_' + task_id + '.txt'
        target_path = processing_temp_full + base_mp4

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
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target + \
                          ' -ss ' + seg_2_in + ' -t ' + seg_2_dur + ' ' + s2_conform_target

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
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target + \
                          ' -ss ' + seg_2_in + ' -t ' + seg_2_dur + ' ' + s2_conform_target + \
                          ' -ss ' + seg_3_in + ' -t ' + seg_3_dur + ' ' + s3_conform_target

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
            seg_conform = '-ss ' + seg_1_in + ' -t ' + seg_1_dur + ' ' + s1_conform_target + \
                          ' -ss ' + seg_2_in + ' -t ' + seg_2_dur + ' ' + s2_conform_target + \
                          ' -ss ' + seg_3_in + ' -t ' + seg_3_dur + ' ' + s3_conform_target + \
                          ' -ss ' + seg_4_in + ' -t ' + seg_4_dur + ' ' + s4_conform_target

        ffmpeg_conform = str(conform_get) \
            .replace('S_PATH/', conform_source) \
            .replace('F_NAME.mp4', base_mp4) \
            .replace('SEG_CONFORM', seg_conform) \
            .replace('LOG_FILE.txt', conform_log)

        print(ffmpeg_conform)

        functions.progress_seconds(config.prog_temp, task_id + '.txt', total_dur)

        sql_conform = "UPDATE task SET status ='Conforming' WHERE task_id ='" + task_id + "'"
        print(sql_conform)
        dbc.execute(sql_conform)
        config.mariadb_connection.commit()

        subprocess.call(ffmpeg_conform)

        shutil.move(processing_temp_root + 'core_metadata.xml', processing_temp_full + 'core_metadata.xml')

        seg_list = glob(processing_temp_conform + '*.mp4')
        cml = processing_temp_conform + base + '_conform_list.txt'
        functions.conform_list(cml, seg_list)

        ffmpeg_transcode = str(transcode_get) \
            .replace('LOG_FILE.txt', transcode_log) \
            .replace('T_PATH/CONFORM_LIST', cml) \
            .replace('TRC_PATH/F_NAME.mp4', target_path)

        sql_transcode = "UPDATE task SET status ='Transcoding' WHERE task_id ='" + task_id + "'"
        dbc.execute(sql_transcode)
        config.mariadb_connection.commit()
        print(ffmpeg_transcode)
        subprocess.call(ffmpeg_transcode)

        video_size = os.path.getsize(target_path)
        video_checksum = hashlib.md5(open(target_path, 'rb').read()).hexdigest()

        functions.create_file_data(target_path, video_size, video_checksum,
                                   'test', 'test', 'test', processing_temp_full)

        xslt_src_dir = 'F:\\Transcoder\\xslt_repo\\' + xslt_profile + '\\'
        xslt_src_file = xslt_src_dir + xslt_profile + '.xsl'

        shutil.copy(xslt_src_file, processing_temp_full)

        xslt_process = 'java -jar C:\\SaxonHE9-7-0-7J\\saxon9he.jar ' + processing_temp_full + 'core_metadata.xml ' +\
                       processing_temp_full + xslt_profile + '.xsl > ' + processing_temp_full + base_xml

        print(xslt_process)

        subprocess.call(str(xslt_process), shell=True)
        final_video = processing_temp_full + base_mp4
        final_xml = processing_temp_full + base_xml
        final_dir = target_end_dir + base_mp4

        if package_type == 'flat':
            print('Moving Files to ' + target_end_dir)
            shutil.move(final_video, target_end_dir)
            shutil.move(final_xml, target_end_dir)
        elif package_type == 'tar':
            print('creating tar package')
            tar_package = processing_temp_full + base_mp4 + '.tar'
            tar = '7z a -ttar ' + tar_package + ' ' + final_video + ' ' + final_xml
            print(tar)
            subprocess.call(tar)
            shutil.move(tar_package, target_end_dir)
        elif package_type == 'dir':
            print('Creating DIR')
            os.mkdir(final_dir)
            shutil.move(final_video, final_dir)
            shutil.move(final_xml, final_dir)

        sql_transcode = "UPDATE task SET status ='Complete' WHERE task_id ='" + task_id + "'"
        dbc.execute(sql_transcode)
        config.mariadb_connection.commit()

transcoder()
