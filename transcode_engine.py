# import sqlite3
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
        core_xml = dom.parse(file)
        root_element = core_xml.getElementsByTagName("manifest")
        task_id = root_element[0].attributes['task_id'].value
        move_time = time.ctime()
        base = os.path.splitext(os.path.basename(file))[0]
        base_xml = base + '.xml'
        base_mp4 = base + '.mp4'

        print(move_time + ': Starting Task' + task_id)

        shutil.move(config.node_1 + base_mp4, 'F:\\Transcoder\\testing\\')
        shutil.move(config.node_1 + base_xml, 'F:\\Transcoder\\testing\\')

transcoder()
