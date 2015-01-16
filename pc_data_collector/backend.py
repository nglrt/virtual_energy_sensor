import system
import mosquitto
import time
import simplejson
from datetime import datetime
import csv
import threading
from blinker import signal
import os
import traceback
import logging
from threading import Thread

PLUGWISE_MAC="B7BE96"
PLUGWISE_POWER_SERVER="127.0.0.1"

class DataCollector(threading.Thread):

    def __init__(self, plugwise_server=PLUGWISE_POWER_SERVER, mac=PLUGWISE_MAC, machine_id = "1", downsample_factor = 25):
        super(DataCollector, self).__init__()
        self.plugwise_server = plugwise_server
        self.mac = mac
        
        logging.info("Plugwise Server: {0}".format(self.plugwise_server))
        logging.info("Plugwise Mac: {0}".format(self.mac))
        
        self.machine_id = machine_id

        self.plugwise_status = signal("plugwise.status")
        self.state_update = signal("plugwise.state_update")

        self.client = mosquitto.Mosquitto("M{1}_{0}".format(self.__class__.__name__, machine_id))
        self.client.on_connect = self._onConnect
        self.client.connect(plugwise_server)
        self.client.on_message = self._onPowerMessage
        self.client.on_subscribe = self._onSubscribe
        self.client.on_disconnect = self._onDisconnect
        
        self.client.subscribe("smtk/raw/#",1)
        
        self.system = system.get_system()
        self.daemon = True
        self.running = True
        
        self.downsample_factor = downsample_factor
        self.samples = []
        
        

    def _onDisconnect(self, mosq, obj, rc):
        logging.info("DataCollector disconnected successfully.")
        self.plugwise_status.send("Disconnected")

    def _onConnect(self, mosq, obj, rc):
        if rc == 0:
            logging.info("DataCollector Connected successfully.")
            self.plugwise_status.send("Connected")

    def _onPowerMessage(self, cli, obj, msg):
        data = simplejson.loads(msg.payload)
        
        if data["sender"].endswith(self.mac):
        
            t,y,ys = data["t"], data["y"], data["ys"]
            self.samples.append((t,y,ys))
           
            if len(self.samples) == self.downsample_factor:
                t = self.samples[0][0]
                y = sum(s[1] for s in self.samples) / self.downsample_factor
                ys = sum(s[2] for s in self.samples) / self.downsample_factor
                
                self.samples = []
                
                self.processPowerMessage(t,y,ys)
        
    def processPowerMessage(self, t, y, ys):
        
        stateVariables = self.system.getParameters()

        csv_row = stateVariables.as_list()
        csv_row.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        csv_row.append(float(y))
        csv_row.append(float(ys))

        self.state_update.send({"machine_id":self.machine_id, "mac":self.mac, "state_variables": csv_row})
        self.plugwise_status.send("{0:0.3}W".format(ys))

        #logging.debug( data)
    
    def close(self):
        try:
            logging.info("disconnecting...")
            self.client.disconnect()
        except:
            logging.warn("Disconnect failed...")

    def _onSubscribe(self, mosq, obj, mid, qos_list):
        logging.info("Subscription setup successful %s" %mid)
        self.plugwise_status.send("Subscription successfull.")

    def run(self):
        self.plugwise_status.send("Connecting")
        while self.running:
            self.client.loop(1)

        self.client.disconnect()
        self.plugwise_status.send("Stopping data collector thread....")


class StateFileWriter(object):
    def __init__(self, logFileDir, filename="trace_{machine_id}_{date}.csv"):
        self.logFileDir = logFileDir
        self.state_update = signal("plugwise.state_update")
        self.logFile = None
        self.file_name = None
        self.filename_template = filename

        self.state_update.connect(self._onStateChange)
        
    def _getLogFile(self, machine_id):
        file_name = self.filename_template.format(machine_id= str(machine_id), date=datetime.today().strftime('%Y-%m-%d'))

        if file_name != self.file_name or self.logFile == None:
            self.file_name = file_name
            fd = open(os.path.join(self.logFileDir,file_name), "ab")
            self.logFile = csv.writer(fd, delimiter=';', quotechar='"')

        return self.logFile

    def close(self):
        self.state_update.disconnect(self._onStateChange)

    def _onStateChange(self, msg):
        self.writeRow(msg["machine_id"],msg["state_variables"])

    def writeRow(self, machine_id, state_variables):
        fd = self._getLogFile(machine_id)
        fd.writerow(state_variables)

class WatchDog(object):
    def __init__(self, signal_name, timeout=30):
        self.signal = signal(signal_name)
        self.signal.connect(self.on_signal)
        self.signal_name = signal_name
        self.timeout = timeout

        self.timeout_signal = signal("watchdog.missing.%s" % self.signal_name)
        self.running=True

        self.last_ok = datetime.now()

        self.setupTimer()

    def setupTimer(self):
        self.timer = Thread(target=self._run)
        self.timer.daemon = True
        self.timer.start()

    def _run(self):
        while self.running:
            time.sleep(1)

            diff = datetime.now() - self.last_ok
            if diff.total_seconds() > self.timeout:
                logging.warn("Timeout happened after %s sec" % diff.total_seconds())
                self.timeout_signal.send()
                self.last_ok = datetime.now()

        logging.info("Watchdog Thread for signal %s stopped" % self.signal_name)

    def on_signal(self, *args, **kwargs):
        self.last_ok = datetime.now()

    def cancel(self):
        self.running=False

