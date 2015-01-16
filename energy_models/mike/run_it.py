from __future__ import print_function
import sh
import array
import extract
import numpy as np
import window
import edimax
import sys
import csv
from datetime import datetime
import argparse

class AudioSampleCollector(object):


    def __init__(self, device_name, edimax_ip, audio_device="hw:0,0"):
        self.feature_extractor = extract.FeatureExtractor(windowSize = 4400, stepSize=4400, threshold=0)
        self.ip = edimax_ip
        self.file = open("data/audio_{1}_{0:%Y%m%d_%H%M}.csv".format(datetime.now(), device_name), 'w')
        self.csv_writer = csv.writer(self.file, delimiter=';')
        self.audio_device = audio_device

    def _write_row(self, row):
        self.csv_writer.writerow(row)
        self.file.flush()

    def collect_features(self):

        result = sh.arecord("-", device=self.audio_device, rate="48k", format="S16_LE", duration=1, channels=1)
        power = edimax.edimax_get_power(self.ip)

        data_vec = np.array(array.array('h', result.stdout ))


        #data_vec = data_vec / 32000 # Make the numbers smaller

        #f0 = self.feature_extractor(data_vec, 5)
        f1 = self.feature_extractor(data_vec, 1)
        f2 = [power]

        #row = np.concatenate((f0[0,:], f1[0,:], f2))
        for i in range(f1.shape[0]):        
            row = np.concatenate((f1[i,:], f2))
            self._write_row(row)
            
        return power


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="auto", help="ip address of the edimax adapter. If not specified, the ip is automatically discovered")
    parser.add_argument("device", help="The device which is currently monitored")
    parser.add_argument("--audio_hardware", default="hw:0,0", help="The audio hardware for recording")
    args = parser.parse_args()

    if args.ip == "auto":
        print("Automatically searching for edimax devices", file=sys.stderr)
        edimax_devices = edimax.find_edimax_devices()

        if len(edimax_devices) == 0:
            print("No Edimax device found. Aborting", file=sys.stderr)
            exit(1)
    else:
        edimax_devices = [args.ip]

    print("Using Edimax Smart Plug with IP {0}".format(edimax_devices[0]), file=sys.stderr)
    print("Using Audio Hardware {0}".format(args.audio_hardware), file=sys.stderr)

    collector = AudioSampleCollector(args.device, edimax_devices[0], args.audio_hardware)

    try:
        for i in range(1000):
            pwr_info = collector.collect_features()
            print("Round {0}	{1}W".format(i, pwr_info))
    except KeyboardInterrupt:
        print("KeyboardInterrupt", file=sys.stderr)

if __name__ == "__main__":
    main()
