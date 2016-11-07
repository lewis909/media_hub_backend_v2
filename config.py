import os.path
from glob import glob
import pymysql as mariadb

# UNC Paths
prep = os.path.join('F:\\Transcoder\\staging\\prep\\')
repo = os.path.join("F:\\Transcoder\\repo\\")
node_1 = os.path.join('F:\\Transcoder\\staging\\node_1\\')
node_1_path = 'F:\\Transcoder\\staging\\node_1\\'
node_2_path = 'F:\\Transcoder\\staging\\node_2\\'
node_3_path = 'F:\\Transcoder\\staging\\node_3\\'
node_4_path = 'F:\\Transcoder\\staging\\node_4\\'
node_1_count = os.listdir('F:\\Transcoder\\staging\\node_1\\')
node_2_count = os.listdir('F:\\Transcoder\\staging\\node_2\\')
node_3_count = os.listdir('F:\\Transcoder\\staging\\node_3\\')
node_4_count = os.listdir('F:\\Transcoder\\staging\\node_4\\')
prep_xml = glob('F:\\Transcoder\\staging\\prep\\*xml')
mp4_src = glob('F:\\Transcoder\\staging\\prep\\*mp4')

# Database Connection
mariadb_connection = mariadb.connect(host='localhost', user='lewis_transcode', password='tool4602', database='media_hub')
cursor = mariadb_connection.cursor()
