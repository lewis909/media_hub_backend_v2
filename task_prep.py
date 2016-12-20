import shutil
import time
import config
import os.path
import xml.dom.minidom as dom
from glob import glob
import datetime


def task_prep():
    prep_xml = glob('F:\\Transcoder\\staging\\prep\\*xml')
    if prep_xml:
        print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + str(prep_xml))

        for file in prep_xml:
            print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + str(file))

            doc = dom.parse(file)
            filename = doc.getElementsByTagName("source_filename")
            fname = filename[0].firstChild.nodeValue
            base = os.path.splitext(os.path.basename(file))[0]
            src_repo = config.repo + fname + '.mp4'
            scr_tar = config.prep + base + '.mp4'
            xml_base = os.path.basename(file)
            vid_base = os.path.basename(scr_tar)
            nc_1 = len(os.listdir(config.node_1_path))
            nc_2 = len(os.listdir(config.node_2_path))
            nc_3 = len(os.listdir(config.node_3_path))
            nc_4 = len(os.listdir(config.node_4_path))

            load = [nc_1, nc_2, nc_3, nc_4]

            if min(load) == nc_1:

                print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': '"Task assigned to Node 1")

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_1_path)
                shutil.move(scr_tar, config.node_1_path)

                return str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' +  ": The following files have been moved to Node 1:" '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + xml_base + '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + vid_base + '\n'

            elif min(load) == nc_2:

                print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "Task assigned to Node 2")

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_2_path)
                shutil.move(scr_tar, config.node_2_path)

                return str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + ": The following files have been moved to Node 2:" '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + xml_base + '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + vid_base + '\n'

            elif min(load) == nc_3:

                print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "Task assigned to Node 3")

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_3_path)
                shutil.move(scr_tar, config.node_3_path)

                return str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' +  ": The following files have been moved to Node 3:" '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + xml_base + '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + vid_base + '\n'

            elif min(load) == nc_4:

                print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + "Task assigned to Node 4")

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_4_path)
                shutil.move(scr_tar, config.node_4_path)

                return str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' +  ": The following files have been moved to Node 4:" '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + xml_base + '\n' + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + vid_base + '\n'

    else:
        print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': ' + 'No files')
