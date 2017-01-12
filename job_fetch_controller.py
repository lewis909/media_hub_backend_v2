from glob import glob
import task_prep
import time
import datetime
import os

# Staging Path
path = glob('F:\\Transcoder\\staging\\prep\\*.xml')

# Checks path for XML file, if an XML is found task_prep() is executed.
while True:

    # TODO - Create dynamic logfile system
    log = open('log_file.txt', 'a')

    if int(len(path)):
        data = (str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': Processing files\n')
        print(data)
        log.write(data + '\n')
        for i in path:
            try:
                task = task_prep.task_prep()
                log.write(task)
                path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
                time.sleep(3)
            except Exception:
                print('Deleting problem file ' + str(i))
                os.remove(i)
                time.sleep(3)
                path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
    else:
        log.write(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ': Waiting for files\n'))
        time.sleep(5)
        path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
        if path == 0:
            log.write(str(datetime.datetime.utcnow()
                          .strftime("%Y-%m-%d %H:%M:%S") + ': No Files found, waiting for next run\n'))
            break
    print(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ': no files\n'))
    log.write(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ': no files\n'))
    log.write(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ': Ending process\n'))
    log.close()
