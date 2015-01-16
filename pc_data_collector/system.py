import psutil as ps
from parameter import Parameter
import sys
import ctypes
import glob
import subprocess

try:
    from ctypes import wintypes
except:
    pass

try:
    import wmi
except:
    pass

class Differentiator(object):
    def __init__(self):
        self.last_x = 0.0
        
    def __call__(self, x):
        return_val =  x - self.last_x
        self.last_x = x
        
        return return_val

def get_system():
    if sys.platform.startswith("linux"):
        source = LinuxSystem()
        
    if sys.platform.startswith("win32"):
        source = WinSystem()
        
    return source

class LinuxSystem:
    def __init__(self):
    
        self.last_capacity = self.getCurrentBatteryLevel()
        self.filter_wnd = 10*[0]
        
        
        self.battery_max_capacity = int(open("/sys/class/power_supply/BAT0/energy_full").read())
        self.diff={}

        self.getParameters()
    
    def calculate_diff(self, stream_name, value, allowNegativeValues=False):
        if not stream_name in self.diff:
            self.diff[stream_name] = Differentiator()

        res_ = self.diff[stream_name](value)

        if not allowNegativeValues:
            return max(0, res_)
        return res_

    def getCurrentBatteryLevel(self):
        return int(open("/sys/class/power_supply/BAT0/energy_now").read())

    def getBatteryPercent(self):
        return "{0:.2f}".format(1.0*self.getCurrentBatteryLevel()/self.battery_max_capacity)

    def getCpuSpeed(self):
        fd = open("/proc/cpuinfo", 'r')
        lines = fd.readlines()

        speed_lines = [s for s in lines if s.startswith("cpu MHz")]
        speed_info = [float(s.split(":")[-1].strip()) for s in speed_lines]

        return sum(speed_info)/len(speed_info)

    def getDisplayBacklight(self):
        backlight = subprocess.check_output(["xbacklight"])
        return float(backlight)

    def getBatteryLevel(self):
        
        capacity = self.getCurrentBatteryLevel()
        delta_cap = (capacity - self.last_capacity) 
        self.last_capacity = capacity


        self.filter_wnd.insert(0,delta_cap)
        self.filter_wnd.pop()

        muAh = (1.0 * sum(self.filter_wnd) / len(self.filter_wnd))
        return "{0:.2f}".format(muAh)

    def getCpuStates(self):
        files = glob.glob("/sys/devices/system/cpu/cpu*/cpuidle/state*/time")

        times = {}

        for fn in files:
            state=fn.split("/")[-2]

            curr_time = 0.0
            if state in times:
                curr_time += times[state]

            curr_time += float(open(fn, 'r').read())
            times[state] = curr_time

        return sorted(times.items(),key=lambda a:a[0])


    def getParameters(self):
        params = dict()
    
        params["cpu"]=ps.cpu_percent(interval=0.05)
        network=ps.net_io_counters()
        
        params["packets_sent"]=self.calculate_diff("packets_sent", network[2])
        params["packets_recv"]=self.calculate_diff("packets_recv", network[3])
        
        hdd=ps.disk_io_counters(perdisk=False) #TODO: Bad hack! Fixme
        
        params["hdd1ReadTime"] = self.calculate_diff("hdd1ReadTime", hdd[4])
        params["hdd1WriteTime"] = self.calculate_diff("hdd1WriteTime", hdd[5])
        
        params["hdd1ReadCount"] = self.calculate_diff("hdd1ReadCount", hdd[0])
        params["hdd1WriteCount"] = self.calculate_diff("hdd1WriteCount",hdd[1])

        params["hdd1ReadBytes"] = self.calculate_diff("hdd1ReadBytes", hdd[2])
        params["hdd1WriteBytes"] = self.calculate_diff("hdd1WriteBytes", hdd[3])

        params["batteryEnergyChange"] = self.getBatteryLevel()
        params["batteryChargeInPercent"] = self.getBatteryPercent()
        
        cpu_info = ps.cpu_times()
        
        #cpu_user=0, cpu_sys=0, cpu_ide=0, cpu_iowait=0, cpu_irq=0 \cpu_softirq=0
        
        params["cpu_user"] = self.calculate_diff("cpu_user",cpu_info[0])
        params["cpu_sys"] = self.calculate_diff("cpu_sys", cpu_info[1])
        params["cpu_idle"] = self.calculate_diff("cpu_idle",cpu_info[2])
        params["cpu_iowait"] = self.calculate_diff("cpu_iowait",cpu_info[4])
        params["cpu_irq"] = self.calculate_diff("cpu_irq",cpu_info[5])
        params["cpu_softirq"] = self.calculate_diff("cpu_softirq",cpu_info[6])
        params["cpu_clock"] = self.getCpuSpeed()
        
        params["display_brightness"] = self.getDisplayBacklight()

        cpu_states = self.getCpuStates()
        for key, val in cpu_states:
            params["cpu_%s"%key]=self.calculate_diff("cpu_%s"%key, val)
        
        #print "Battery level is {0}. ({1}% charged)".format(batteryLevel, batteryPercent)

        parameter=Parameter(**params)
        return parameter

