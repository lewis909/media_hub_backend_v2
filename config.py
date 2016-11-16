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
prog_temp = os.path.join('F:\\Transcoder\\logs\\transcode_logs\\temp\\')


# Database Connection
host = 'localhost'
user = 'lewis_transcode'
password = 'tool4602'
database = 'media_hub'


dbc1 = mariadb.connect(host=host,
                       user=user,
                       password=password,
                       database=database)

dbc2 = mariadb.connect(host=host,
                       user=user,
                       password=password,
                       database=database)

dbc3 = mariadb.connect(host=host,
                       user=user,
                       password=password,
                       database=database)

dbc4 = mariadb.connect(host=host,
                       user=user,
                       password=password,
                       database=database)
cursor_1 = dbc1.cursor()
cursor_2 = dbc2.cursor()
cursor_3 = dbc3.cursor()
cursor_4 = dbc4.cursor()
