import os.path
import time
import config
import shutil
import xml.dom.minidom as dom
from glob import glob


def transcoder():

    # mp4 = glob('F:\\Transcoder\\staging\\node_1\\*.mp4')
    xml = glob('F:\\Transcoder\\staging\\node_1\\*.xml')

    for file in xml:
        node = config.node_1
        core_xml = dom.parse(file)
        root_element = core_xml.getElementsByTagName("manifest")
        task_id = root_element[0].attributes['task_id'].value
        move_time = time.ctime()
        base = os.path.splitext(os.path.basename(file))[0]
        processing_temp_full = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\conform\\temp\\'
        processing_temp_root = 'F:\\Transcoder\\processing_temp\\' + 'task_' + task_id + '\\'
        base_xml = base + '.xml'
        base_mp4 = base + '.mp4'

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



transcoder()
