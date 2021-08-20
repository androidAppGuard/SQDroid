from settings.GlobalConfiguration import GlobalConfiguration
from abstract.UILayoutObject import UILayoutObject
from abstract.UIExecutableObject import UIExecutableObject
import hashlib

# static class
class Action(object):
    # action type
    click = 'tap'
    check = 'tap'
    textEdit = 'text'
    longClick = 'swipe'
    scroll = 'swipe'
    back = 'back'

    # the source of action
    actionFromStaticAnalysis = "static";
    actionFromScreenAnalysis = "screen";
    actionFromSystem = "system";

    # the global total number of action
    actionNumber = 0

    # the initial value of action
    actionInitValue = GlobalConfiguration.INITIAL_VALUE

    textViewLongClickByIndex = "clickLongTextViewByIndex";
    imageBtnClick = "clickImgBtn";
    imageViewClick = "clickImgView";
    menuItemClick = "clickMenuItem";
    checkboxClick = "clickCheckBox";
    radiobuttonClick = "clickRadioButton";
    togglebuttonClick = "clickToggleButton";
    buttonClick = "";
    textViewClick = "clickIdx";
    editTextClick = "key_event";

    @staticmethod
    def computActionMD5(uiObject, actionType):
        content = ''
        if isinstance(uiObject, UILayoutObject):
            content += uiObject.cis + ';' + str(uiObject.boundsX) + ';' + str(uiObject.boundsY) + ';' + str(uiObject.boundsWidth) + ';' + str(uiObject.boundsHight) +';' + actionType
        elif isinstance(uiObject, UIExecutableObject):
            content += uiObject.cis + ';' + uiObject.className + ';' + uiObject.index +';' + actionType
        md5_value = hashlib.md5(content.encode('utf8')).hexdigest()
        return md5_value

    @staticmethod
    def actionNumberIncrement():
        Action.actionNumber +=1

    @staticmethod
    def getActionNumber():
        return Action.actionNumber