from settings.GlobalConfiguration import GlobalConfiguration
from xml.dom.minidom import parseString
from abstract.UIPage import UIPage
from abstract.AppState import AppState
from abstract.AppAction import AppAction
from abstract.Action import Action
import random


class QLearningAgent(object):

    def __init__(self):
        self.q_table = dict()  # AppState(md5) -> AppState(executableActions[dict()]:AppAction(md5))
        self.semantic_path = GlobalConfiguration.SEMANTIC_PATH
        self.suite_path = GlobalConfiguration.SUITE_PATH

        self.current_state_md5 = None
        self.current_action_md5 = None

    # get the current AppState by UIHierarchy return Appstate Type
    def observe_environment(self, uiHierarchy):
        uiPage = UIPage(parseString(uiHierarchy).childNodes)
        appState_current = AppState(stateId=len(self.q_table.keys()) + 1, uiPage=uiPage)
        # judge appState weather in self.q_table, not: update  in: compare for new executableActions
        md5Value = appState_current.computeMD5()
        if md5Value not in self.q_table.keys():
            self.q_table.update({md5Value: appState_current})
            appState_current.assignActionId()
        # compare and add new executableActions
        else:
            for executableAction_key in appState_current.executableActions.keys():
                if executableAction_key not in self.q_table[md5Value].executableActions.keys():
                    appAction_add = appState_current.executableActions[executableAction_key]
                    # stateId and actionId should be managed by agent class
                    Action.actionNumberIncrement()
                    actionId = Action.getActionNumber()
                    actionType = appAction_add.actionType
                    actionSource = appAction_add.actionSource
                    textContent = appAction_add.textContent
                    bounds = appAction_add.bounds
                    className = appAction_add.className
                    appAction = AppAction(actionId, actionType, actionSource, textContent, bounds, className)
                    # add AppAction to executableActions dict
                    self.q_table[md5Value].executableActions.update({executableAction_key: appAction})
                    appState_current.recordWidgetType(
                        self.q_table[md5Value].executableActions[executableAction_key].className)
        self.current_state_md5 = md5Value
        return self.q_table[md5Value]

    # current selection: greedy policy  return: the cmds to execute
    def sample(self, state_key):
        executableActions = self.q_table[state_key].executableActions
        # select actions with max value
        selection_cmds = []
        selection_keys = []
        cur_val = 0.0
        for executableAction_key in executableActions.keys():
            if executableActions[executableAction_key].actionType != Action.textEdit and executableActions[executableAction_key].actionValue > cur_val:
                print(executableActions[executableAction_key].actionValue)
                selection_cmds.clear()
                selection_keys.clear()
                selection_cmds.append(executableActions[executableAction_key].executeCmds)
                selection_keys.append(executableAction_key)
                cur_val = executableActions[executableAction_key].actionValue
            elif executableActions[executableAction_key].actionType != Action.textEdit and executableActions[executableAction_key].actionValue == cur_val:
                selection_cmds.append(executableActions[executableAction_key].executeCmds)
                selection_keys.append(executableAction_key)
            else:
                continue

        # no action to sample
        if cur_val == 0.0 or len(selection_cmds) == 0:  # action with no value
            if GlobalConfiguration.ExplorationStatus != GlobalConfiguration.STATE_CRASH_LABEL:
                GlobalConfiguration.ExplorationStatus = GlobalConfiguration.STATE_END_LABEL
            print("cur_val==0.0:", cur_val == 0.0, ' len(selection_cmds) == 0:', len(selection_cmds) == 0)
            return []
        index = random.randint(0, len(selection_cmds) - 1)
        self.current_action_md5 = selection_keys[index]
        self.q_table[state_key].executableActions[
            self.current_action_md5].actionTimes += 1  # increment the execution time
        # return selection_cmds[index]
        # add text context
        result_cmds = []
        for executableAction_key in executableActions.keys():
            if executableActions[executableAction_key].actionType == Action.textEdit:
                result_cmds.extend(executableActions[executableAction_key].executeCmds)
        result_cmds.extend(selection_cmds[index])
        return result_cmds

    def calculate_final_reward(self, frequency_reward, semantic_reward, visit_flag):
        explore_degree = 0
        for flag in visit_flag:
            if flag == 1:
                explore_degree += 1
        explore_degree = explore_degree * 1.0 / len(visit_flag)
        # the weight avoid to be 0
        reward = (explore_degree + 0.1) * frequency_reward + (1 - explore_degree + 0.1) * semantic_reward
        return reward

    # get the frequency reward in the current AppState
    def calculate_frequency_reward(self, state_key, action_key):
        if state_key == None or action_key == None or state_key not in self.q_table.keys() or action_key not in self.q_table[state_key].executableActions.keys():
            return 0.0
        return 1.0 / self.q_table[state_key].executableActions[action_key].actionTimes

    # get the semantic reward in the current AppState
    def calculate_semantic_reward(self, explored, sequence_list, visit_flag):
        match_count = 0
        for index in range(len(sequence_list)):
            sequence = sequence_list[index]
            flag = 0
            for i in range(len(explored)):
                if flag == 0:
                    # flag =1 : match tail party
                    for j in range(0, min(len(explored) - i, len(sequence))):
                        flag == 1
                        if (explored[i + j] != sequence[j]):
                            flag = 0
                            break
                    # flag =2 : match whole sequence
                    if flag == 1 and j == len(sequence) - 1:
                        flag = 2
                else:
                    break
            if flag != 0:
                match_count += 1
            if flag == 2:
                visit_flag[index] = 1
        return match_count * 1.0 / len(sequence_list)

    def learn(self, reward, pre_state_key, pre_action_key):
        if pre_state_key == None or pre_action_key == None or self.current_state_md5 not in self.q_table.keys() or pre_state_key not in self.q_table.keys() or pre_action_key not in self.q_table[pre_state_key].executableActions.keys():
            return None
        # calculate the target value(max)
        q_target = 0
        curAppState = self.q_table[self.current_state_md5]
        for executableAction_key in curAppState.executableActions.keys():
            if curAppState.executableActions[executableAction_key].actionValue > q_target:
                q_target = curAppState.executableActions[executableAction_key].actionValue
        # standard update equation
        self.q_table[pre_state_key].executableActions[pre_action_key].actionValue = \
            self.q_table[pre_state_key].executableActions[
                pre_action_key].actionValue + GlobalConfiguration.LEARNING_RATE * (reward +
                    GlobalConfiguration.GAMMY * q_target - self.q_table[pre_state_key].executableActions[
                pre_action_key].actionValue)

    # accurate the exploration speed
    def prune(self, state_key, action_key):
        if state_key != None or action_key != None or state_key not in self.q_table.keys() or action_key not in self.q_table[state_key].executableActions.keys():
            return
        self.q_table[state_key].executableActions[action_key].actionValue = 0.0
