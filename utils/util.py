import os
import time
from settings.GlobalConfiguration import GlobalConfiguration

class Util:
    @staticmethod
    def printQ_table(q_table, preStateMD5):
        for action_key in q_table[preStateMD5].executableActions.keys():
            print(q_table[preStateMD5].executableActions[action_key].actionValue)

    def executeCmd(cmd):
        result = ""
        with os.popen(cmd) as console:
            result = console.read()
        return result

    @staticmethod
    def save_coverage_file():
        # create out file

        count = 0
        while GlobalConfiguration.THREAD_COVERAGE or count < 60:
            time.sleep(2)
            os.system("")
            pass