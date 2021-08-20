from datetime import datetime
class GlobalConfiguration(object):
    # Testing Android App settings
    APK_DIR = r"/opt/apks/SQTesting"
    TEST_CASE_MAXLEN = 100
    APP_PICKAGE = 'com.mattallen.loaned'
    APP_LUNCH_ACTIVITY = "xxx"
    START_INSTRUCMENT_CMD = 'xxx'
    STOP_INSTRUCMENT_CMD = 'xxx'
    OUT_DIR = 'xxx'

    DEVICE_ID = 'emulator-5554'
    EDIT_TEXT = ['12', '24']

    SWAP_RATIO = 3 # swap radio on the operatable widget
    SWAR_TIME = 1000
    SYSTEM_EVENT_PROBILITY = 0.05

    SCREEN_WIDTH = 480
    SCREEN_HIGHT = 800

    TEXT_CLASS = '.EditText'
    EVENT_DELETE_CHARACTOR = 67

    # Q-learning Setting
    APK_PATH = r"xxx"
    SEMANTIC_PATH = r"/opt/code/STesting/data"
    SUITE_PATH = ''
    GAMMY = 0.99
    INITIAL_VALUE = 500.0
    INITIAL_TIME = 1.0 # initial frequency
    LEARNING_RATE = 1.0


    # Thread Setting
    INTERVAL_TIME = 0.5

    # view setting
    STATE_NORMAL_LABEL = 'normal'
    STATE_END_LABEL = 'END'
    STATE_END_LABEL_COLOR = 'gray'
    STATE_CRASH_LABEL = 'CRASH'
    STATE_CRASH_LABEL_COLOR = 'red'
    ExplorationStatus = STATE_NORMAL_LABEL

    # logcat setting
    LOGCAT_BUFF_MAXSIZE = 10
    LOGCAT_COMMAND_MONITOR = 'adb -s ' + DEVICE_ID + ' logcat -v threadtime'
    LOGCAT_MATCH_ERROR = r"^\d{2}-\d{2} (\d{2}:){2}\d{2}.\d{3}([ ]{1,} \d{1,}){2}[ ]{1,}E"
    LOGCAT_MATCH_CRASH = r'* Exception *'
    LOGCAT_LOG_PATH = 'xxx'
    LOGCAT_CRASH_PATH = 'xxx'

