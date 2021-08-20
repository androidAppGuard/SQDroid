from settings.GlobalConfiguration import GlobalConfiguration
from abstract.Action import Action
from abstract.AppAction import AppAction
import hashlib


class AppState(object):

    def __init__(self, stateId, uiPage):
        self.stateId = stateId
        self.uiPage = uiPage

        # the number of widget in AppState
        self.textViewCnt = 0
        self.buttonCnt = 0
        self.imageButtonCnt = 0
        self.toggleButtonCnt = 0
        self.editTextCnt = 0
        self.checkBoxCnt = 0
        self.radioButtonCnt = 0
        self.checkedTextViewCnt = 0
        self.seekbarCnt = 0

        self.md5Value = self.computeMD5()
        self.executableActions = dict() # AppAction(md5)->AppAction
        self.updateActions()

    # compute the md5 value by layout widget positions UIPage(md5) = AppAction(md5)
    def computeMD5(self):
        content = ''
        md5_set = set()
        for uiLayoutObject in self.uiPage.uiLayoutObjects:
            if uiLayoutObject.packageName == GlobalConfiguration.APP_PICKAGE:
                # state clustering module
                # if (uiLayoutObject.cis[0:len(uiLayoutObject.cis)-1] + ';' + uiLayoutObject.className) not in md5_set:
                #     content += uiLayoutObject.cis[0:len(uiLayoutObject.cis)-1] + ';' + uiLayoutObject.className
                #     md5_set.add(uiLayoutObject.cis[0:len(uiLayoutObject.cis)-1] + ';' + uiLayoutObject.className)

                # define executable widgets as state
                if (uiLayoutObject.cis[0:len(uiLayoutObject.cis)] + ';' + uiLayoutObject.className) not in md5_set:
                    content += uiLayoutObject.cis[0:len(uiLayoutObject.cis)] + ';' + uiLayoutObject.className
                    md5_set.add(uiLayoutObject.cis[0:len(uiLayoutObject.cis)] + ';' + uiLayoutObject.className)
        md5_value = hashlib.md5(content.encode('utf8')).hexdigest()
        return md5_value

    # update executable actions by current UIPage
    def updateActions(self):
        # each state has back action
        # self.executableActions.update({"backevent":AppAction(None, Action.back, Action.actionFromSystem,"xxx", None, None)})
        # UILayout Scroall
        for uiLayoutObject in self.uiPage.uiLayoutObjects:
            if uiLayoutObject.isScrollable and uiLayoutObject.packageName == GlobalConfiguration.APP_PICKAGE:
                # Layout action can identify by bounds attr while executable widget cannot
                md5Key = Action.computActionMD5(uiLayoutObject, Action.scroll)
                # not exist then create AppAction
                if md5Key not in self.executableActions.keys():
                    actionId = None
                    actionType = Action.scroll
                    actionSource = Action.actionFromStaticAnalysis
                    textContent = 'layout text'
                    bounds = [uiLayoutObject.boundsX, uiLayoutObject.boundsY, uiLayoutObject.boundsWidth, uiLayoutObject.boundsHight]
                    appAction = AppAction(actionId, actionType, actionSource,textContent, bounds, uiLayoutObject.className)
                    self.executableActions.update({md5Key: appAction})
        # UIExecutable widget action[click long-click check]
        for uiExecuteObject in self.uiPage.uiExecutableObjects:
            if uiExecuteObject.packageName == GlobalConfiguration.APP_PICKAGE:
                actionSource = Action.actionFromStaticAnalysis
                textContent = uiExecuteObject.text
                className = uiExecuteObject.className
                bounds = [uiExecuteObject.boundsX, uiExecuteObject.boundsY, uiExecuteObject.boundsWidth,
                          uiExecuteObject.boundsHight]
                # record the number of widget type
                self.recordWidgetType(className)
                # TODO Now we consider only "click" and "long click" and  "check" and "scroll" and "edit"
                # click TODO GlobalConfiguration.TEXT_CLASS need to extract
                if uiExecuteObject.clickable == True and GlobalConfiguration.TEXT_CLASS not in uiExecuteObject.className:
                    md5Key = Action.computActionMD5(uiExecuteObject, Action.click)
                    # not exist then create AppAction
                    if md5Key not in self.executableActions.keys():
                        actionId = None
                        actionType = Action.click
                        appAction = AppAction(actionId, actionType, actionSource, textContent, bounds, className)
                        self.executableActions.update({md5Key: appAction})
                # longClick
                if uiExecuteObject.longClickable == True and GlobalConfiguration.TEXT_CLASS not in uiExecuteObject.className:
                    md5Key = Action.computActionMD5(uiExecuteObject, Action.longClick)
                    # not exist then create AppAction
                    if md5Key not in self.executableActions.keys():
                        actionId = None
                        actionType = Action.longClick
                        appAction = AppAction(actionId, actionType, actionSource, textContent, bounds, className)
                        self.executableActions.update({md5Key: appAction})
                # check
                if uiExecuteObject.checkable == True and GlobalConfiguration.TEXT_CLASS not in uiExecuteObject.className:
                    md5Key = Action.computActionMD5(uiExecuteObject, Action.check)
                    # not exist then create AppAction
                    if md5Key not in self.executableActions.keys():
                        actionId = None
                        actionType = Action.check
                        appAction = AppAction(actionId, actionType, actionSource, textContent, bounds, className)
                        self.executableActions.update({md5Key: appAction})
                # EditText
                if uiExecuteObject.clickable == True and GlobalConfiguration.TEXT_CLASS in uiExecuteObject.className:
                    md5Key = Action.computActionMD5(uiExecuteObject, Action.textEdit)
                    # not exist then create AppAction
                    if md5Key not in self.executableActions.keys():
                        actionId = None
                        actionType = Action.textEdit
                        appAction = AppAction(actionId, actionType, actionSource, textContent, bounds, className)
                        self.executableActions.update({md5Key: appAction})

        pass

    # assign the actionId
    def assignActionId(self):
        for executableAction_key in self.executableActions.keys():
            Action.actionNumberIncrement()
            self.executableActions[executableAction_key].actionId = Action.getActionNumber()

    # set the current UIPage
    def setUIPage(self, uiPage):
        self.uiPage = uiPage

    # record the number of widget type
    def recordWidgetType(self ,className):
        if className == 'android.widget.TextView':
            self.textViewCnt += 1
        elif className == 'android.widget.Button':
            self.buttonCnt += 1
        elif className == 'android.widget.ImageView':
            self.imageButtonCnt += 1
        elif className == 'android.widget.ToggleButton':
            self.toggleButtonCnt += 1
        elif className == 'android.widget.EditText':
            self.editTextCnt += 1
        elif className == 'android.widget.CheckBox':
            self.checkBoxCnt += 1
        elif className == 'android.widget.RadioButton':
            self.radioButtonCnt += 1
        elif className == 'android.widget.CheckedTextView':
            self.checkedTextViewCnt += 1
        elif className == 'android.widget.SeekBar':
            self.seekbarCnt += 1
        else:
            print(className ,': the widget type is not handled')

if __name__ == '__main__':
    content = ""
    md5_value = hashlib.md5(content.encode('utf8')).hexdigest()
    print(md5_value)