class DataUploader(threading.Thread):
    def __init__(self, upload_server, machine_id, computer_name):
        super(DataUploader, self).__init__()
        self.machine_id = machine_id
        self.upload_server = upload_server
        self.computer_name = computer_name

        self.state_update = signal("plugwise.state_update")
        self.keep_alive = signal("uploader.keep_alive")
        self.uploader_status = signal("uploader.status")

        self.client = mosquitto.Mosquitto("M{1}_{0}".format(self.__class__.__name__, machine_id))
        self.client.on_connect = self._onConnect
        self.client.on_disconnect = self._onDisconnect
        self.client.on_publish = self._onPublish
        self.client.connect(self.upload_server)

        self.publish_count = 0
        self.ack_count = 0
        
        self.tag = "default"

        self.state_update.connect(self._onStatusUpdate)
        self.running=True
        self.daemon = True
        
        logging.info("Machine id is {0}".format( machine_id ))
        logging.info("computer name is {0}".format( computer_name))
        logging.info("Upload Server: {0}".format(upload_server))

    def close(self):
        try:
            logging.info("Data Uploader is disconnecting")
            self.client.disconnect()
        except:
            logging.warn("Data Uploader disconnect failed")

    def _onPublish(self, mosq, msg, mid):
        fail = self.publish_count - self.ack_count
        self.uploader_status.send("Upload: {0} ok, {1} fail".format(self.ack_count, fail))
        self.keep_alive.send()
        self.ack_count += 1

    def _onStatusUpdate(self, msg):
        msg["machine_name"]=self.computer_name
        msg["tag"] = self.tag
        msg_str = simplejson.dumps(msg)
        
        #print msg["machine_name"]
        
        self.client.publish("smtk/state_variables/{0}".format(self.machine_id), msg_str)
        self.publish_count += 1

    def _onDisconnect(self, mosq, obj, rc):
        logging.info("Data Uploader Disconnected successfully (rc={0}).".format(rc))
        self.uploader_status.send("Disconnected")

    def _onConnect(self, mosq, obj, rc):
        if rc == 0:
            logging.info("Connected successfully.")
            self.uploader_status.send("Connected")

    def run(self):
        while self.running:
            self.client.loop(1)

        self.state_update.disconnect(self._onStatusUpdate)
        self.client.disconnect()
        self.uploader_status.send("Stopping DataUploader thread...")


class CollectDataAndUploadWorker(object):
    def __init__(self, config):
        self.config = config
        
        signal("config.changed").connect(self.on_config_change)

        threading.Thread(target=self.startWorker).start()

        self.uploaderWatchdog = WatchDog("uploader.keep_alive")
        self.uploaderWatchdog.timeout_signal.connect(self.onTimeout)

    def __enter__(self):
        pass
        
    def __exit__(self, *args, **kwargs):
        logging.info("Exiting")
        if hasattr(self, "collector"):
            self.collector.running=False
            self.collector.join()
            self.collector.close()
            
        if hasattr(self, "uploader"):
            self.uploader.running=False
            self.uploader.join()
            self.uploader.close()
            
        self.uploaderWatchdog.cancel()

    def on_config_change(self, *args, **kwargs):
        self.resetWorker()

    def resetWorker(self):
        if hasattr(self, "collector"):
            self.collector.running=False
            self.collector.join()
            self.collector.close()
        
        if hasattr(self, "uploader"):
            self.uploader.running=False
            self.uploader.join()
            self.uploader.close()

        if self.store != None:
            self.store.close()

        self.startWorker()

    def startWorker(self):
        c = self.config
        logging.info ("connecting")
        try:
            self.uploader = DataUploader(c.upstream_server, c.machine_id, c.computer_name)
            self.uploader.tag = c.tag
            self.uploader.start()
        except Exception as e:
            logging.exception(e)
            logging.warn ("connection failed")
            signal("uploader.status").send("Failed...")

        if c.local_storage_activated:
            self.store = StateFileWriter(c.local_storage, filename=c.logfile_name)
        else:
            self.store = None

        try:
            self.collector = DataCollector(plugwise_server = c.plugwise_server, \
                                    mac = c.plugwise_mac_address, \
                                    machine_id=c.machine_id, downsample_factor = c.downsample_factor)
            self.collector.start()
        except Exception as e:
            logging.warn("Plugwise has %s" % e)
            logging.exception(e)
            
            signal("plugwise.status").send("Failed...")

    def onTimeout(self, *args, **kwargs):
        logging.warn("Sth. went horribly wrong... resetting.")
        signal("uploader.status").send("Timeout...")
        self.resetWorker()

if __name__=="__main__":
    collector = DataCollector()
    collector.run()
