#!/usr/bin/python

#Authors: Gaetano Carlucci
#         Giuseppe Cofano

import os, psutil,math
import threading
import time
import thread
import multiprocessing 


class MonitorThread(threading.Thread):
    def __init__(self, coreID):
        self.interval = 0.1;
        self.sample = 0;
        self.cpu = 0;
        self.running = 1;
        self.alpha = 0.1;
        self.cpu_log = list()
        self.coreID = coreID
        super(MonitorThread, self).__init__()
        
    def get_cpu_load(self):
        return self.cpu
        
    def run(self):
        p = psutil.Process(os.getpid())
        p.set_cpu_affinity([self.coreID]) #the process is forced to run only on CPU coreID
        while self.running:
            self.sample = p.get_cpu_percent(interval=self.interval)
            self.cpu = self.alpha * self.sample + (1-self.alpha)*self.cpu
            self.cpu_log.append(self.cpu)


class ControllerThread(threading.Thread):
    def __init__(self):
        self.running = 1;
        self.sleepTime = 0.0;
        self.CT = 0.20;    #default value
        self.cpu = 0;
        self.ki = -1;
        self.kp = -0.5;
        self.int_err = 0;
        self.last_ts = time.time();
        super(ControllerThread, self).__init__()
        
    def getSleepTime(self):
        return self.sleepTime

    def getCpuTarget(self):
        return self.CT

    def setCpu(self, cpu): 
       self.cpu = cpu

    def setCpuTarget(self, CT): 
       self.CT = CT
     
    def run(self):
        #through this timer this cycle has the same sampling interval as the cycle in MonitorThread
        while self.running:
           time.sleep(0.1)
           self.err = self.CT - self.cpu*0.01
           ts = time.time()
           
           samp_int = ts - self.last_ts
           self.int_err = self.int_err + self.err*samp_int
           self.last_ts = ts
           self.sleepTime = self.kp*self.err + self.ki*self.int_err
           
           
           if self.sleepTime < 0:
              self.sleepTime = 0;
              self.int_err = self.int_err - self.err*samp_int
              

def benchmark_single_core(coreID, load_level=0.2, duration = 20):
    """ coreID is the core which you want to test """
   
                
    monitor = MonitorThread(coreID)       
    monitor.start()

    SAMPLES=1000;

    control = ControllerThread()
    control.start()
    control.setCpuTarget(load_level)
    last_ts = time.time()

    tempo = 0
    
    while tempo < duration:

        for i in range(1,2):
           pr = 213123 + 324234 * 23423423

        control.setCpu(monitor.get_cpu_load())
        sleep_time = control.getSleepTime()
        time.sleep(sleep_time)
        
        ts = time.time()
        delta = ts - last_ts
        last_ts = ts
        tempo += delta

    monitor.running = 0;
    control.running = 0;
    monitor.join()
    control.join()
               
def run_benchmark():
    load_levels = range(0,10, 1)    
    
    for load_level in load_levels:
        # determine number of cores and overload the CPU
        print "Load Level %s" % (1.0 * load_level / 10)
    
        process_list = []
        for idx in xrange(multiprocessing.cpu_count()):
            p = multiprocessing.Process(target=benchmark_single_core, args=(idx,1.0*load_level/10))
            p.start()
            process_list.append(p)
            
        [p.join() for p in process_list]
    
    print "done"

if __name__ == "__main__":
    run_benchmark()
    
   

    
    
