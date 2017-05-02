# -*- coding: utf-8 -*-
import sys
args = sys.argv
file = args[1]

f=open(file,'ab')
f.write(b'\x0aruncon u:r:su:s0 /system/bin/sh /system/bin/qsst_wrapper.sh &\x0a')
f.close()