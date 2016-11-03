import shutil
import os.path
import xml.dom.minidom as dom
import time
import config


for file in config.prep_xml:
    move_time = time.ctime()
    base = os.path.splitext(os.path.basename(file))[0]
    doc = dom.parse(file)
    filename = doc.getElementsByTagName("source_filename")
    fname = filename[0].firstChild.nodeValue
    mp4 = fname + '.mp4'
    src_repo = config.repo + mp4
    scr_tar = config.prep + base + '.mp4'

    nc_1 = len(config.node_1_count)
    nc_2 = len(config.node_2_count)
    nc_3 = len(config.node_3_count)
    nc_4 = len(config.node_4_count)

    load = [nc_1, nc_2, nc_3, nc_4]

    # print(load)

    if min(load) == nc_1:

        print("Task assigned to Node 1")

        shutil.copy(src_repo, scr_tar)
        shutil.move(file, config.node_1_path)
        shutil.move(scr_tar, config.node_1_path)

        print(move_time + ": The following files have been moved to Node 1:" '\n' + file + '\n' + scr_tar)

    elif min(load) == nc_2:

        shutil.copy(src_repo, scr_tar)
        shutil.move(file, config.node_2_path)
        shutil.move(scr_tar, config.node_2_path)

        print(move_time + ": The following files have been moved to Node 2:" '\n' + file + '\n' + scr_tar)

    elif min(load) == nc_3:

        shutil.copy(src_repo, scr_tar)
        shutil.move(file, config.node_3_path)
        shutil.move(scr_tar, config.node_3_path)

        print(move_time + ": The following files have been moved to Node 3:" '\n' + file + '\n' + scr_tar)

    elif min(load) == nc_4:

        shutil.copy(src_repo, scr_tar)
        shutil.move(file, config.node_4_path)
        shutil.move(scr_tar, config.node_4_path)

        print(move_time + ": The following files have been moved to Node 4:" '\n' + file + '\n' + scr_tar)
