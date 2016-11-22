import os.path
import time
import config
import subprocess
import functions
import shutil
import xml.dom.minidom as dom
from glob import glob
import hashlib


def transcoder(transcode_node, cursor, dbc):
    xml = glob(transcode_node + '*.xml')

    for file in xml:
        node = transcode_node
        core_xml = dom.parse(file)

        # Core XML values
        root_element = core_xml.getElementsByTagName("manifest")
        task_id = root_element[0].attributes['task_id'].value
        target_profile_path = core_xml.getElementsByTagName('target_path')
        target_end_dir = target_profile_path[0].firstChild.nodeValue
        transcode_profile = core_xml.getElementsByTagName('transcode_profile')
        package_type = transcode_profile[0].attributes['package_type'].value
        xslt_profile = transcode_profile[0].attributes['profile_name'].value
        transcode_get = transcode_profile[0].firstChild.nodeValue
        move_time = time.ctime()
        total_dur = ''

        base = os.path.splitext(os.path.basename(file))[0]
        processing_temp_full = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\temp\\'
        processing_temp_conform = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\'
        processing_temp_root = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\'
        base_xml = base + '.xml'
        base_mp4 = base + '.mp4'
        s1_conform_target = processing_temp_conform + 's1_' + base_mp4
        s2_conform_target = processing_temp_conform + 's2_' + base_mp4
        s3_conform_target = processing_temp_conform + 's3_' + base_mp4
        s4_conform_target = processing_temp_conform + 's4_' + base_mp4
        conform_source = processing_temp_root + base_mp4
        conform_log = 'F:\\Transcoder\\logs\\transcode_logs\\' + 'c_' + task_id + '.txt'
        transcode_log = 'F:\\Transcoder\\logs\\transcode_logs\\' + 't_' + task_id + '.txt'
        target_path = processing_temp_full + base_mp4
        core_metadata_path = processing_temp_root + '\\core_metadata.xml'

        print(move_time + ': Starting Task ' + task_id)

        if not os.path.exists(processing_temp_full):
            print(move_time + ': Creating path: ' + processing_temp_full)
            os.makedirs(processing_temp_full)
            print(move_time + ': Moving files to ' + processing_temp_root)
            shutil.move(node + base_mp4, processing_temp_root)
            shutil.move(node + base_xml, core_metadata_path)
        else:
            print(move_time + ': Folder structure already exists, moving files to ' + processing_temp_root)
            shutil.move(node + base_mp4, processing_temp_root)
            shutil.move(node + base_xml, core_metadata_path)

        ffmpeg_conform_cmd, seg_number = functions.parse_xml(core_metadata_path, processing_temp_conform,  base_mp4)
        ffmpeg_conform = str(ffmpeg_conform_cmd).replace('INPUT_FILE', conform_source).replace('LOGFILE', conform_log)

        functions.progress_seconds(config.prog_temp, task_id + '.txt', total_dur)

        sql_conform = "UPDATE task SET status ='Conforming' WHERE task_id ='" + task_id + "'"
        print(sql_conform)
        cursor.execute(sql_conform)
        dbc.commit()
        print(ffmpeg_conform)
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
        cursor.execute(sql_transcode)
        dbc.commit()

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

        sql_complete = "UPDATE task SET status ='Complete' WHERE task_id ='" + task_id + "'"
        cursor.execute(sql_complete)
        dbc.commit()

