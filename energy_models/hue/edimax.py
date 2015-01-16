import requests
from bs4 import BeautifulStoneSoup
import phue
import csv
import time
import datetime

# Quelle http://sun-watch.net/index.php/eigenverbrauch/ipschalter/edimax-protokoll/

def edimax_get_power(ip_addr="192.168.178.137"):

    req = """<?xml version="1.0" encoding="UTF8"?><SMARTPLUG id="edimax"><CMD id="get">
    <NOW_POWER><Device.System.Power.NowCurrent>
    </Device.System.Power.NowCurrent><Device.System.Power.NowPower>
    </Device.System.Power.NowPower></NOW_POWER></CMD></SMARTPLUG>
    """
    
    r = requests.post("http://{0}:10000/smartplug.cgi".format(ip_addr), auth=("admin","1234"), data=req)
    soup = BeautifulStoneSoup(r.text)
    power = soup.find(name="Device.System.Power.NowPower").get_text()
    
    return float(power)

class HueEnergy(object):
    def __init__(self):
        self.b = phue.Bridge(ip="192.168.178.109")
        self.b.connect()

        self.x = np.linspace(0, 1, 100)
        self.y = np.linspace(0, 1, 100)
        self.colortemp = np.linspace(154, 500, 10)
        self.saturation = np.linspace(0, 254, 10)
        self.hue = np.linspace(0, 65535, 10)
        self.brightness = np.linspace(0, 254, 100)
        
        
    def run_test(self, params):
        x = self.x[params[0]]
        y = self.y[params[1]]
        
        colortemp = int(self.colortemp[params[2]])
        saturation = int(self.saturation[params[3]])
        hue = int(self.hue[params[4]])
        brightness=int(self.brightness[params[5]])
        
        light = self.b.get_light_objects("id")[1]
        #print light
        assert isinstance(light, phue.Light)
        light.xy = (x,y)
        light.colortemp = colortemp
        light.saturation = saturation
        #light.hue = hue
        light.brightness = brightness
        
        time.sleep(4)
        
        power = edimax_get_power()
        
        return {"x":x, "y":y, "colortemp":colortemp, "saturation":saturation, "hue":hue, "brightness":brightness, "power":power}

def test_rand(writer, hue):
    factors = np.random.rand(1000,6)            
    fac_int = np.floor(factors * 10)           
    
    for i in range(fac_int.shape[0]):
        print ("{0} / {1}".format(i, fac_int.shape[0]))
        dict_ = hue.run_test(fac_int[i])
        writer.writerow(dict_)

def test_bright(writer, hue):
    factors = [0,0,9,9,9,9]  
    
    for i in range(0, len(hue.brightness)):
        factors[5]=i
        dict_ = hue.run_test(factors)
        writer.writerow(dict_)
        
        print("{0}/{1}".format(i, len(hue.brightness)))

def main():
    
    test_functions = {"rnd":test_rand, "bri":test_bright}    
    mode = "bri"
    
    date = datetime.datetime.now()
    with open('hue_power_{1}_{0}.csv'.format(date.strftime("%Y.%m.%d_%H%M"), mode), 'w') as csvfile:
            fieldnames = ['x', 'y', 'colortemp', 'saturation', 'hue', 'brightness', 'power']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
            writer.writeheader()
            
            hue = HueEnergy()
            test_functions[mode](writer, hue)
            
            print("done")
    
if __name__=="__main__":    
    main()
    