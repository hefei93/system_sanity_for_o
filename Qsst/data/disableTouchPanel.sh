#!/system/bin/sh
export PATH=$PATH:/data/qbusybox
filename=$(getevent -lp |grep "TOUCH" -B4|grep "/dev/input/event[0-9]" -o)
echo "touch dev filname is : "
echo $filename

#is /dev/input/$index  readable , if yes return 0 
if ls -l $filename | grep "crw" > /dev/null 2>&1  
then
    chmod 000 $filename
    #chmod 660 /dev/input/$index
    # wait for enable...
    sleep 2
    # restart android
    stop
    sleep 5
    start
    sleep 40  
    #go back home activity
    input keyevent 3
    #intent.putExtra(QsstService.QSST_SERVICE_FLAG, QsstService.QSST_SERVICE_FLAG_START);
    #public static final String QSST_SERVICE_FLAG = "com.android.qrdtest.QsstService.flag";    
    #public static final int QSST_SERVICE_FLAG_START = 987;    
    #$1 is test_env*** directory
    am startservice -n com.android.qrdtest/.QsstService --ei com.android.qrdtest.QsstService.flag 987 --es path $1
    sleep 2    
else
    echo "already changed. do nothing"
fi
echo "end disable DND"
exit 0