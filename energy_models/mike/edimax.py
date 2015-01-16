import requests
from bs4 import BeautifulSoup
import csv
import time
import datetime
import nmap
import logging

logger = logging.getLogger("edimax")


def find_edimax_devices():
    """
    Returns a list of available Edimax smartplugs which are available in the
    current environment
    """

    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.42.0/24', arguments='-sn')

    host_list = []
    for host in nm.all_hosts():
        logger.debug("Host {0} is online".format(host))
        try:
            power = edimax_get_power(host)
            host_list.append(host)
            logger.debug("Edimax found on host: {0} ".format(host))
        except:
            logger.debug("No edimax present on {0} ".format(host))

    return host_list



def edimax_get_power(ip_addr="192.168.178.137"):
    """
    Quelle http://sun-watch.net/index.php/eigenverbrauch/ipschalter/edimax-protokoll/
    """
    
    req = """<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax"><CMD id="get">
    <NOW_POWER><Device.System.Power.NowCurrent>
    </Device.System.Power.NowCurrent><Device.System.Power.NowPower>
    </Device.System.Power.NowPower></NOW_POWER></CMD></SMARTPLUG>
    """
    
    r = requests.post("http://{0}:10000/smartplug.cgi".format(ip_addr), auth=("admin","1234"), data=req)
    soup = BeautifulSoup(r.text, features="xml")
    power = soup.find(name="Device.System.Power.NowPower").get_text()
    
    print r.text
    return float(power)

if __name__ == "__main__":
    print find_edimax_devices()
