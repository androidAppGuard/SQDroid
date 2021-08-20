from settings.GlobalConfiguration import GlobalConfiguration
from abstract.Action import Action
import random


class AppAction(object):

    def __init__(self, actionId, actionType, actionSource, textContent, bounds, className):
        self.actionId = actionId
        self.actionType = actionType
        self.actionSource = actionSource
        self.actionValue = GlobalConfiguration.INITIAL_VALUE
        self.textContent = textContent
        self.bounds = bounds  # [boundsX, boundsY, boundsWidth, boundsHight]
        self.className = className
        self.executeCmds = self.generateActionCmd()
        self.actionTimes = GlobalConfiguration.INITIAL_TIME
        pass

    # generate positions event executed by adb
    def generateActionCmd(self):
        cmds = []
        # input swipe 360 531 720 1061 300

        if self.actionType == Action.click:
            cmd = 'input '
            positionX = self.bounds[0] + self.bounds[2] / 2
            positionY = self.bounds[1] + self.bounds[3] / 2
            cmd += Action.click + ' ' + str(positionX) + ' ' + str(positionY)
            cmds.append(cmd)
        elif self.actionType == Action.check:
            positionX = self.bounds[0] + self.bounds[2] / 2
            positionY = self.bounds[1] + self.bounds[3] / 2
            counts = 2 + random.randint(0, 10) % 2
            for i in range(0, counts):
                cmd = 'input '
                cmd += Action.check + ' ' + str(positionX) + ' ' + str(positionY)
                cmds.append(cmd)
        elif self.actionType == Action.textEdit:
            positionX = self.bounds[0] + self.bounds[2] / 2
            positionY = self.bounds[1] + self.bounds[3] / 2
            # get the focus of textView Widget
            cmd = 'input ' + Action.click + ' ' + str(positionX) + ' ' + str(positionY)
            cmds.append(cmd)
            if random.randint(0, 2) % 2 == 0:  # 随机清空文本
                for i in range(0, len(self.textContent)):
                    cmd = 'input '
                    cmd += 'keyevent' + ' ' + str(GlobalConfiguration.EVENT_DELETE_CHARACTOR)
                    cmds.append(cmd)
            cmd = 'input '
            cmd += Action.textEdit + ' ' + '\'' + GlobalConfiguration.EDIT_TEXT[random.randint(0, len(GlobalConfiguration.EDIT_TEXT)-1)]+ '\''
            cmds.append(cmd)
            # close keyboard
            cmds.append('input keyevent 4')
        elif self.actionType == Action.longClick:
            positionX = self.bounds[0] + self.bounds[2] / 2
            positionY = self.bounds[1] + self.bounds[3] / 2
            cmd = 'input '
            cmd += Action.longClick + ' ' + str(positionX) + ' ' + str(positionY) + ' ' + str(positionX) + ' ' + str(
                positionY) + ' ' + str(GlobalConfiguration.SWAR_TIME)
            cmds.append(cmd)
        elif self.actionType == Action.scroll:
            positionX = self.bounds[0] + self.bounds[2] / 2
            positionY = self.bounds[1] + self.bounds[3] / 2
            # select direction randomly
            endX = 0
            endY = 0
            if random.randint(0, 2) % 2 == 0:
                endX = max(0, positionX - self.bounds[2] / GlobalConfiguration.SWAP_RATIO)
                endY = max(0, positionY - self.bounds[3] / GlobalConfiguration.SWAP_RATIO)
            else:
                endX = min(GlobalConfiguration.SCREEN_WIDTH,
                           positionX + self.bounds[2] / GlobalConfiguration.SWAP_RATIO)
                endY = min(GlobalConfiguration.SCREEN_HIGHT,
                           positionY + self.bounds[3] / GlobalConfiguration.SWAP_RATIO)
            cmd = 'input '
            cmd += Action.scroll + ' ' + str(positionX) + ' ' + str(positionY) + ' ' + str(endX) + ' ' + str(
                endY) + ' ' + str(GlobalConfiguration.SWAR_TIME)
            cmds.append(cmd)
        elif self.actionType == Action.back:
            self.actionValue = GlobalConfiguration.INITIAL_VALUE / 10.0
            cmds.append("input keyevent 4")
        return cmds
