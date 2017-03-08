#!/usr/bin/env python
import sys
import os

def main():
	#env
	path = os.path.abspath(os.curdir)
	path = os.path.join(path, 'rabbitMQ')
	print path
	os.system('export PYTHONPATH='+path)

	# initial sensor_data.py
	os.system('python ./sensor/vehicle_status.py >> ./sensor/vehicle_status.log 2>&1 &')	

	# initial receivefile.py
	os.system('python ./rabbitMQ/receivefile.py >> ./rabbitMQ/receivefile.log 2>&1 &')

	# initial net_control.py
	os.system('python ./network/net_control.py >> ./network/net_control.log 2>&1 &')
	pass

if __name__ == '__main__':
	main()
