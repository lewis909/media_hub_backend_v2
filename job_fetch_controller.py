from glob import glob
import task_prep
import time
import os

from functions import timestamp

# Staging Path
path = glob('F:\\Transcoder\\staging\\prep\\*.xml')

# Checks path for XML file, if an XML is found task_prep() is executed.
while True:

    with open('test_log.txt', 'a') as log:
        if int(len(path)):
            data = (timestamp() + ': Processing files\n')
            print(data)
            log.write(data + '\n')
            for i in path:
                try:
                    task = task_prep.task_prep()
                    log.write(task)
                    path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
                    time.sleep(3)
                except Exception as e:
                    print(str(e))
                    print('Deleting problem file ' + str(i))
                    os.remove(i)
                    time.sleep(3)
                    path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
        else:
            time.sleep(5)
            path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
            print(timestamp() + ': Waiting for files\n')
            log.write(timestamp() + ': Waiting for files\n')
