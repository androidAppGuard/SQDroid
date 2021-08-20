from algorithm.rl.env import ENV
from algorithm.rl.agent import QLearningAgent
from abstract.SystemEvent import SystemEvent
from utils.util import Util
from settings.GlobalConfiguration import GlobalConfiguration
from abstract.UIPage import UIPage
from abstract.AppState import AppState
from xml.dom.minidom import parse
from threads.LogcatThread import LogcatThread
from threads.CoverageThread import CoverageThread

import os
import random
import time


class Explore(object):

    def __init__(self):
        self.env = ENV()
        self.agent = QLearningAgent()

        self.preStateMD5 = None
        self.preActionMD5 = None
        self.curStateMD5 = None
        self.curActionMD5 = None

        self.explored = None
        self.sequence_list = self.getSemanticSequence(GlobalConfiguration.SEMANTIC_PATH, GlobalConfiguration.APK_PATH)
        self.visit_flag = [0 for i in range(len(self.sequence_list))]
        print(self.sequence_list)

    def getSemanticSequence(self, data_dir, apk_path):
        dir = data_dir + '/' + apk_path.split('/')[-1].split(".")[0]
        print(dir)
        dir_list = os.listdir(dir)
        sequence_list = []
        for sequence_id in dir_list:
            if sequence_id != "coverage.ec":
                sequence_dir = os.path.join(dir, sequence_id)
                sequence = []
                for sequence_file in os.listdir(sequence_dir):
                    state_file = os.path.join(sequence_dir, sequence_file)
                    uiPage = UIPage(parse(state_file).childNodes)
                    appState_current = AppState(stateId=-1, uiPage=uiPage)
                    # judge appState weather in self.q_table, not: update  in: compare for new executableActions
                    md5Value = appState_current.computeMD5()
                    sequence.append(md5Value)
                sequence_list.append(sequence)
        return sequence_list

    def run_episode(self):
        self.env.restart()
        self.agent.observe_environment(self.env.getUIHierarchy())
        self.preStateMD5 = self.agent.current_state_md5
        pre_cmds = self.agent.sample(self.agent.current_state_md5)
        self.preActionMD5 = self.agent.current_action_md5
        self.explored = []
        self.repeated_counts = 0

        # TODO the logcat can stop the exploration
        while len(self.explored) < GlobalConfiguration.TEST_CASE_MAXLEN:
            self.env.step(pre_cmds)
            self.agent.observe_environment(self.env.getUIHierarchy())
            # prune operation
            if self.env.driver.current_app()['package'] != GlobalConfiguration.APP_PICKAGE:
                print('self.env.driver.current_app()[package] != GlobalConfiguration.APP_PICKAGE')
                if self.preStateMD5 == None or self.preActionMD5 == None or self.preStateMD5 not in self.agent.q_table.keys() or self.preActionMD5 not in \
                        self.agent.q_table[self.preStateMD5].executableActions.keys():
                    break
                # reduce value no try
                self.agent.q_table[self.preStateMD5].executableActions[self.preActionMD5].actionValue = \
                self.agent.q_table[self.preStateMD5].executableActions[self.preActionMD5].actionValue / 10
                break
            self.curStateMD5 = self.agent.current_state_md5
            self.explored.append(self.curStateMD5)
            # print("self.explored:",self.explored)

            # calculate the frequency reward
            frequency_reward = self.agent.calculate_frequency_reward(self.preStateMD5, self.preActionMD5)
            # calculate the semantic reward
            semantic_reward = self.agent.calculate_semantic_reward(self.explored, self.sequence_list, self.visit_flag)
            # calculate the final reward
            reward = self.agent.calculate_final_reward(frequency_reward, semantic_reward, self.visit_flag)

            # learn
            self.agent.learn(reward, self.preStateMD5, self.preActionMD5)

            cur_cmds = self.agent.sample(self.curStateMD5)
            self.curActionMD5 = self.agent.current_action_md5

            # no cmd to execute
            if len(cur_cmds) == 0:  # TODO the condision should include exclude app_package
                print('len(cur_cmds) == 0')
                # action value set to zero
                self.agent.prune(self.preStateMD5, self.preActionMD5)
                cur_cmds.append("input tap 225 457")
                self.env.step(cur_cmds)
                print("len(cur_cmds) == 0!")
                # TODO It is a end flag
                # DigraphThread.addInNormalRelation(self.agent.q_table[self.preStateMD5].stateId, self.agent.q_table[self.preStateMD5].executableActions[self.preActionMD5].actionId)
                break

            # send system events [random] 0.01
            # if random.randint(1, 100) < 100 * GlobalConfiguration.SYSTEM_EVENT_PROBILITY:
            #     cur_cmds.extend(SystemEvent.generate_system_cmd())

            # is a loop
            if self.preStateMD5 == self.curStateMD5:
                self.repeated_counts += 1
                if self.repeated_counts > 10:
                    # click back event
                    cur_cmds.append("input keyevent 4")
                    self.repeated_counts = 0
                    print("state repeated max times!")
            else:
                self.repeated_counts = 0
            # print('state Id:', self.agent.q_table[self.preStateMD5].stateId, ' ' ,self.agent.q_table[self.curStateMD5].stateId, ' :', self.agent.q_table[self.preStateMD5].executableActions[self.preActionMD5].actionId)
            # DigraphThread.addRelation(self.agent.q_table[self.preStateMD5].stateId, self.agent.q_table[self.curStateMD5].stateId, self.agent.q_table[self.preStateMD5].executableActions[self.preActionMD5].actionId)
            # DigraphThread.viewGraph()

            pre_cmds = cur_cmds
            self.preStateMD5 = self.curStateMD5
            self.preActionMD5 = self.curActionMD5
        self.env.stop()


