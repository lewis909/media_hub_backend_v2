import os.path
from glob import glob
import pymysql as mariadb
import psycopg2

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
transcode_logs = os.path.join('F:\\Transcoder\\logs\\transcode_logs\\')

# Database Connections
# Media hub Connection
mh_host = 'localhost'
mh_user = 'lewis_transcode'
mh_password = 'tool4602'
mh_database = 'media_hub'

# Txmam Connection
tx_host = 'localhost'
tx_user = 'lewis_transcode'
tx_password = 'tool4602'
tx_database = 'txmam'

# Schedule Connection
sc_host = 'localhost'
sc_user = 'lewis_transcode'
sc_password = 'tool4602'
sc_database = 'schedule'

# postgreSQL connections

p_con_string = "host='localhost' dbname='media_hub' user='media_hub_transcode' password='tool4602'"

p_con = psycopg2.connect(p_con_string)

p_cursor = p_con.cursor()

# Connection 1
dbc1 = mariadb.connect(host=mh_host,
                       user=mh_user,
                       password=mh_password,
                       database=mh_database)
# Connection 2
dbc2 = mariadb.connect(host=mh_host,
                       user=mh_user,
                       password=mh_password,
                       database=mh_database)
# Connection 3
dbc3 = mariadb.connect(host=mh_host,
                       user=mh_user,
                       password=mh_password,
                       database=mh_database)
# Connection 4
dbc4 = mariadb.connect(host=mh_host,
                       user=mh_user,
                       password=mh_password,
                       database=mh_database)
# txmam Connection
dbctx = mariadb.connect(host=tx_host,
                        user=tx_user,
                        password=tx_password,
                        database=tx_database)
# schedule Connection
dbcsc = mariadb.connect(host=sc_host,
                        user=sc_user,
                        password=sc_password,
                        database=sc_database)
# DB Cursors
cursor_1 = dbc1.cursor()
cursor_2 = dbc2.cursor()
cursor_3 = dbc3.cursor()
cursor_4 = dbc4.cursor()
cursor_tx = dbctx.cursor()
cursor_sc = dbcsc.cursor()
