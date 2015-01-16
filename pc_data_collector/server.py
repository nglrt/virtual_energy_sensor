import mosquitto
import simplejson
from datetime import datetime
import csv
import os

SERVER="127.0.0.1"

class App(object):
    def __init__(self, server):
        self.client = mosquitto.Mosquitto(self.__class__.__name__)
        self.client.on_connect = self._onConnect
        self.client.connect(server)
        self.client.on_message = self._onStateMessage
        self.client.on_subscribe = self._onSubscribe
        self.client.on_disconnect = self._onDisconnect

        self.client.subscribe("smtk/state_variables/#",1)

        self.files = {}
        self.handles = {}
        self.file_names = {}
    def _onDisconnect(self, obj, rc):
        if rc == 0:
            print("Disconnected successfully.")
        else:
            print("Unexpected disconnect")

    def _onConnect(self, mosq, obj, rc):
        if rc == 0:
            print("Connected successfully.")

    def get_log_file_fd(self, machine_id, tag_name="default", machine_name=None):
        
        if machine_name != None:
            path = os.path.join("./recordings", machine_name, tag_name)        
        else:
            path = os.path.join(path)
        
        if not os.path.exists(path):
            os.mkdirs(path)        
        
        date_str = datetime.today().strftime('%Y-%m-%d')
        file_name = 'trace_{0}_{1}.csv'.format(str(machine_id),date_str)
        full_file_path = os.path.join(path, file_name)        
        
        if not machine_id in self.files or self.file_names[machine_id] != full_file_path:
            print("Starting file {0}".format(full_file_path))
        
            fd = open(full_file_path, 'ab')
            self.files[machine_id] = csv.writer(fd, delimiter=';', quotechar='"')
            self.handles[machine_id] = fd
            self.file_names[machine_id] = full_file_path

        return self.files[machine_id]

    def _onStateMessage(self, cli, obj, msg):
        data = simplejson.loads(msg.payload)
        
        if "tag" in data:
            tag = data["tag"]
        else:
            tag = "default"
        
        if "machine_name" in data:
            machine_name = data["machine_name"]
        else:
            machine_name = None
        
        logFile = self.get_log_file_fd(data["machine_id"], tag, machine_name)
        logFile.writerow(data["state_variables"])
        self.handles[data["machine_id"]].flush()
    
    def _onSubscribe(self, mosq, obj, mid, qos_list):
        print("Subscription setup successful %s" %mid)

    def run(self):
        self.client.loop_forever()

if __name__ == '__main__':
    m = App(SERVER)
    m.run()