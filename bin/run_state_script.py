import os

state_ret = {
    '10': '272',
    '11': '91',
    '12': '47',
    '14': '296',
    '15': '61',
    '16': '74',
    '18': '51',
    '19': '88',
    '1': '43',
    '21': '1',
    '22': '12',
    '24': '7',
    '27': '108',
    '28': '38',
    '29': '25',
    '2': '46',
    '30': '11',
    '32': '13',
    '35': '15',
    '36': '28',
    '37': '10',
    '38': '34',
    '39': '2',
    '3': '4',
    '40': '15',
    '41': '9',
    '43': '6',
    '44': '7',
    '45': '12',
    '46': '11',
    '47': '8',
    '48': '10',
    '49': '1',
    '4': '1',
    '50': '1',
    '51': '1',
    '52': '1',
    '53': '1',
    '54': '1',
    '55': '1',
    '56': '1',
    '57': '1',
    '5': '1',
    '6': '1',
    '7': '1',
    '8': '1',
    '9': '1'
}

SQ_testing2_dir = r"F:\Paper\SQTesting2"
SQ_testing_dir = r"/opt/apks/SQTesting"

DIR = SQ_testing_dir

state_dict = {}
for dir in os.listdir(DIR):
    if len(dir.split(".")) == 1:
        # process
        # print(dir)
        for states in os.listdir(os.path.join(os.path.join(DIR, dir))):
            if "state" in states:
                state_dict.update({dir.split("_")[0]: [states.split(".")[0]]})
for key in state_dict.keys():
    if key in state_ret.keys():
        state_dict[key].append(state_ret[key])

sequence_index = ['55', '5', '6', '7', '37', '54', '43', '3', '51', '50', '53', '9', '48', '4', '52', '47', '45', '41', '44', '46', '39', '8', '40', '30', '1', '38', '2', '36', '49', '56', '35', '13', '32', '29', '27', '28', '24', '19', '21', '22', '18', '17', '16', '14', '12', '15', '11', '10']
for index in sequence_index:
    print(index,":",state_dict[index])