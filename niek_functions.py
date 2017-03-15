# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:57:50 2017

@author: Niek
#"""
import visa
import numpy as np
import matplotlib as plt
import time
import string

class ENA(object):
    def _init_(self): 
           rm = visa.ResourceManager()
           print(rm.list_resources())
           self = rm.open_resource('USB0::0x0957::0x1309::MY49406990::0::INSTR')
           self.read_termination = '\n'
           self.write_termination = '\n'
           print(self.query("*IDN?"))
           return self
           
    
    
    def setup(self,v): 
         for case in switch(v):
             if case():
                 print("setup default values")
             
             if case('Mutual'):
                 print("setup as a mutual coupling measurement")
                 self.write(":SYST:PREset")
                 self.write(":DISPlay:ENAB ON") #enable the display updates
                 self.write(":DISPlay:SPLit D1") #activate 1 channel
                 self.write(":DISPlay:WIND1:SPLit D1_2_3_4") # split window into 4 displays
                 self.write(":DISPlay:WIND1:ACT") # activate chanel 1
                 self.write("CALC:PAR:COUN 4")     #set amount of traces
                 self.write(":DISPlay:WIND1:TRAC1:STAT ON") #activate trace 1
                 self.write("CALCulate:PARameter:DEF S11" ) #set to S11
                 self.write(":DISPlay:WIND1:TRAC2:STAT ON") #activate trace 2
                 self.write("CALCulate:PARameter2:DEF S12") #set to S12
                 self.write(":DISPlay:WIND1:TRAC3:STAT ON") #activate trace 3
                 self.write("CALCulate:PARameter3:DEF S21") #set to S21
                 self.write(":DISPlay:WIND1:TRAC4:STAT ON") #activate trace 4
                 self.write("CALCulate:PARameter4:DEF S22") #set to S22
                 self.write(":SENS1:FREQ:STAR 1E3") #set start freq
                 self.write(":SENS1:FREQ:STOP 100E6") #sets stop freq
                 self.write(":SENS1:SWE:POIN 1601") #sets amount of freq points
                 self.write(":DISP:WIND1:TRAC1:Y:AUTO") #auto scales Y-axis trace1
                 self.write(":DISP:WIND1:TRAC2:Y:AUTO") #auto scales Y-axis trace2
                 self.write(":DISP:WIND1:TRAC3:Y:AUTO") #auto scales Y-axis trace3
                 self.write(":DISP:WIND1:TRAC4:Y:AUTO") #auto scales Y-axis trace4
                 self.write(":SOUR1:POW 10") #Power on port: -45 to 10 dbm. specify in dbm
    
    
    def ENA(): #program does nothing as written
    print("Happy Birthday to you!")
    print("Happy Birthday to you!")
    print("Happy Birthday, dear Emily.")
    print("Happy Birthday to you!")
    
    

    
    
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False