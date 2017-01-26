import shutil
import config
import os.path
import xml.dom.minidom as dom
from glob import glob


def task_prep():
    prep_xml = glob('F:\\Transcoder\\staging\\prep\\*xml')
    if prep_xml:

        for file in prep_xml:

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

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_1_path)
                shutil.move(scr_tar, config.node_1_path)

                return ': The following files have been moved to Node 1:' + xml_base + ', ' + vid_base + '\n'

            elif min(load) == nc_2:

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_2_path)
                shutil.move(scr_tar, config.node_2_path)

                return ': The following files have been moved to Node 2:' + xml_base + ', ' + vid_base + '\n'

            elif min(load) == nc_3:

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_3_path)
                shutil.move(scr_tar, config.node_3_path)

                return ': The following files have been moved to Node 3:' + xml_base + ', ' + vid_base + '\n'

            elif min(load) == nc_4:

                shutil.copy(src_repo, scr_tar)
                shutil.move(file, config.node_4_path)
                shutil.move(scr_tar, config.node_4_path)

                return ': The following files have been moved to Node 4:' + xml_base + ', ' + vid_base + '\n'

    else:
        print(': ' + 'No files')
