from abstract.UILayoutObject import UILayoutObject
from abstract.UIExecutableObject import UIExecutableObject
from abstract.AppState import AppState
from abstract.common.Utils import Utils
from settings.GlobalConfiguration import GlobalConfiguration


class UIPage(object):
    def __init__(self, nodeList):
        self.indexList = []
        self.uiLayoutObjects = []
        self.uiExecutableObjects = []
        self.analyzeNode(nodeList, False, False, False)

        # todo the number of  widget to record
        pass

    # analyze the UI xml nodes
    def analyzeNode(self, nodeList, clickable, longClickable, checkable):
        for node in nodeList:
            # ignore the com.android.systemui className widget
            if node.nodeName == 'node' and node.getAttribute('package') == GlobalConfiguration.APP_PICKAGE:
                attrIndex = node.getAttribute('index')
                if attrIndex != None and attrIndex != '':
                    self.indexList.append(attrIndex)
                cis = self.getCIS(indexList=self.indexList)
                packageName = node.getAttribute('package')
                className = node.getAttribute('class')
                isScrollable = True if node.getAttribute('scrollable') == 'true' else False
                clickable = True if node.getAttribute('clickable') == 'true' else False or clickable
                longClickable = True if node.getAttribute('long-clickable') == 'true' else False or longClickable
                checkable = True if node.getAttribute('checkable') == 'true' else False or checkable
                (x, y, width, hight) = Utils.parseBoundsStr(node.getAttribute('bounds'))
                # no leafNode
                if node.hasChildNodes():
                    # create layoutObject
                    ui_LayoutObject = UILayoutObject(cis, packageName, className, isScrollable)
                    # assign bounds attr
                    ui_LayoutObject.setBoundsAttr(x, y, width, hight)
                    self.uiLayoutObjects.append(ui_LayoutObject)
                # is leafNode(contains button textview imagebutton...identify by className)
                else:
                    text = node.getAttribute('text')
                    resourceId = node.getAttribute('resource-id')
                    contentDesc = node.getAttribute('content-desc')
                    ui_ExecutableObject = UIExecutableObject(cis, packageName, className, clickable,
                                                             longClickable, checkable, text, resourceId, contentDesc,
                                                             attrIndex)
                    ui_ExecutableObject.setBoundsAttr(x, y, width, hight)
                    self.uiExecutableObjects.append(ui_ExecutableObject)
            # recursion child nodes
            self.analyzeNode(node.childNodes, clickable, longClickable, checkable)
            if node.nodeName == 'node' and node.getAttribute('package') == GlobalConfiguration.APP_PICKAGE:
                attrIndex = node.getAttribute('index')
                if attrIndex != None and attrIndex != '':
                    self.indexList.pop()

    def getCIS(self, indexList):
        ret = ""
        for index in indexList:
            ret += str(index)
        return ret

if __name__=='__main__':
    import uiautomator2 as u2
    from xml.dom.minidom import parseString

    driver = u2.connect('emulator-5554')
    node = parseString(driver.dump_hierarchy())

    # test AppState md5 is what we abstract
    import time
    md5_dict = dict()
    while True:
        appState1 = AppState(stateId=1, uiPage=UIPage(parseString(driver.dump_hierarchy()).childNodes))
        if appState1.md5Value not in md5_dict.keys():
            md5_dict.update({appState1.md5Value:appState1})
            print(len(md5_dict.keys()))
        input("input:")

    # uiPage = UIPage(node.childNodes)
    # # testing UILayoutObject
    # # print(len(uiPage.uiLayoutObjects))
    # # for uiLayoutObject in uiPage.uiLayoutObjects:
    # #     if uiLayoutObject.isScrollable:
    # #         print(uiLayoutObject)
    #
    # # testing UIExecutableObject
    # # print(len(uiPage.uiExecutableObjects))
    # # for uiExecuteObject in uiPage.uiExecutableObjects:
    # #     if uiExecuteObject.clickable or uiExecuteObject.longClickable or uiExecuteObject.checkable:
    # #         print(uiExecuteObject)
    #
    # # testing AppState
    # appState = AppState(stateId=1, uiPage=uiPage)
    # print(appState.md5Value)
    # appState.assignActionId()
    # print(len(appState.executableActions.keys()))
    # for key in appState.executableActions.keys():
    #     print(appState.executableActions[key].actionId, ' adb sehll ', appState.executableActions[key].executeCmds)
    # # print('appState.buttonCnt', ' ', appState.buttonCnt)
    # # print('appState.textViewCnt', ' ', appState.textViewCnt)
    # # print('appState.imageButtonCnt', ' ', appState.imageButtonCnt)
    # # print('appState.toggleButtonCnt', ' ', appState.toggleButtonCnt)
    # # print('appState.editTextCnt', ' ', appState.editTextCnt)
    # # print('appState.checkBoxCnt', ' ', appState.checkBoxCnt)
    # # print('appState.radioButtonCnt', ' ', appState.radioButtonCnt)
    # # print('appState.checkedTextViewCnt', ' ', appState.checkedTextViewCnt)
    # # print('appState.seekbarCnt', ' ', appState.seekbarCnt)
