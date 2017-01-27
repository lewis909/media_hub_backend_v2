import task_prep
import time
import os
import logging.handlers

from functions import timestamp
from glob import glob

# Staging Path
path = glob('F:\\Transcoder\\staging\\prep\\*.xml')

# Logging
date_stamp = timestamp()[:11].replace('-', '_')
file_log = logging.getLogger()
file_log.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(filename='F:\\Transcoder\\logs\\move_logs\\move_log_' + date_stamp + '.txt',
                                          maxBytes=10000000, backupCount=5)
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
file_log.addHandler(fh)


# Checks path for XML file, if an XML is found task_prep() is executed.
while True:

    for s in range(30):

        if s == 15:
            print(timestamp() + ': sleeping\n')
            file_log.info(': sleeping\n')
            time.sleep(30)
        else:

            if int(len(path)) > 0:
                data = ': Processing files\n'
                print(timestamp() + data)
                file_log.info(data)
                for i in path:
                    try:
                        task = task_prep.task_prep()
                        print(timestamp() + task)
                        file_log.info(task)
                        path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
                        time.sleep(3)
                    except Exception as e:
                        print(str(e))
                        print('Deleting problem file ' + str(i))
                        file_log.error(str(e))
                        file_log.warning('Deleting problem file ' + str(i))
                        os.remove(i)
                        time.sleep(3)
                        path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
            else:
                time.sleep(1)
                path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
                print(timestamp() + ': Waiting for files\n')
                file_log.info(': Waiting for files\n')
