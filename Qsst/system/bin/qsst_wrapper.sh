#!/system/bin/sh

CLASSPATH=/system/framework/qsst_super_daemon.jar
export CLASSPATH
exec app_process32 /system/bin com.android.qsst.QsstSuperDaemonService \&