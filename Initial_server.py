#!/usr/bin/env python
import sys
import os

def main():
	#env
	path = os.path.abspath(os.curdir)
	path = os.path.join(path, 'rabbitMQ')
	os.system('export PYTHONPATH='+path)
	# initial sensor_data.py
	os.system('python ./sensor/sensor_data.py 2&1 > ./sensor/sensor_data.log')	
	pass

if __name__ == '__main__':
	main()