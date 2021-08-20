import uiautomator2 as u2
import os

driver = u2.connect()
driver.implicitly_wait(10)

apk_name = r"57_splitbills-debug"
semantic_data_dir = r"D:\paper\STesting\data"

data_path = semantic_data_dir + r"/" + apk_name
if not os.path.exists(data_path):
    os.mkdir(data_path)

sequenceId = 1
stateId = 1
while True:
    if not os.path.exists(data_path + r"/" + str(sequenceId)):
        os.mkdir(data_path + r"/" + str(sequenceId))
    with open(data_path + r"/" + str(sequenceId) + r"/" + str(stateId) + r".txt", "w", encoding='utf-8') as file:
        ui_hierarchy = driver.dump_hierarchy()
        file.write(ui_hierarchy)
    cmd = input("cmd 1: Next sequence 2: Next state 3: Save coverage.ec\n")
    if cmd == "1":
        sequenceId += 1
        stateId = 1
    elif cmd == "2":
        stateId += 1
    else:
        os.system("adb pull /mnt/sdcard/coverage.ec " + data_path + r"/coverage.ec")
        os.system("adb shell rm /mnt/sdcard/coverage.ec")
        break

