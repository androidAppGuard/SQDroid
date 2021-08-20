import os

SQ_testing2_dir = r"F:\Paper\SQTesting2"
Monkey_dir = r"/opt/apks/monkey_app"
Sapienz_dir = r"/opt/apks/sapienz_app"
stoat_dir = r"/opt/apks/stoat_app"
SQ_testing_dir = r"/opt/apks/SQTesting"


def get_SQtesting_Monkey_StoatCrashes(DIR):
    statics_exception_file = os.path.join(DIR, 'exception_result.txt')
    ret = {}
    for dir in os.listdir(DIR):
        if len(dir.split(".")) == 1:
            # process
            print(dir)
            file_path = os.path.join(os.path.join(DIR, dir), 'log.txt')
            exception_file = os.path.join(os.path.join(DIR, dir), 'exception.txt')
            exception_ret_file = os.path.join(os.path.join(DIR, dir), 'exception_ret.txt')

            # logcat
            exception_info = []
            with open(file_path, "r", encoding='UTF-8') as log_file:
                for line in log_file.readlines():
                    if 'Exception' in line.strip():
                        exception_info.append(line)
            with open(exception_file, 'w', encoding='utf-8') as ret_file:
                for line in exception_info:
                    ret_file.write(line)
                    ret_file.write("\n")

            pid_set = {}
            with open(exception_file, "r", encoding='UTF-8') as ret_file:
                for line in ret_file.readlines():
                    if len(line.strip()) > 31:
                        # if 'Exception' in line.strip():
                        if line.strip()[25:30] not in pid_set.keys():
                            pid_set.update({line.strip()[25:30]: [line.strip()]})
                        else:
                            pid_set[line.strip()[25:30]].append(line.strip())
            with open(exception_ret_file, 'w', encoding='utf-8') as ret_file:
                for key in pid_set.keys():
                    for line in pid_set[key]:
                        for words in line.split(" "):
                            if "Exception" in words:
                                if words not in ret.keys():
                                    ret.update({words: 1})
                                else:
                                    ret[words] += 1
                        ret_file.write(line)
                    ret_file.write("\n")
    with open(statics_exception_file, 'w', encoding='utf-8') as ret_file:
        for key in ret.keys():
            ret_file.write(key + " " + str(ret[key]))
            ret_file.write("\n")


def get_Sapienz(DIR):
    statics_exception_file = os.path.join(DIR, 'exception_result.txt')
    ret = {}
    for dir in os.listdir(DIR):
        if len(dir.split(".")) == 1:
            # process
            print(dir)
            file_path = os.path.join(os.path.join(DIR, dir), 'log.txt')
            exception_file = os.path.join(os.path.join(DIR, dir), 'exception.txt')
            exception_ret_file = os.path.join(os.path.join(DIR, dir), 'exception_ret.txt')

            # logcat
            exception_info = []
            with open(file_path, "r", encoding='UTF-8') as log_file:
                for line in log_file.readlines():
                    if 'Exception' in line.strip():
                        exception_info.append(line)
            with open(exception_file, 'w', encoding='utf-8') as ret_file:
                for line in exception_info:
                    ret_file.write(line)
                    ret_file.write("\n")
            pid_set = {}
            with open(exception_file, "r", encoding='UTF-8') as ret_file:
                for line in ret_file.readlines():
                    # if 'Exception' in line.strip():
                    if '(' in line.strip() and ')' in line.strip():
                        key = line[line.find('('):line.find(')') + 1]
                        # print(key)
                        if key not in pid_set.keys():
                            pid_set.update({key: [line.strip()]})
                        else:
                            pid_set[key].append(line.strip())
            with open(exception_ret_file, 'w', encoding='utf-8') as ret_file:
                for key in pid_set.keys():
                    for line in pid_set[key]:
                        for words in line.split(":"):
                            if "Exception" in words:
                                if words not in ret.keys():
                                    ret.update({words: 1})
                                else:
                                    ret[words] += 1
                        ret_file.write(line)
                    ret_file.write("\n")
    ret_new = {}
    for key in ret.keys():
        if " " in key:
            for words in key.split(" "):
                if "Exception" in words:
                    if words in ret_new.keys():
                        ret_new[words] += ret[key]
                    else:
                        ret_new.update({words: ret[key]})
                    break
    with open(statics_exception_file, 'w', encoding='utf-8') as ret_file:
        for key in ret_new.keys():
            ret_file.write(key + " " + str(ret_new[key]))
            ret_file.write("\n")


