import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
import logging
import os

from config import Configuration
from backend import CollectDataAndUploadWorker

path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
filename = os.path.join(path, "data_collector_service.log"),
level = logging.DEBUG,
format = '[data-collector] %(levelname)-7.7s %(message)s'
)
 
class DataCollectorSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "DataCollector-Service"
    _svc_display_name_ = "Data Collector Service"
    
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
     
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('Stopping service ...')
        self.stop_requested = True
     
    def SvcDoRun(self):
        servicemanager.LogMsg(
        servicemanager.EVENTLOG_INFORMATION_TYPE,
        servicemanager.PYS_SERVICE_STARTED,
        (self._svc_name_,'')
        )
        self.main()
     
    def main(self):
        logging.info(' ** Data Collector has started ** ')
        
        logging.info(' Base dir is %s' % path)
        # Simulate a main loop

        config = Configuration.load()
        worker = CollectDataAndUploadWorker(config)
        
        with worker:
            while True:
                if self.stop_requested:
                    logging.info('A stop signal was received: Breaking main loop ...')
                    break
                time.sleep(.1)
                
        logging.info("Exiting")
     
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DataCollectorSvc)