def win_get_battery_rate():
    """
    Returns the battery charge or discharge rate in mW
    """
    l = ctypes.windll.LoadLibrary("powrprof")

    SystemBatteryState = 5  
    
    class SYSTEM_BATTERY_STATE(ctypes.Structure):
        _fields_ = [
                    ("AcOnLine", ctypes.c_bool),
                    ("BatteryPresent", ctypes.c_bool),
                    ("Charging", ctypes.c_bool),
                    ("Discharging", ctypes.c_bool),
                    ("Spare1", ctypes.c_bool * 4),
                    ("MaxCapacity", ctypes.c_long),
                    ("RemainingCapacity", ctypes.c_long),
                    ("Rate", ctypes.c_long),
                    ("EstimatedTime", ctypes.c_long),
                    ("DefaultAlert1", ctypes.c_long),
                    ("DefaultAlert2", ctypes.c_long),
                    ]
    
    
    sb = SYSTEM_BATTERY_STATE(0)
    retval = l.CallNtPowerInformation(SystemBatteryState, 
                                      None, 0, 
                                      ctypes.addressof(sb), ctypes.sizeof(sb))
    assert retval == 0  
    
    return sb.Rate / 1000.0


def win_get_battery_life_percent():    
    """
    Returns the remaining battery level in percent.
    """

    
    class SYSTEM_POWER_STATUS(ctypes.Structure):
        _fields_ = [
            ('ACLineStatus', ctypes.wintypes.BYTE),
            ('BatteryFlag', ctypes.wintypes.BYTE),
            ('BatteryLifePercent', ctypes.wintypes.BYTE),
            ('Reserved1', ctypes.wintypes.BYTE),
            ('BatteryLifeTime', ctypes.wintypes.DWORD),
            ('BatteryFullLifeTime', ctypes.wintypes.DWORD),
        ]

    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = ctypes.wintypes.BOOL

    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()

    return status.BatteryLifePercent

class WinSystem:
    
    def __init__(self):

        self.c_wmi = wmi.WMI ()

        self.diff = {}

        self.getParameters()
    
    def calculate_diff(self, stream_name, value):
        if not stream_name in self.diff:
            self.diff[stream_name] = Differentiator()

        return self.diff[stream_name](value)

    def get_current_clock_speed(self):
        processors = self.c_wmi.Win32_Processor ()
        return sum([p.CurrentClockSpeed for p in processors])/len(processors)
    
    def getParameters(self):
        params = dict()
    
        params["cpu"]=ps.cpu_percent(interval=0.85)
        network=ps.net_io_counters()
        
        params["packets_sent"]=self.calculate_diff("packets_sent", network[2])
        params["packets_recv"]=self.calculate_diff("packets_recv", network[3])
        
        hdd=ps.disk_io_counters(perdisk=False) #TODO: Bad hack! Fixme
        
        params["hdd1ReadTime"] = self.calculate_diff("hdd1ReadTime", hdd[4])
        params["hdd1WriteTime"] = self.calculate_diff("hdd1WriteTime", hdd[5])
        
        params["hdd1ReadCount"] = self.calculate_diff("hdd1ReadCount", hdd[0])
        params["hdd1WriteCount"] = self.calculate_diff("hdd1WriteCount",hdd[1])

        params["hdd1ReadBytes"] = self.calculate_diff("hdd1ReadBytes", hdd[2])
        params["hdd1WriteBytes"] = self.calculate_diff("hdd1WriteBytes", hdd[3])

        params["batteryEnergyChange"] = win_get_battery_rate()
        params["batteryChargeInPercent"] = win_get_battery_life_percent()
        
        cpu_info = ps.cpu_times()
        
        #cpu_user=0, cpu_sys=0, cpu_ide=0, cpu_iowait=0, cpu_irq=0 \cpu_softirq=0
        
        params["cpu_user"] = self.calculate_diff("cpu_user",cpu_info[0])
        params["cpu_sys"] = self.calculate_diff("cpu_sys", cpu_info[1])
        params["cpu_idle"] = self.calculate_diff("cpu_idle",cpu_info[2])
        params["cpu_iowait"] = self.calculate_diff("cpu_iowait",cpu_info[4])
        params["cpu_irq"] = self.calculate_diff("cpu_irq",cpu_info[5])
        params["cpu_softirq"] = self.calculate_diff("cpu_softirq",cpu_info[6])
        params["cpu_clock"] = self.get_current_clock_speed()
        
        #print "Battery level is {0}. ({1}% charged)".format(batteryLevel, batteryPercent)

        parameter=Parameter(**params)
        return parameter


if __name__=="__main__":
    li = LinuxSystem()
    print li.getDisplayBacklight()