# get_SQtesting_Monkey_StoatCrashes(SQ_testing_dir)
# get_SQtesting_Monkey_StoatCrashes(stoat_dir)
# get_SQtesting_Monkey_StoatCrashes(Monkey_dir)
# get_Sapienz(Sapienz_dir)

def getAllException():
    monkey_path = r'D:\paper\Result\monkey\exception_result.txt'
    sapienz_path = r'D:\paper\Result\sapienz\exception_result.txt'
    stoat_path = r'D:\paper\Result\stoat\exception_result.txt'
    SQtesting_path = r'D:\paper\Result\SQtesting\exception_result.txt'

    monkey_dict = {}
    with open(monkey_path, "r", encoding='UTF-8') as file:
        for line in file.readlines():
            if ":" in line.strip().split(" ")[0]:
                key = line.strip().split(" ")[0].split(":")[0]
            else:
                key = line.strip().split(" ")[0]
            if ":" in line.strip().split(" ")[1]:
                value = line.strip().split(" ")[1].split(":")[0]
            else:
                value = line.strip().split(" ")[1]
            monkey_dict.update({key: value})

    sapienz_dict = {}
    with open(sapienz_path, "r", encoding='UTF-8') as file:
        for line in file.readlines():
            if ":" in line.strip().split(" ")[0]:
                key = line.strip().split(" ")[0].split(":")[0]
            else:
                key = line.strip().split(" ")[0]
            if ":" in line.strip().split(" ")[1]:
                value = line.strip().split(" ")[1].split(":")[0]
            else:
                value = line.strip().split(" ")[1]
            sapienz_dict.update({key: value})

    stoat_dict = {}
    with open(stoat_path, "r", encoding='UTF-8') as file:
        for line in file.readlines():
            if ":" in line.strip().split(" ")[0]:
                key = line.strip().split(" ")[0].split(":")[0]
            else:
                key = line.strip().split(" ")[0]
            if ":" in line.strip().split(" ")[1]:
                value = line.strip().split(" ")[1].split(":")[0]
            else:
                value = line.strip().split(" ")[1]
            stoat_dict.update({key: value})

    SQtesting_dict = {}
    with open(SQtesting_path, "r", encoding='UTF-8') as file:
        for line in file.readlines():
            if ":" in line.strip().split(" ")[0]:
                key = line.strip().split(" ")[0].split(":")[0]
            else:
                key = line.strip().split(" ")[0]
            if ":" in line.strip().split(" ")[1]:
                value = line.strip().split(" ")[1].split(":")[0]
            else:
                value = line.strip().split(" ")[1]
            SQtesting_dict.update({key: value})

    # SQtesting monkey
    repeat = 0
    norepeat1 = 0
    norepeat2 = 0
    # 37 : 117 : 63  SQtesting : monkey
    # 21 : 117 : 41  SQtesting stoat
    # 30 : 117 : 58  SQtesting sapienz
    # 27 : 63 : 58  monkey sapienz
    # 17 : 63 : 41    monkey stoat
    # 18 : 58 : 41    sapienz stoat
    dict1 = SQtesting_dict
    dict2 = sapienz_dict
    for key in dict1.keys():
        if key in dict2.keys():
            repeat += 1
        else:
            norepeat1 += 1
    for key in dict2.keys():
        if key not in dict1.keys():
            norepeat2 += 1

    print(repeat, ":", norepeat1, ":", norepeat2)
    # print(len(monkey_dict.keys()))
    # print(len(sapienz_dict))
    # print(len(stoat_dir))
    # print(len(SQtesting_dict))


getAllException()
