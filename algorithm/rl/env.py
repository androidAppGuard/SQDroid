from settings.GlobalConfiguration import GlobalConfiguration
import uiautomator2 as u2
import time
import os


class ENV(object):

    def __init__(self):
        self.device_id = GlobalConfiguration.DEVICE_ID
        self.app_package = GlobalConfiguration.APP_PICKAGE

        # change follow the diver
        self.current_activity = 'not start'
        self.current_app_package = 'not start'

        # init the device environment
        self.driver = u2.connect(self.device_id)
        self.driver.implicitly_wait(10)

    def restart(self):
        self.driver.shell(GlobalConfiguration.STOP_INSTRUCMENT_CMD)
        time.sleep(0.5)
        self.driver.shell(GlobalConfiguration.START_INSTRUCMENT_CMD)
        self.driver.app_wait(GlobalConfiguration.APP_PICKAGE, front=True)
        time.sleep(2)

    def getUIHierarchy(self):
        # TODO after 10s should exit the program and restart [the work should follow the logcat]
        count = 0
        while self.driver.current_app()['package'] != GlobalConfiguration.APP_PICKAGE and count < 5:
            print('wait', self.driver.current_app()['package'])
            time.sleep(0.5)
            count += 1
        ui_hierarchy = self.driver.dump_hierarchy()
        if count == 5:
            if GlobalConfiguration.ExplorationStatus != GlobalConfiguration.STATE_CRASH_LABEL:
                GlobalConfiguration.ExplorationStatus = GlobalConfiguration.STATE_END_LABEL
        return ui_hierarchy

    def step(self, cmds):
        print(cmds)
        for cmd in cmds:
            print("adb shell " + cmd)
            os.system("adb shell " + cmd)
            # output = self.driver.shell(cmd, stream=True)
            # try:
            #     # read each unclosed line
            #     for line in output.iter_lines():
            #         print(line.decode('utf8'))
            # finally:
            #     output.close()
        self.current_app_package = self.driver.current_app()['package']
        self.current_activity = self.driver.current_app()['activity']

    # stop the current app and save coverage.ec file
    def stop(self):
        self.driver.shell(GlobalConfiguration.STOP_INSTRUCMENT_CMD)
        time.sleep(1)
