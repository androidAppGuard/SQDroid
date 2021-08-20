import os
import subprocess
import time


def get_package_and_activity(apk_apth):
    package_cmd = 'aapt dump badging ' + apk_apth + ' | grep package:'
    console_pipe = subprocess.Popen(package_cmd, shell=True, stdout=subprocess.PIPE)
    out, err = console_pipe.communicate()
    package_name = out.decode().strip().split(" ")[1].split("'")[1]

    activity_cmd = 'aapt dump badging ' + apk_apth + ' | grep launchable-activity:'
    console_pipe = subprocess.Popen(activity_cmd, shell=True, stdout=subprocess.PIPE)
    out, err = console_pipe.communicate()
    activity_name = out.decode().strip().split(" ")[1].split("'")[1]
    return package_name, activity_name


conf_context = [
    "[Path]",
    "APK_NAME = ",
    r"Benchmark = /opt/apks/Qtesting/",
    "[Setting]",
    "DEVICE_ID = emulator-5554",
    "TIME_LIMIT = 10",
    "TEST_INDEX = 2"
]

if __name__ == '__main__':
    apk_dir = r'/opt/apks/Qtesting'
    apk_list = os.listdir(apk_dir)
    apk_list.sort()
    for filename in apk_list:
        if len(filename.split(".")) == 2 and filename.split(".")[1] == "apk":
            apk_apth = apk_dir + '/' + filename
            package_name, activity_name = get_package_and_activity(apk_apth)

            outdir = apk_dir + '/' + filename.split(".")[0] + "_Qtestingout"
            if not os.path.exists(outdir):
                os.makedirs(outdir)
                print("creating ok")

            os.system("adb reboot")
            time.sleep(10)
            # clean coverage.ec
            os.system("adb shell rm /mnt/sdcard/coverage.ec")
            # uninstall apk
            os.system('adb uninstall ' + package_name)
            # install apk
            os.system('adb install ' + apk_apth)
            print("prepare work finish!")
            log_file = open(outdir + '/log.txt', 'w+')
            crash_file = open(outdir + '/crash.txt', 'w+')
            os.system('adb -s emulator-5554 logcat -c')
            save_pipe = subprocess.Popen(args='adb -s emulator-5554 logcat -v threadtime', stdin=None, stdout=log_file,
                                         stderr=crash_file, shell=True)
            os.system("adb shell am start -n " + package_name + r"/" + activity_name)

            with open("/opt/code/Q-testing/CONF.txt", "w", encoding="utf-8") as f:
                for i in range(len(conf_context)):
                    if i == 1:
                        f.write(conf_context[i] + filename)
                    else:
                        f.write(conf_context[i])
                    f.write("\n")

            # start the Qtesting task
            Qtesting_pipe = subprocess.Popen(
                args='exec ./q-testing-wgx-publish-pyinstaller/main -r CONF.txt',
                # stdin=subprocess.PIPE,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                shell=True,
                cwd=r'/opt/code/Q-testing'
            )

            # real time get coverage.ec file
            time_count = 0
            while time_count < 3600:
                time.sleep(60)
                # log = stoat_pipe.stdout.read()
                # stoat_pipe.stdout.close()
                # print(log.decode())
                os.system('adb pull /mnt/sdcard/coverage.ec ' + outdir + '/' + str(time_count) + '_coverage.ec')
                time_count = time_count + 60
                print("time explore: ", time_count)
            os.system('adb pull /mnt/sdcard/coverage.ec ' + outdir + '/' + str(time_count) + '_coverage.ec')
            Qtesting_pipe.terminate()
            Qtesting_pipe.kill()
            save_pipe.terminate()
            save_pipe.kill()
            crash_file.close()
            log_file.close()
            # uninstall apk
            os.system('adb uninstall ' + package_name)
