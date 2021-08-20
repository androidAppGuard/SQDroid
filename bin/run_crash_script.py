import os

SQ_testing2_dir = r"F:\Paper\SQTesting2"
Monkey_dir = r"/opt/apks/monkey_app"
Sapienz_dir = r"/opt/apks/sapienz_app"
stoat_dir = r"/opt/apks/stoat_app"
SQ_testing_dir = r"/opt/apks/SQTesting"

DIR = SQ_testing2_dir

package_dict = {
    '10': 'org.totschnig.myexpenses.debug',
    '11': 'com.ichi2.anki',
    '12': 'com.eleybourn.bookcatalogue',
    '13': 'com.cody.ammeter',
    '14': 'com.amaze.filemanager.debug',
    '15': 'com.forrestguice.suntimeswidget',
    '16': 'org.runnerup.debug',
    '17': 'org.liberty.android.fantastischmemodev',
    '18': 'it.fossoft.timberfoss.dev',
    '19': 'ch.blinkenlights.android.vanilla',
    '1': 'com.mattallen.loaned',
    '21': 'com.asksven.betterbatterystats_xdaedition',
    '22': 'de.k3b.android.androFotoFinder',
    '24': 'com.android.keepass',
    '27': 'org.openbmap',
    '28': 'io.github.hidroh.materialistic',
    '29': 'org.tomdroid',
    '2': 'budget.notriddle.com.budget',
    '30': 'com.android.a30_importcontacts',
    '32': 'com.android.sanity',
    '35': 'be.ppareit.swiftp_free',
    '36': 'org.asdtm.goodweather',
    '37': 'com.android.manpages',
    '38': 'protect.budgetwatch',
    '39': 'com.android.a39_passwordmaker',
    '3': 'batterydog.andbatdog.sf.net.batterydog',
    '40': 'org.billthefarmer.notes',
    '41': 'com.android.a41_alarm',
    '43': 'com.android.a43_manille',
    '44': 'trikita.talalarmo',
    '45': 'com.android.a45_smsscheduler',
    '46': 'com.bytestemplar.tonedef',
    '47': 'com.android.a47_alogcat',
    '48': 'com.android.a48_multismssender',
    '49': 'fr.ac_versailles.dane.xiaexpress',
    '4': 'whohasmystuff.freewarepoint.de.whohasmystuff',
    '50': 'de.meonwax.soundboard',
    '51': 'com.github.yeriomin.dumbphoneassistant',
    '52': 'ru.neverdark.silentnight',
    '53': 'com.android.a53_lockpatterngenerator',
    '54': 'net.thebrennt.anycut',
    '55': 'com.android.a55_munchlife',
    '56': 'com.android.a56_bequick',
    '57': 'org.weilbach.splitbills.mock',
    '5': 'mynotes.aa.com.a5_mynotes',
    '6': 'recordtimedroid.oml.com.a6_recordtimedroid',
    '7': 'snotepad.aario.info.snotepad',
    '8': 'moneybalance.android.ivl.a8_moneybalance',
    '9': 'org.billthefarmer.siggen'
}


def get_SQtesting_Monkey_StoatCrashes(DIR):
    for dir in os.listdir(DIR):
        if len(dir.split(".")) == 1:
            # process
            print(dir)
            file_path = os.path.join(os.path.join(DIR, dir), 'logcat.txt')
            crash_file = os.path.join(os.path.join(DIR, dir), 'crash.txt')
            crash_ret_file = os.path.join(os.path.join(DIR, dir), 'crash_pid.txt')
            crash_final_file = os.path.join(os.path.join(DIR, dir), 'crash_ret.txt')
            package_name = package_dict[dir.split("_")[0]]

            # logcat
            crash_info = []
            with open(file_path, "r", encoding='UTF-8') as log_file:
                for line in log_file.readlines():
                    if package_name in line.strip():
                        crash_info.append(line)
            with open(crash_file, 'w', encoding='utf-8') as ret_file:
                for line in crash_info:
                    ret_file.write(line)
                    ret_file.write("\n")
            pid_set = {}
            with open(crash_file, "r", encoding='UTF-8') as ret_file:
                for line in ret_file.readlines():
                    if len(line.strip()) > 52:
                        # if 'Exception' in line.strip():
                        if line.strip()[33:51] not in pid_set.keys():
                            pid_set.update({line.strip()[33:51]: [line.strip()]})
                        else:
                            pid_set[line.strip()[33:51]].append(line.strip())
            with open(crash_ret_file, 'w', encoding='utf-8') as ret_file:
                for key in pid_set.keys():
                    for line in pid_set[key]:
                        ret_file.write(line)
                    ret_file.write("\n")

            # filter no Error
            array_info = []
            with open(crash_ret_file, "r", encoding='UTF-8') as log_file:
                for line in log_file.readlines():
                    # if re.match(r"^\d{2}-\d{2} (\d{2}:){2}\d{2}.\d{3}([ ]{1,} \d{1,}){2}[ ]{1,}E",line.strip()):
                    if len(line.strip()) > 32 and line.strip()[31] == "E":
                        array_info.append(line)
            with open(crash_final_file, 'w', encoding='utf-8') as ret_file:
                for line in array_info:
                    ret_file.write(line)
                    ret_file.write("\n")


