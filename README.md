# SQDroid
SQDroid is a semantic-driven approach for Android apps based Q-learning. It employs dynamic semantic reward function to understand the business logic and test complex functionalities in apps. Meantime, we design a state clustering module, which is beneficial to compress state space in Q-table and improve the exploration efficiency of SQDroid.
# Installation
## System Requirements
+ Python: 3.6<br>
+ Android SDK: API 19 (make sure adb and aapt commands are available)<br>
+ Linux: Ubuntu 16.04<br>
+ Gradle: (for instrumented apks)<br>
+ uiautomator: pip install uiautomator2==2.16.3<br>
+ lxml: pip install lxml==4.6.3<br>

The above version of the software has been tested in our experiment. We use Pyinstalller to bundle the Q-testing project into an executable file that can be run in Linux. You don't need to install the tool or any other python dependencies; just download all the project source code is enough. The application under test can be installed in a physical phone connected to a computer, or in an Android virtual machine, where API level 19 (4.4) has been tested.<br>

# Usage
## Semantic state sequence data requirements
+ For the app in the experiment, we upload the collected semantic state data to the data folder; 
+ For the custom apps, the user should also update the collected semantic state sequence data to the project data folder.

It is worth noting that the sequence number of the data folder storing the semantic state sequence should be consistent with the apk sequence number (e.g., the folder name of the semantic state sequence corresponding to 1_x.apk is 1_x). The detailed semantic state sequence data collection steps are described in the paper Section III.C (semantic state sequence collecting).
## Subject Requirements
+ SQDroid can test both on open-source and closed-source apps. If users want to obtain code coverage information, the app should be instrumented with JaCoCo first and then built as an APK file (see JaCoCo/README for detailed usage).
+ The apk file corresponding to the app should be uploaded to the apk folder of the project.
## Settings
Before running SQDroid, please update the settings/GlobalConfiguration.py as follow:<br>
```python
    # Testing Android App settings
    APK_DIR = r"/opt/apks/SQDroid"
    SEMANTIC_PATH = r"/opt/code/SQDroid/data"
    DEVICE_ID = 'emulator-5554'
    SCREEN_WIDTH = 480
    SCREEN_HIGHT = 800
```
Other configuration information of the GlobalConfiguration.py can be selected according to user customization or default configuration.
## Running
For apps that require permissions, the user should install the apk at the beginning and grant the corresponding permissions. Then the user can start the test according to the following command.
+ cd /opt/apks/SQTesting # Entering the project workspace
+ python ./algorithm/rl/explore.py # Starting the testing
## Output
For each app, the corresponding code coverage file.<br>
+ ./apk/X_X/coverage_x.ec --We save the code coverage file every minute during the test. If you want the code coverage information, run the script "python ./bin/run_coverage_scripy.py" or directly generate specific code coverage information through the graddle project and the coverage.ec file. 
+ ./apk/X_X/logcat.txt -- The corresponding log information during the test, you can run the script "python ./bin/run_crash_scripy.py" to obtain the crash info.
