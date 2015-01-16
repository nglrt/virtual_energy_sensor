
import sys
import subprocess
import time

class WinSystem(object):
    def set_backlight(self, val):
        pass

class LinuxSystem(object):
    def set_backlight(self, val):
        subprocess.check_output(["xbacklight", "-set", str(val)])       


def get_system():
    if sys.platform.startswith("linux"):
        source = LinuxSystem()
        
    if sys.platform.startswith("win32"):
        source = WinSystem()
        
    return source
    

def run_benchmark():
    sys = get_system()
    for i in range(0, 100, 10):
        print("Backlight to {0}%".format(i))
        sys.set_backlight(i)
        time.sleep(10)
    

