#!/usr/bin/python

import serial
import time
import sys


ser=serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=.1, rtscts=0)

ser.write(b'ATE1')
# time.sleep(0.1)
response = ser.read(256)
print response

ser.write(b'AT^SYSINFO')
# time.sleep(0.1)
response = ser.read(256)
print response

//获取信号强度命令
