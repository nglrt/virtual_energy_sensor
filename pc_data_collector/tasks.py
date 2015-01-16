import platform, subprocess


class DeviceInfoTask(object):
	def run(self):
		processor = self.get_processor_info()
		system = "system		: " + platform.platform()
		node = "name		: " + platform.node()

		return "\n".join([processor, system, node])

	def __call__(self):
		return self.run()

	def get_processor_info(self):
	    if platform.system() == "Windows":
	        return platform.processor()
	    elif platform.system() == "Darwin":
	        return subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()
	    elif platform.system() == "Linux":
	        command = "cat /proc/cpuinfo"
	        return subprocess.check_output(command, shell=True).strip()
	    return ""

