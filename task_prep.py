import shutil
import time
import config
import os.path
import xml.dom.minidom as dom

move_time = time.ctime()
nc_1 = len(config.node_1_count)
nc_2 = len(config.node_2_count)
nc_3 = len(config.node_3_count)
nc_4 = len(config.node_4_count)

load = [nc_1, nc_2, nc_3, nc_4]

print(move_time + ': Load Balance Status: Node_1 = ' + str(load[0]) + ', Node_2 = ' + str(load[1]) + ', Node_3 = ' + str(load[2]) + ', Node_4 =' + str(load[3]))

for file in config.prep_xml:

    doc = dom.parse(file)
    filename = doc.getElementsByTagName("source_filename")
    fname = filename[0].firstChild.nodeValue
    base = os.path.splitext(os.path.basename(file))[0]
    src_repo = config.repo + fname + '.mp4'
    scr_tar = config.prep + base + '.mp4'

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