def get_sapienz(DIR):
    for dir in os.listdir(DIR):
        if len(dir.split(".")) == 1:
            # process
            print(dir)
            file_path = os.path.join(os.path.join(DIR, dir), 'log.txt')
            crash_file = os.path.join(os.path.join(DIR, dir), 'crash.txt')
            crash_ret_file = os.path.join(os.path.join(DIR, dir), 'crash_pid.txt')
            crash_final_file = os.path.join(os.path.join(DIR, dir), 'crash_ret.txt')
            package_name = package_dict[dir.split("_")[0]]

            # logcat
            crash_info = []
            with open(file_path, "r", encoding='UTF-8') as log_file:
                for line in log_file.readlines():
                    if package_name in line.strip():
                        crash_info.append(line)
            with open(crash_file, 'w', encoding='utf-8') as ret_file:
                for line in crash_info:
                    ret_file.write(line)
                    ret_file.write("\n")
            pid_set = {}
            with open(crash_file, "r", encoding='UTF-8') as ret_file:
                for line in ret_file.readlines():
                    if len(line.strip()) > 52:
                        # if 'Exception' in line.strip():
                        if line.strip()[2:10] not in pid_set.keys():
                            pid_set.update({line.strip()[2:10]: [line.strip()]})
                        else:
                            pid_set[line.strip()[2:10]].append(line.strip())
            with open(crash_ret_file, 'w', encoding='utf-8') as ret_file:
                for key in pid_set.keys():
                    for line in pid_set[key]:
                        ret_file.write(line)
                    ret_file.write("\n")

            array_info = []
            with open(crash_ret_file, "r", encoding='UTF-8') as log_file:
                for line in log_file.readlines():
                    # if re.match(r"^\d{2}-\d{2} (\d{2}:){2}\d{2}.\d{3}([ ]{1,} \d{1,}){2}[ ]{1,}E",line.strip()):
                    if len(line.strip()) > 1 and line.strip()[0] == "E":
                        array_info.append(line)
            with open(crash_final_file, 'w', encoding='utf-8') as ret_file:
                for line in array_info:
                    ret_file.write(line)
                    ret_file.write("\n")


get_SQtesting_Monkey_StoatCrashes(DIR)
# get_sapienz(DIR)

# for dir in os.listdir(DIR):
#     ret_dict = {}
#     if len(dir.split(".")) == 1:
#         crash_final_file = os.path.join(os.path.join(DIR, dir), 'crash_ret.txt')
#         count = 0
#         with open(crash_final_file, 'r', encoding='utf-8') as ret_file:
#             for line in ret_file.readlines():
#                 if len(line) > 5:
#                     count += 1
#         print(dir.split("_")[0],":",count)





SQ_testing2 = {
    '10': '1',
    '11': '1',
    '12': '5',
    '14': '3',
    '15': '1',
    '16': '1',
    '17': '1',
    '18': '2',
    '19': '0',
    '1': '1',
    '21': '0',
    '22': '0',
    '24': '0',
    '27': '3',
    '28': '5',
    '29': '2',
    '2': '0',
    '30': '0',
    '32': '0',
    '35': '0',
    '36': '1',
    '37': '1',
    '38': '1',
    '39': '0',
    '3': '0',
    '40': '0',
    '41': '0',
    '43': '0',
    '44': '1',
    '45': '0',
    '46': '0',
    '47': '0',
    '48': '0',
    '49': '0',
    '4': '0',
    '50': '1',
    '51': '0',
    '52': '0',
    '53': '0',
    '54': '0',
    '55': '0',
    '56': '0',
    '57': '0',
    '5': '0',
    '6': '0',
    '7': '0',
    '8': '0',
    '9': '0'
}

# ret_dict = {}
#
#
# for task_dir in [Monkey_dir, Sapienz_dir, stoat_dir, SQ_testing_dir]:
#     for dir in os.listdir(task_dir):
#         if len(dir.split(".")) == 1:
#             crash_final_file = os.path.join(os.path.join(task_dir, dir), 'crash_ret.txt')
#             count = 0
#             with open(crash_final_file, 'r', encoding='utf-8') as ret_file:
#                 for line in ret_file.readlines():
#                     if len(line) > 5:
#                         count += 1
#             if dir.split("_")[0] in ret_dict.keys():
#                 ret_dict[dir.split("_")[0]].append(str(count))
#             else:
#                 ret_dict.update({dir.split("_")[0]: [str(count)]})
#
# for key in SQ_testing2.keys():
#     if key in ret_dict.keys():
#         ret_dict[key].append(SQ_testing2[key])
#     else:
#         ret_dict.update({key: [SQ_testing2[key]]})
#
# for key in ret_dict:
#     print(key, ":", ret_dict[key])


# ret_dict= {}
# for dir in os.listdir(SQ_testing2_dir):
#     if len(dir.split(".")) == 1:
#         crash_final_file = os.path.join(os.path.join(SQ_testing2_dir, dir), 'crash_ret.txt')
#         count = 0
#         with open(crash_final_file, 'r', encoding='utf-8') as ret_file:
#             for line in ret_file.readlines():
#                 if len(line) > 5:
#                     count += 1
#         ret_dict.update({dir.split("_")[0]: [str(count)]})
# for key in ret_dict:
#     print(key, ":", ret_dict[key])

