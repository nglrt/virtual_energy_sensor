from __future__ import print_function
import array
import numpy as np
import window
import edimax
import sys
import h5py
from datetime import datetime
import argparse
import gevent
import alsaaudio
import signal

CHUNK = 4000
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 44100

from gevent import monkey
monkey.patch_socket(dns=True, aggressive=True)

class AudioSampleCollector(object):


    def __init__(self, device_name, edimax_ip, audio_device="hw:0,0"):
        fname = "data/audio_{1}_{0:%Y%m%d_%H%M}.hdf5".format(datetime.now(), device_name)
        self.file = h5py.File(fname, 'w')
        self.audio_dset = self.file.create_dataset("audio", (0, CHUNK/2), maxshape=(None, CHUNK/2))
        self.power_dset = self.file.create_dataset("power", (0, 1), maxshape=(None, 1))

        self.ip = edimax_ip
        self.audio_device = audio_device

        self.chunk_count = 0
        self.power = 0

        self.running = True

        #self.record_audio()
        self.g_audio = gevent.spawn_later(2, self.record_audio,)
        self.g_power = gevent.spawn(self.record_power)

        print("Recording started...")

    def stop(self):
        self.running=False
        gevent.killall([self.g_audio, self.g_power])

    def record_audio(self):
        try:
            print("Audio Recorder Greenlet started")
            
            inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, self.audio_device)
            inp.setchannels(1)
            inp.setrate(RATE)
            inp.setformat(FORMAT)
            inp.setperiodsize(CHUNK/2)

            while self.running:
                l, data = inp.read()
		
		#print(l)
                data_vec = np.array(array.array('h', data ))
                #print(data_vec.shape) 
                self.audio_dset.resize(self.chunk_count+1, axis = 0)
                self.power_dset.resize(self.chunk_count+1, axis = 0)
                self.audio_dset[self.chunk_count, :] = data_vec
                self.power_dset[self.chunk_count, 0] = self.power
                self.chunk_count += 1
                gevent.sleep(0.00001)

        except KeyboardInterrupt:
            print("Keyboard interrupt [audio]")
            self.stop()


    def record_power(self):
        print("Power Recorder Greenlet started")
        try:
            self.power_chunk_count = 0
            while self.running:
                self.power = edimax.edimax_get_power(self.ip)
                gevent.sleep(1.0)
        except KeyboardInterrupt:
            print("Keyboard Interrupt [power]")
            self.stop()


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
    #gevent.signal(signal.SIGQUIT, collector.stop())

    try:
        for i in range(1000):
            print("{0}\tChunks #{1}\tPower \t{2}W".format(i, collector.chunk_count, collector.power))
            gevent.sleep(1.0)

            if not collector.running:
                break

    except KeyboardInterrupt:
        print("KeyboardInterrupt [main]", file=sys.stderr)

    collector.stop()

if __name__ == "__main__":
    
    main()
