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

if __name__ == '__main__':
    apk_dir = r'/opt/apks/open_source/jacoco'
    for filename in os.listdir(apk_dir):
        if len(filename.split(".")) == 2 and filename.split(".")[1] == "apk":
            apk_apth = apk_dir + '/' + filename
            package_name, activity_name = get_package_and_activity(apk_apth)

            outdir = apk_dir + '/' + filename.split(".")[0] + "_stoatout"
            if not os.path.exists(outdir):
                os.makedirs(outdir)
                print("creating ok")

            # clean coverage.ec
            os.system("adb shell rm /mnt/sdcard/coverage.ec")
            # uninstall apk
            os.system('adb uninstall '+ package_name)
            # install apk
            os.system('adb install ' + apk_apth)
            print("prepare work finish!")

            # start the stoat task
            stoat_pipe = subprocess.Popen(args='exec ruby /opt/code/Stoat/Stoat/bin/run_stoat_testing.rb --app_dir '+ apk_apth +' --avd_name stoat_avd1 --avd_port 5554 --stoat_port 2000',
                             #stdin=subprocess.PIPE,
                             #stdout=subprocess.PIPE,
                             #stderr=subprocess.PIPE,
                             shell=True
                             )

            # real time get coverage.ec file
            time_count = 0
            while time_count < 3600:
                time.sleep(60)
                #log = stoat_pipe.stdout.read()
                #stoat_pipe.stdout.close()
                #print(log.decode())
                os.system('adb pull /mnt/sdcard/coverage.ec ' + outdir + '/' + str(time_count) + '_coverage.ec')
                time_count = time_count + 60
                print("time explore: ",time_count)
            os.system('adb pull /mnt/sdcard/coverage.ec ' + outdir + '/' + str(time_count) + '_coverage.ec')
            stoat_pipe.terminate()
            stoat_pipe.kill()
            # uninstall apk
            os.system('adb uninstall '+ package_name)
        #break
        # push coverage.ec file and rename x_coverage.ec

    # console_pipe = subprocess.Popen(args='python D:/paper/testing.py',
    #                  stdin=None,
    #                  stdout=None,
    #                  stderr=None,
    #                  shell=False,
    #                  )
    #
    # import time
    # time.sleep(10)
    # console_pipe.terminate()
    # console_pipe.kill()

