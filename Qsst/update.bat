@echo off
if not exist C:\Qsst md C:\Qsst
copy tool\qxdm C:\Qsst
copy tool\Asia\QsstUtility.pm "C:\Program Files\Qualcomm\Asia\perlenv"

FOR /F "delims=" %%I IN ("python.exe") DO (if exist %%~$PATH:I (echo Python is detected, Pls continue...) else (echo cann't detect Python inside system, Pls CTRL + C to exiting and ensure the python is installed and setinto System PATH))

echo adb wait-for-device root
adb wait-for-device root

echo adb wait-for-device remount
adb wait-for-device remount


adb push  system /
adb push  data   /

del /f /q init.qcom.testscripts.sh
adb pull /system/etc/init.qcom.testscripts.sh
python file_convert.py init.qcom.testscripts.sh
adb push init.qcom.testscripts.sh /system/etc
adb shell chmod 777 /system/etc/init.qcom.testscripts.sh
del /f /q init.qcom.testscripts.sh

adb shell chmod 4777 /system/bin/python
adb shell chmod 4777 /system/bin/uiautomator
adb shell chmod 777 /data/disableTouchPanel.sh
adb shell chmod 777 /data/EnableTouchPanel.sh
adb shell chmod 777 /system/bin/qsst_wrapper.sh
adb wait-for-device
adb shell chmod -R  777 /data/python_env/
adb wait-for-device
adb shell chmod -R  777 /data/test_env/
adb wait-for-device
adb shell rm /system/framework/uiautomator.odex

echo cd /data/python_env/com.googlecode.pythonforandroid/files/python/lib/ > temp.txt
echo sh push_python_libs.sh >> temp.txt
echo exit >> temp.txt
adb shell < temp.txt
del /f /q temp.txt

adb reboot

exit
