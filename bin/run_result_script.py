monkey_file = r"D:\paper\Result\monkey\result.txt"
stoat_file = r"D:\paper\Result\stoat\result.txt"
sapienz_file = r"D:\paper\Result\sapienz\result.txt"
SQtesting_file = r"F:\Paper\SQTesting\result.txt"
SQtesting2_file = r"D:\paper\Result\SQtesting2\result.txt"


def getResult(file):
    result = {}
    with open(file) as f:
        coverage = ""
        app = ""
        for line in f.readlines():
            if "Paper" in line or "paper" in line:
                if app != "" and coverage != "":
                    if "-debug" in app.split("_")[1]:
                        result.update({app.split("_")[1].split("-")[0]: coverage})
                    else:
                        result.update({app.split("_")[1]: coverage})
                app = line.strip().split("/")[-1]
            else:
                coverage = line.strip().split(",")[-1]
                # instruction_total = line.split("of")[-1].replace(","+coverage+"\n", "")
                # print(instruction_total)
        if "-debug" in app.split("_")[1]:
            result.update({app.split("_")[1].split("-")[0]: coverage})
        else:
            result.update({app.split("_")[1]: coverage})
    return result


monkey_result = getResult(monkey_file)
stoat_result = getResult(stoat_file)
sapienz_result = getResult(sapienz_file)
SQtesting_result = getResult(SQtesting_file)
SQtesting2_result = getResult(SQtesting2_file)

# print(monkey_result)
# print(stoat_result)
# print(sapienz_result)
# print(SQtesting_result)
# print(SQtesting2_result)

def getFinalResult(monkey_result, sapienz_result, stoat_result, SQtesting_result, SQtesting2_result):
    final_result = {}
    for key in monkey_result.keys():
        if key in final_result.keys():
            continue
        else:
            if key in sapienz_result.keys():
                final_value = monkey_result[key] + "@" + sapienz_result[key]
            else:
                final_value = monkey_result[key] + "@ "
            if key in stoat_result.keys():
                final_value = final_value + "@" + stoat_result[key]
            else:
                final_value = final_value + "@ "
            final_result.update({key: final_value})

    for key in sapienz_result.keys():
        if key in final_result.keys():
            continue
        else:
            if key in monkey_result.keys():
                final_value = monkey_result[key] + "@" + sapienz_result[key]
            else:
                final_value = " @" + sapienz_result[key]
            if key in stoat_result.keys():
                final_value = final_value + "@" + stoat_result[key]
            else:
                final_value = final_value + "@ "
            final_result.update({key: final_value})

    for key in stoat_result.keys():
        if key in final_result.keys():
            continue
        else:
            if key in monkey_result.keys():
                final_value = monkey_result[key] + "@"
            else:
                final_value = " @"
            if key in sapienz_result.keys():
                final_value = final_value + sapienz_result[key] + "@" + stoat_result[key]
            else:
                final_value = final_value + " @" + stoat_result[key]
            final_result.update({key: final_value})

    # SQtesting
    for key in final_result.keys():
        if key in SQtesting_result.keys():
            final_result[key] = final_result[key] + "@" + SQtesting_result[key]
        else:
            final_result[key] = final_result[key] + "@ "

    # SQtesting2
    for key in final_result.keys():
        if key in SQtesting2_result.keys():
            final_result[key] = final_result[key] + "@" + SQtesting2_result[key]
        else:
            final_result[key] = final_result[key] + "@ "
    return final_result


final_result = getFinalResult(monkey_result, sapienz_result, stoat_result, SQtesting_result, SQtesting2_result)
print(final_result)

monkey_max_count = 0
sapienz_max_count = 0
stoat_max_count = 0
SQtesting_max_count = 0
monkey_apps = []
sapienz_apps = []
stoat_apps = []
SQtesting_apps = []

for key in final_result.keys():
    monkey = 0 if final_result[key].split('@')[0] == " " else int(final_result[key].split('@')[0])
    sapienz = 0 if final_result[key].split('@')[1] == " " else int(final_result[key].split('@')[1])
    stoat = 0 if final_result[key].split('@')[2] == " " else int(final_result[key].split('@')[2])
    SQtesting = 0 if final_result[key].split('@')[3] == " " else int(final_result[key].split('@')[3])
    tmp = max(monkey, sapienz, stoat, SQtesting)
    if tmp == monkey:
        monkey_max_count += 1
        monkey_apps.append(key)
    if tmp == sapienz:
        sapienz_max_count += 1
        sapienz_apps.append(key)
    if tmp == stoat:
        stoat_max_count += 1
        stoat_apps.append(key)
    if tmp == SQtesting:
        SQtesting_max_count += 1
        SQtesting_apps.append(key)
    print(key + ": " + final_result[key])
print(monkey_max_count, " ", sapienz_max_count, " ", stoat_max_count, " ", SQtesting_max_count)
print("\n")
print(monkey_apps)
print(sapienz_apps)
print(stoat_apps)
print(SQtesting_apps)
