#!/usr/bin/python3


def build_config(config_file, **kwargs):

	"""

	This will build configuration files by replacing placeholders in config file.
	First argument is the config file name.
	Second and next arguments after, are config placeholders you want to replace in config file.
	Eg: build_config("mikrotik_config.rsc", VHOSTNAME="Mikrotik-test", VMKTWANIP="192.168.0.11/24", VMKTWANGW="192.168.0.1")
	
	"""
	
	import datetime
	timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")

	with open(config_file, 'r') as rf:
		with open(timestamp + "_" + config_file, 'w') as wf:
			read_template = rf.read()
			for arg in kwargs:
				read_template = read_template.replace(arg, kwargs[arg])
			wf.write(read_template)

	return read_template


