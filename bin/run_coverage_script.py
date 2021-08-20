import subprocess
from lxml import html
import os
import shutil

# monkey F:\Paper\Monkey
# sapienz F:\Paper\Sapienz
# stoat D:\paper\Result\stoat
# SQ-testing F:\Paper\SQTesting

src_dir = r'D:\paper\Result\stoat'
result_path = src_dir + r"/" + 'result1.txt'

cmd_dict = {
    # "1": [r"D:\paper\apks\jacoco\1_loaned\app\build\outputs", "gradlew jacocoTestReport"],
    # "2": [r"D:\paper\apks\jacoco\2_com.notriddle.budget\app\build\outputs", "gradlew jacocoTestReport"],
    # "3": [r"D:\paper\apks\jacoco\3_batterydog\app\build\outputs", "gradlew jacocoTestReport"],
    # "4": [r"D:\paper\apks\jacoco\4_whohasmystuff\app\build\outputs", "gradlew jacocoTestReport"],
	# "5": [r"D:\paper\apks\jacoco\5_mynotes\app\build\outputs", "gradlew jacocoTestReport"],
    # "6": [r"D:\paper\apks\jacoco\6_recordtimedroid\app\build\outputs", "gradlew jacocoTestReport"],
	# "7": [r"D:\paper\apks\jacoco\7_snotepad\app\build\outputs", "gradlew jacocoTestReport"],
	# "8": [r"D:\paper\apks\jacoco\8_moneybalance\app\build\outputs", "gradlew jacocoTestReport"],
	# "9": [r"D:\paper\apks\jacoco\9_siggen\app\build\outputs", "gradlew jacocoTestReport"],
    # "10": [r"D:\paper\apks\jacoco\10_myexpenses\myExpenses\build\outputs", "gradlew jacocoTestReport"],
    # "11": [r"D:\paper\apks\jacoco\11_anki\AnkiDroid\build\outputs", "gradlew jacocoTestReport"],
    # "12": [r"D:\paper\apks\jacoco\12_bookcatalogue\build\outputs", "gradlew jacocoTestReport"],
    "13": [r"D:\paper\apks\jacoco\13_ammeter\app\build\outputs", "gradlew jacocoTestReport"],
    # "14": [r"D:\paper\apks\jacoco\14_amazeFileManage\app\build\outputs", "gradlew jacocoTestReport1"],
    # "15": [r"D:\paper\apks\jacoco\15_Suntimes\app\build\outputs", "gradlew jacocoTestReport"],

	# "16": [r"D:\paper\apks\jacoco\16_runnerup\app\build\outputs", "gradlew jacocoTestReport"],
    # "17": [r"D:\paper\apks\jacoco\17_AnyMemo\app\build\outputs", "gradlew jacocoTestReport"],
    # "18": [r"D:\paper\apks\jacoco\18_Timber\app\build\outputs", "gradlew jacocoTestReport"],
    # "19": [r"D:\paper\apks\jacoco\19_vanilla\app\build\outputs", "gradlew jacocoTestReport"],
    # "21": [r"D:\paper\apks\jacoco\21_betterBatteryStats\app\build\outputs", "gradlew jacocoTestReport"],
    # "22": [r"D:\paper\apks\jacoco\22_APhotoManager\app\build\outputs", "gradlew jacocoTestReport"],
    # "24": [r"D:\paper\apks\jacoco\24_keepassdroid\app\build\outputs", "gradlew jacocoTestReport"],
    # "27": [r"D:\paper\apks\jacoco\27_radioBeacon\app\build\outputs", "gradlew jacocoTestReport"],
    # "28": [r"D:\paper\apks\jacoco\28_materialistic\app\build\outputs", "gradlew jacocoTestReport"],
    # "29": [r"D:\paper\apks\jacoco\29_tomdroid\build\outputs", "gradlew jacocoTestReport"],
    # "30": [r"D:\paper\apks\jacoco\30_importcontacts\app\build\outputs", "gradlew jacocoTestReport"],
    # "32": [r"D:\paper\apks\jacoco\32_sanity\app\build\outputs", "gradlew jacocoTestReport"],
    # "35": [r"D:\paper\apks\jacoco\35_swiftp\app\build\outputs", "gradlew jacocoTestReport"],
    # "36": [r"D:\paper\apks\jacoco\36_goodweather\app\build\outputs", "gradlew jacocoTestReport"],
    # "37": [r"D:\paper\apks\jacoco\37_manpages\app\build\outputs", "gradlew jacocoTestReport"],
    # "38": [r"D:\paper\apks\jacoco\38_budgetwatch\app\build\outputs", "gradlew jacocoTestReport"],
    # "39": [r"D:\paper\apks\jacoco\39_passwordmaker\app\build\outputs", "gradlew jacocoTestReport"],
    # "40": [r"D:\paper\apks\jacoco\40_notes\build\outputs", "gradlew jacocoTestReport"],
    # "41": [r"D:\paper\apks\jacoco\41_alarm\app\build\outputs", "gradlew jacocoTestReport"],
    # "43": [r"D:\paper\apks\jacoco\43_manille\app\build\outputs", "gradlew jacocoTestReport"],
    # "44": [r"D:\paper\apks\jacoco\44_talarmo\build\outputs", "gradlew jacocoTestReport"],
    # "45": [r"D:\paper\apks\jacoco\45_smsscheduler\app\build\outputs", "gradlew jacocoTestReport"],
    # "46": [r"D:\paper\apks\jacoco\46_tonedef\MainApp\build\outputs", "gradlew jacocoTestReport"],
    # "47": [r"D:\paper\apks\jacoco\47_alogcat\app\build\outputs", "gradlew jacocoTestReport"],
    # "48": [r"D:\paper\apks\jacoco\48_multismssender\app\build\outputs", "gradlew jacocoTestReport"],
    # "49": [r"D:\paper\apks\jacoco\49_xiaexpress\app\build\outputs", "gradlew jacocoTestReport"],
    # "50": [r"D:\paper\apks\jacoco\50_soundboard\app\build\outputs", "gradlew jacocoTestReport"],
    # "51": [r"D:\paper\apks\jacoco\51_dumpphoneAssistant\app\build\outputs", "gradlew jacocoTestReport"],
    # "52": [r"D:\paper\apks\jacoco\52_autonight\app\build\outputs", "gradlew jacocoTestReport"],
    # "53": [r"D:\paper\apks\jacoco\53_lockpatterngenerator\app\build\outputs", "gradlew jacocoTestReport"],
    # "54": [r"D:\paper\apks\jacoco\54_anycut\app\build\outputs", "gradlew jacocoTestReport"],
    # "55": [r"D:\paper\apks\jacoco\55_munchlife\app\build\outputs", "gradlew jacocoTestReport"],
    # "56": [r"D:\paper\apks\jacoco\56_bequick\app\build\outputs", "gradlew jacocoTestReport"],
    # "57": [r"D:\paper\apks\jacoco\57_splitbills\app\build\outputs", "gradlew jacocoTestReport"]
}
src_path = {}
for elem in os.listdir(src_dir):
    src_path.update({elem.split('_')[0]: src_dir + r"/" + elem})
