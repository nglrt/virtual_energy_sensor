import random
import simplejson
import logging
import os
import sys

class Configuration(object):
    def __init__(self, plugwise_server=None, upstream_server=None, machine_id=None, local_storage="", plugwise_mac_address="",local_storage_activated = False, activated=True, computer_name="", tag="default", downsample_factor=25, logfile_name="trace_{machine_id}_{date}.csv"):
        if plugwise_server == None:
            plugwise_server = "127.0.0.1"
        if upstream_server == None:
            upstream_server = "10.0.19.4"
        if machine_id ==None:
            random.seed()
            machine_id = random.randint(0, 99999999)
        
        self.plugwise_mac_address = plugwise_mac_address
        self.plugwise_server = plugwise_server
        self.upstream_server = upstream_server
        self.local_storage = local_storage
        self.local_storage_activated = local_storage_activated
        self.activated = activated
        self.machine_id = machine_id
        self.computer_name = computer_name
        self.tag = tag
        self.downsample_factor = int(downsample_factor)
        self.logfile_name=logfile_name
    
    @staticmethod
    def getConfigFileLoc():
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            config_dir = os.path.dirname(sys.executable)
        elif __file__:
            config_dir = os.path.dirname(__file__)
        
        return os.path.join(config_dir, "config.json")

    def save(self):
        json_str = simplejson.dumps(self.__dict__)
        
        config_file = open(Configuration.getConfigFileLoc(), "w+")
        config_file.write(json_str)

    @staticmethod
    def load():
        config_file = Configuration.getConfigFileLoc()
        logging.info("Reading config from {0}".format(config_file))
        if not os.path.isfile(config_file):
            return Configuration()

        config_file = open(config_file, "r")
        json_str = config_file.read()
        json_dict = simplejson.loads(json_str)

        return Configuration(**json_dict)

