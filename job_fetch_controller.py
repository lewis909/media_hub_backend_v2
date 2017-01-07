from glob import glob
import task_prep
import time
import datetime

# Staging Path
path = glob('F:\\Transcoder\\staging\\prep\\*.xml')

# Checks path for XML file, if an XML is found task_prep() is executed.
while True:

    log = open('log_file.txt', 'a')

    if int(len(path)):
        data = (str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")) + ': Processing files\n')
        print(data)
        log.write(data + '\n')
        task = task_prep.task_prep()
        log.write(task)
        path = glob('F:\\Transcoder\\staging\\prep\\*.xml')
        time.sleep(3)
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
