from settings.GlobalConfiguration import GlobalConfiguration
import threading
import subprocess
import os
import time

class LogcatThread(threading.Thread):

    def __init__(self, threadName):
        super(LogcatThread, self).__init__(name=threadName)
        os.system('adb -s ' + GlobalConfiguration.DEVICE_ID + ' logcat -c')
        self.log_file = open(GlobalConfiguration.LOGCAT_LOG_PATH, 'w+')
        self.crash_file = open(GlobalConfiguration.LOGCAT_CRASH_PATH, 'w+')
        self.console_pipe = subprocess.Popen(args=GlobalConfiguration.LOGCAT_COMMAND_MONITOR, stdin=None,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.save_pipe = subprocess.Popen(args=GlobalConfiguration.LOGCAT_COMMAND_MONITOR, stdin=None, stdout=self.log_file, stderr=self.crash_file, shell=True)


    def close_monitor(self):
        self.save_pipe.terminate()
        self.save_pipe.kill()
        self.log_file.close()
        self.crash_file.close()
        self.console_pipe.terminate()
        self.console_pipe.kill()
        pass

    # monitor the any Exception every time
    def run(self):
        with self.console_pipe:
            for line in self.console_pipe.stdout:
                # TODO specify eligible crashes
                # print(line.decode('utf-8').strip())
                time.sleep(1)

if __name__ == '__main__':
    logcatThread = LogcatThread('L1')
    logcatThread.start()
    input()
    logcatThread.close_monitor()
