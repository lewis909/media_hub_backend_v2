import shutil
import time
import config
import os.path
import xml.dom.minidom as dom

if config.prep_xml:

    for file in config.prep_xml:

        move_time = time.ctime()
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

            print("Task assigned to Node 1")

            shutil.copy(src_repo, scr_tar)
            shutil.move(file, config.node_1_path)
            shutil.move(scr_tar, config.node_1_path)

            print(move_time + ": The following files have been moved to Node 1:" '\n' + xml_base + '\n' + vid_base)

        elif min(load) == nc_2:

            print("Task assigned to Node 2")

            shutil.copy(src_repo, scr_tar)
            shutil.move(file, config.node_2_path)
            shutil.move(scr_tar, config.node_2_path)

            print(move_time + ": The following files have been moved to Node 2:" '\n' + xml_base + '\n' + vid_base)

        elif min(load) == nc_3:

            print("Task assigned to Node 3")

            shutil.copy(src_repo, scr_tar)
            shutil.move(file, config.node_3_path)
            shutil.move(scr_tar, config.node_3_path)

            print(move_time + ": The following files have been moved to Node 3:" '\n' + xml_base + '\n' + vid_base)

        elif min(load) == nc_4:

            print("Task assigned to Node 4")

            shutil.copy(src_repo, scr_tar)
            shutil.move(file, config.node_4_path)
            shutil.move(scr_tar, config.node_4_path)

            print(move_time + ": The following files have been moved to Node 4:" '\n' + xml_base + '\n' + vid_base)

else:
    print('No files')
