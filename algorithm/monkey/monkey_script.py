import os
import time
import sys

package = sys.argv[1]
print(package)
count = 1
while True:
    os.system("adb shell monkey -p " + package + " --throttle 200 -v 500")
    time.sleep(1)
    print(count)