def main():
    for apk_name in os.listdir(GlobalConfiguration.APK_DIR):
        if len(apk_name.split(".")) == 2 and apk_name.split(".")[1] == "apk":
            apk_path = os.path.join(GlobalConfiguration.APK_DIR, apk_name)
            # generate corresponding APP_PICKAGE
            GlobalConfiguration.APK_PATH = apk_path
            GlobalConfiguration.APP_PICKAGE = \
                Util.executeCmd(
                    "aapt dump badging " + GlobalConfiguration.APK_PATH + "| grep package:").strip().split(
                    " ")[1].split("'")[1]
            GlobalConfiguration.APP_LUNCH_ACTIVITY = Util.executeCmd(
                "aapt dump badging " + GlobalConfiguration.APK_PATH + "| grep launchable-activity:").strip().split(
                " ")[1].split("'")[1]

            GlobalConfiguration.START_INSTRUCMENT_CMD = "am start -n " + GlobalConfiguration.APP_PICKAGE + '/' + GlobalConfiguration.APP_LUNCH_ACTIVITY
            GlobalConfiguration.STOP_INSTRUCMENT_CMD = "am force-stop " + GlobalConfiguration.APP_PICKAGE

            # generate outfile
            GlobalConfiguration.OUT_DIR = GlobalConfiguration.APK_DIR + '/' + apk_name.split(".")[0] + "_SQtestingout"
            if not os.path.exists(GlobalConfiguration.OUT_DIR):
                os.makedirs(GlobalConfiguration.OUT_DIR)
                print("creating ok")
            # generate logfile.txt and crash.txt
            GlobalConfiguration.LOGCAT_LOG_PATH = os.path.join(GlobalConfiguration.OUT_DIR, 'logcat.txt')
            GlobalConfiguration.LOGCAT_CRASH_PATH = os.path.join(GlobalConfiguration.OUT_DIR, 'crash.txt')
            # clean coverage.ec
            os.system("adb shell rm /mnt/sdcard/coverage.ec")
            # uninstall apk
            os.system('adb uninstall ' + GlobalConfiguration.APP_PICKAGE)
            # install apk
            os.system('adb install ' + apk_path)
            print("prepare work finish!")

            # start logcat
            logcatThread = LogcatThread('L1')
            logcatThread.start()
            # # start save coverage.ec
            coverageThread = CoverageThread("C1")
            coverageThread.start()

            # start exploring
            start = time.time()
            explorer = Explore()
            while True:
                explorer.run_episode()
                if int(time.time() - start) > 3700:  # 3700
                    break
            print("one explore ok!")
            # close logcatThread
            logcatThread.close_monitor()
            coverageThread.join()
            # recorn state number
            if not os.path.exists(
                    os.path.join(GlobalConfiguration.OUT_DIR, str(len(explorer.agent.q_table.keys())) + '.state')):
                os.mkdir(os.path.join(GlobalConfiguration.OUT_DIR, str(len(explorer.agent.q_table.keys())) + '.state'))

            # uninstall apk
            os.system('adb uninstall ' + GlobalConfiguration.APP_PICKAGE)


# testing explore
if __name__ == '__main__':
    # DigraphThread('T1').start()
    main()
