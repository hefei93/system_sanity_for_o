#!/system/bin/sh
export PATH=$PATH:/data/qbusybox
filename=$(getevent -lp |grep "TOUCH" -B4|grep "/dev/input/event[0-9]" -o)
echo "touch dev filname is : "
echo $filename

#is /dev/input/$index not readable
if ls -l $filename | grep "c\-\-" > /dev/null 2>&1  
then
    reboot
else
    echo "already changed. do nothing"
fi
echo "done"
exit 0