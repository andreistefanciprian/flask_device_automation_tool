#!/usr/bin/python3


def build_config(config_file_path, **kwargs):

	"""

	This will build configuration files by replacing placeholders in config file.
	First argument is the config file path name.
	Second and next arguments after, are config placeholders (key=value pairs) you want to replace in config file.
	Eg: build_config("mikrotik_config.rsc", VHOSTNAME="Mikrotik-test", VMKTWANIP="192.168.0.11/24", VMKTWANGW="192.168.0.1")

	"""

	import datetime
	import os

	timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
	basedir = os.path.dirname(config_file_path)
	filename = os.path.basename(config_file_path)
	new_filename = os.path.join(basedir, timestamp + "_" + filename)

	if os.path.isfile(config_file_path):
		with open(config_file_path, 'r') as rf:
			with open(new_filename, 'w') as wf:
				read_config = rf.read()
				for arg in kwargs:
					read_config = read_config.replace(arg, kwargs[arg])
				wf.write(read_config)
		return read_config
	else:
		return f"Configuration template for this device, {config_file_path} doesn't exist!"



