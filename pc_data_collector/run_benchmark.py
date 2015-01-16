import os
import tasks
from blinker import signal
import logging
from backend import CollectDataAndUploadWorker
import sys
import signal as sig
from config import Configuration
import random
from benchmark.cpu import run_benchmark as run_cpu_benchmark
from benchmark.network import run_benchmark as run_network_benchmark
from benchmark.testdisk import run_benchmark as run_disk_benchmark
from benchmark.backlight import run_benchmark as run_backlight_benchmark
import threading
import time

logging.basicConfig()

if __name__=="__main__":

    config = Configuration.load()
    
    config.downsample_factor=10
    
    freq = 25.0 / config.downsample_factor
    
    config.logfile_name = "trace_{machine_id}_"+str(freq)+"hz_{date}.csv"
    
    worker = CollectDataAndUploadWorker(config)
    worker.startWorker()

    logging.info("Idle 60s benchmark")
    time.sleep(60)        
    
    logging.info("Running CPU benchmark")
    run_cpu_benchmark()
    
    logging.info("Running Network benchmark")        
    run_network_benchmark()
    
    logging.info("Running Disk benchmark") 
    run_disk_benchmark()        
    
    logging.info("Running Backlight benchmark")
    run_backlight_benchmark()
    
    logging.info("Done")
