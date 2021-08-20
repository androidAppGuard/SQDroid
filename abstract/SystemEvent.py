import random

class SystemEvent(object):
    EVENT_PREFIX_CMD = 'input keyevent '
    SystemEventList = {
        'EVENT_BACK_CMD': [EVENT_PREFIX_CMD + '4'],  # can think about trigger twice
        'EVENT_HOME_CMD': [EVENT_PREFIX_CMD + '3'],
        'ENENT_OPENBROWSER_CMD': [EVENT_PREFIX_CMD + '64'],  # open the browser
        'EVENT_ADDVOLUME_CMD': [EVENT_PREFIX_CMD + '24'],
        'EVENT_ADDVOLUME_CMD': [EVENT_PREFIX_CMD + '25'],
        'EVENT_NAVIGATE_SURE_CMD': [EVENT_PREFIX_CMD + '23'],
        'EVENT_NAVIGATE_UP_CMD': [EVENT_PREFIX_CMD + '19'],
        'EVENT_NAVIGATE_DOWN_CMD': [EVENT_PREFIX_CMD + '20'],
        'EVENT_NAVIGATE_LEFT_CMD': [EVENT_PREFIX_CMD + '21'],
        'EVENT_NAVIGATE_RIGHT_CMD': [EVENT_PREFIX_CMD + '22'],
        'EVENT_CAPS_LOCK_CMD': [EVENT_PREFIX_CMD + '115'],
    }


    @staticmethod
    def generate_system_cmd():
        index = random.randint(0, len(SystemEvent.SystemEventList)-1)
        index_key = list(SystemEvent.SystemEventList.keys())[index]
        return SystemEvent.SystemEventList[index_key]

# print(SystemEvent.generate_system_cmd())