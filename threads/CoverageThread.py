from settings.GlobalConfiguration import GlobalConfiguration
import threading
import os
import time


class CoverageThread(threading.Thread):
    def __init__(self, threadName):
        super(CoverageThread, self).__init__(name=threadName)
        os.system('adb shell rm /mnt/sdcard/coverage.ec')

    def run(self):
        time.sleep(2)
        for i in range(61):
            os.system(
                'adb pull /mnt/sdcard/coverage.ec ' + GlobalConfiguration.OUT_DIR + '/' + str(i * 60) + '_coverage.ec')
            time.sleep(60)


if __name__ == '__main__':
    coverageThread = CoverageThread("C1")
    coverageThread.start()