eloc_info = {}
for i in range(57):
    if str(i) in cmd_dict.keys() and str(i) in src_path.keys():
        with open(result_path, 'a+') as result_f:
            result_f.write(src_path[str(i)] + "\n")
        if i in [12, 29, 40, 44]:
            for time in range(1, 61):
                src = src_path[str(i)] + r"/" + str(time * 60) + "_coverage.ec"
                dst = cmd_dict[str(i)][0] + r"/" + "coverage.ec"
                shutil.copy(src, dst)
                subprocess.check_call(cmd_dict[str(i)][1], shell=True,
                                      cwd=os.path.abspath(os.path.join(cmd_dict[str(i)][0], "../..")))
                html_path = os.path.abspath(
                    os.path.join(cmd_dict[str(i)][0], "..")) + r"/reports/jacoco/" + cmd_dict[str(i)][1].split(" ")[
                                1] + "/html/index.html"
                html_res = html.parse(html_path)
                coverage_info = html_res.xpath('//*[@id="coveragetable"]/tfoot/tr/td')
                with open(result_path, 'a+') as result_f:
                    result_f.write(coverage_info[1].text)
                    result_f.write(",")
                    result_f.write(coverage_info[2].text.split('%')[0])
                    result_f.write("\n")
                # print(coverage_info[1].text, coverage_info[2].text.split('%')[0])
        else:
            for time in range(1, 61):
                src = src_path[str(i)] + r"/" + str(time * 60) + "_coverage.ec"
                dst = cmd_dict[str(i)][0] + r"/" + "coverage.ec"
                if not os.path.exists(src):
                    continue
                shutil.copy(src, dst)
                subprocess.check_call(cmd_dict[str(i)][1], shell=True,
                                      cwd=os.path.abspath(os.path.join(cmd_dict[str(i)][0], "../../..")))
                html_path = os.path.abspath(
                    os.path.join(cmd_dict[str(i)][0], "..")) + r"/reports/jacoco/" + cmd_dict[str(i)][1].split(" ")[
                                1] + "/html/index.html"
                html_res = html.parse(html_path)
                coverage_info = html_res.xpath('//*[@id="coveragetable"]/tfoot/tr/td')
                with open(result_path, 'a+') as result_f:
                    result_f.write(coverage_info[1].text)
                    result_f.write(",")
                    result_f.write(coverage_info[2].text.split('%')[0])
                    result_f.write("\n")
                # print(coverage_info[1].text, coverage_info[2].text.split('%')[0])

        print(os.path.abspath(os.path.join(cmd_dict[str(i)][0], "../../..")), "finish!")

        # ELOC info
        # html_path = os.path.abspath(
        #     os.path.join(cmd_dict[str(i)][0], "..")) + r"/reports/jacoco/" + cmd_dict[str(i)][1].split(" ")[
        #                 1] + "/html/index.html"
        # html_res = html.parse(html_path)
        # coverage_info = html_res.xpath('//*[@id="coveragetable"]/tfoot/tr/td')
        # eloc_info.update({cmd_dict[str(i)][0].split('\\')[4]:coverage_info[8].text.replace(',',"")})

# print(sorted(eloc_info.items(), key = lambda item:int(item[1])))
# subprocess.check_call('gradlew jacocoTestReport', shell=True, cwd=r'D:\paper\apks\jacoco\1_loaned')
# print("ok")
