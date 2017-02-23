#!/usr/bin/env python

from rpc_server import rpc_server

class vehicle_status(rpc_server):
	"""docstring for vehicle_status"""
	def __init__(self, username, passwd, hostip, queuename):
		super(vehicle_status, self).__init__(username, passwd, hostip, queuename)

	def do_something(self, response):
		print response
		return (True, "success")

factory = vehicle_status("encore", "encore", "127.0.0.1", "sensor_data")
