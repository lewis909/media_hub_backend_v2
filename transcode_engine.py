import os.path
import time
import config
import subprocess
import functions
import shutil
import hashlib
import tarfile
import xml.dom.minidom as dom

from metadata_profiles import profile_dict
from subprocess import PIPE
from glob import glob


def transcoder(transcode_node, cursor, dbc):
    xml = glob(transcode_node + '*.xml')

    try:

        for file in xml:
            node = transcode_node
            core_xml = dom.parse(file)

            # Core XML values.
            root_element = core_xml.getElementsByTagName("manifest")
            task_id = root_element[0].attributes['task_id'].value
            target_profile_path = core_xml.getElementsByTagName('target_path')
            target_end_dir = target_profile_path[0].firstChild.nodeValue
            transcode_profile = core_xml.getElementsByTagName('transcode_profile')
            package_type = transcode_profile[0].attributes['package_type'].value
            xml_profile = transcode_profile[0].attributes['profile_name'].value
            transcode_get = transcode_profile[0].firstChild.nodeValue
            move_time = time.ctime()
            total_dur = ''
            base = os.path.splitext(os.path.basename(file))[0]
            processing_temp_root = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\'
            processing_temp_full = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\temp\\'
            processing_temp_conform = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\'
            conform_log = 'F:\\Transcoder\\logs\\transcode_logs\\' + 'c_' + task_id + '.txt'
            transcode_log = 'F:\\Transcoder\\logs\\transcode_logs\\' + 't_' + task_id + '.txt'
            base_xml = base + '.xml'
            base_mp4 = base + '.mp4'
            conform_source = processing_temp_root + base_mp4
            target_path = processing_temp_full + base_mp4
            core_metadata_path = processing_temp_root + 'core_metadata.xml'
            file_data_xml = processing_temp_full + 'file_data.xml'
            final_xml = processing_temp_full + base_xml

            # Processing starts
            print(move_time + ': Starting Task ' + task_id)

            # Updated database with task start time
            job_start_time = time.ctime()
            start_job = "UPDATE task SET job_start_time ='" + job_start_time + "'WHERE task_id ='" + task_id + "'"
            cursor.execute(start_job)
            dbc.commit()

            # Logic to move files into a DIR if that DIR already exists.
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

            # Conform section.
            ffmpeg_conform_cmd, seg_number = functions.parse_xml(core_metadata_path, processing_temp_conform,  base_mp4)
            ffmpeg_conform = str(ffmpeg_conform_cmd).replace('INPUT_FILE', conform_source).replace('LOGFILE', conform_log)
            print(ffmpeg_conform)

            functions.progress_seconds(config.prog_temp, task_id + '.txt', total_dur)

            # Updated database stating that the conform process has started
            sql_conform = "UPDATE task SET status ='Conforming' WHERE task_id ='" + task_id + "'"
            cursor.execute(sql_conform)
            dbc.commit()
            try:
                conform_result = subprocess.run(ffmpeg_conform, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                print(conform_result.stderr)
                # TODO - prefix time stamp to STDOUT for FFMPEG log
                c_log = open(config.transcode_logs + 'c_' + task_id + '_detail.txt', 'w')
                c_log.write(conform_result.stderr)
                c_log.close()
            except ValueError:
                print('Conform has Failed: ' + task_id)

            shutil.move(processing_temp_root + 'core_metadata.xml', processing_temp_full + 'core_metadata.xml')

            seg_list = glob(processing_temp_conform + '*.mp4')
            cml = processing_temp_conform + base + '_conform_list.txt'
            functions.conform_list(cml, seg_list)

            # Transcode section.
            ffmpeg_transcode = str(transcode_get) \
                .replace('LOG_FILE.txt', transcode_log) \
                .replace('T_PATH/CONFORM_LIST', cml) \
                .replace('TRC_PATH/F_NAME.mp4', target_path)

            # Updated database stating that the transcode process has started
            sql_transcode = "UPDATE task SET status ='Transcoding' WHERE task_id ='" + task_id + "'"
            cursor.execute(sql_transcode)
            dbc.commit()
            try:
                print(ffmpeg_transcode)
                transcode_result = subprocess.run(ffmpeg_transcode, stdout=PIPE, stderr=PIPE, universal_newlines=True)
                print(transcode_result.stderr)
                t_log = open(config.transcode_logs + 't_' + task_id + '_detail.txt', 'w')
                t_log.write(transcode_result.stderr)
                t_log.close()
            except ValueError:
                print('Transcode has failed: ' + task_id)

            video_size = os.path.getsize(target_path)
            video_checksum = hashlib.md5(open(target_path, 'rb').read()).hexdigest()

            # Create file_date.xml (image section current contains test info).
            functions.create_file_data(target_path, video_size, video_checksum,
                                       'test', 'test', 'test', processing_temp_full)

            # Create metadata
            profile_dict.metadata_profiles[xml_profile](*functions.get_metadata(processing_temp_full + 'core_metadata.xml',
                                                                             file_data_xml, final_xml))
            # file name creator
            video_name_out, xml_name_out, image_name_out, dir_name_out = functions.naming_convention(*functions.get_metadata(processing_temp_full + 'core_metadata.xml',
                                                                             file_data_xml, final_xml))

            # Final package delivery.
            final_video = processing_temp_full + base_mp4
            target_video_file = processing_temp_full + video_name_out + '.mp4'
            os.rename(final_video, target_video_file)
            final_xml = processing_temp_full + base_xml
            target_xml = processing_temp_full + xml_name_out + '.xml'
            os.rename(final_xml, target_xml)
            final_dir = target_end_dir + dir_name_out

            # Moves all files into the target DIR
            if package_type == 'flat':
                print('Moving Files to ' + target_end_dir)
                shutil.move(target_video_file, target_end_dir)
                shutil.move(target_xml, target_end_dir)
            # Wraps required files in a .tar in the target DIR
            elif package_type == 'tar':
                print('creating tar package')
                file_list = [target_video_file, target_xml]
                with tarfile.open(final_dir + '.tar', 'x') as tar:
                    for t_file in file_list:
                        tar.add(t_file, arcname=os.path.basename(t_file))
                    tar.close()
            # Creates a DIR in the target DIR and moves package files into that DIR.
            elif package_type == 'dir':
                print('Creating DIR')
                os.mkdir(final_dir)
                shutil.move(target_video_file, final_dir)
                shutil.move(target_xml, final_dir)

            # Updated database stating that the task has completed
            sql_complete = "UPDATE task SET status ='Complete' WHERE task_id ='" + task_id + "'"
            cursor.execute(sql_complete)
            dbc.commit()
            job_complete_time = time.ctime()
            # Updated database stating task completion time
            end_job = "UPDATE task SET job_end_time ='" + job_complete_time + "'WHERE task_id ='" + task_id + "'"
            cursor.execute(end_job)
            dbc.commit()

    except Exception as e:
        print(str(e))
