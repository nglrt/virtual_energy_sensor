# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 10:32:15 2014

@author: Patrick
"""

class Parameter():
    def __init__(self,cpu=0,hdd1ReadTime=0,hdd1WriteTime=0,difReadTimeSecondHD=0,\
                difWriteTimeSecondHD=0,packets_sent=0,packets_recv=0, batteryEnergyChange=0,\
                batteryChargeInPercent=0,hdd1ReadCount=0, hdd1WriteCount=0, hdd1ReadBytes=0, \
                hdd1WriteBytes=0, cpu_user=0, cpu_sys=0, cpu_idle=0, cpu_iowait=0, cpu_irq=0, \
                cpu_softirq=0, cpu_clock = 0, cpu_state0=0, cpu_state1=0, cpu_state2=0, \
                cpu_state3=0, cpu_state4=0, cpu_state5=0, display_brightness=0, **kwargs):    
        self.cpu                    = cpu
        self.difReadTimeMainHD      = hdd1ReadTime
        self.difWriteTimeMainHD     = hdd1WriteTime
        self.difReadTimeSecondHD    = difReadTimeSecondHD
        self.difWriteTimeSecondHD   = difWriteTimeSecondHD
        self.difPackets_sent        = packets_sent
        self.difPackets_recv        = packets_recv
        self.batteryEnergyChange    = batteryEnergyChange
        self.batteryChargeInPercent = batteryChargeInPercent
        self.readCountHdd           = hdd1ReadCount
        self.writeCountHdd          = hdd1WriteCount
        self.hdd1ReadBytes          = hdd1ReadBytes
        self.hdd1WriteBytes         = hdd1WriteBytes
        self.cpu_user               = cpu_user
        self.cpu_sys                = cpu_sys
        self.cpu_idle               = cpu_idle
        self.cpu_iowait             = cpu_iowait
        self.cpu_irq                = cpu_irq
        self.cpu_softirq            = cpu_softirq
        self.cpu_clock              = cpu_clock
        self.cpu_state0             = cpu_state0
        self.cpu_state1             = cpu_state1
        self.cpu_state2             = cpu_state2
        self.cpu_state3             = cpu_state3
        self.cpu_state4             = cpu_state4
        self.cpu_state5             = cpu_state5
        self.display_brightness     = display_brightness
        
    def as_list(self):
        row = [self.cpu,self.difReadTimeMainHD,self.difWriteTimeMainHD,
                     self.difReadTimeSecondHD,self.difWriteTimeSecondHD,
                     self.difPackets_sent,self.difPackets_recv,  
                     self.batteryEnergyChange, self.batteryChargeInPercent, 
                     self.readCountHdd, self.writeCountHdd, self.cpu_user,
                     self.cpu_idle, self.cpu_iowait, self.cpu_irq, self.cpu_softirq,
                     self.cpu_clock, self.cpu_state0, self.cpu_state1, self.cpu_state2,
                     self.cpu_state3, self.cpu_state4, self.cpu_state5, 
                     self.display_brightness]
        return row
        
        
