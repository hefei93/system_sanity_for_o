#!/system/bin/sh

#move all files under /lib/python2.6/lib-dynload/ to /lib/
mv /data/python_env/com.googlecode.pythonforandroid/files/python/lib/python2.6/lib-dynload/* .
rm -rf /data/python_env/com.googlecode.pythonforandroid/files/python/lib/python2.6

#list all .so files under /system/lib/ and /vendor/lib/ to system.libs and sort
ls /system/lib/ | grep '\.so$' > system.libs
ls /vendor/lib/ | grep '\.so$' >> system.libs
sort -u system.libs

#list all .so files under /lib/ to python.libs and sort
ls | grep '\.so$' > python.libs
sort -u python.libs

#list the .so files that not in system.libs, but only in python.libs to push.libs
sort python.libs  system.libs  system.libs | uniq -u > push.libs

file_name=/data/python_env/com.googlecode.pythonforandroid/files/python/lib/push.libs

#move .so files that only under python/lib/, not in /system/lib/ and /vendor/lib/ to /vendor/lib/
while read line
do
	echo $line
    mv $line /vendor/lib/
done <$file_name

rm -rf /data/python_env/com.googlecode.pythonforandroid/files/python/lib/