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
    rm = visa.ResourceManager()
   
    
    def __init__(self): 
#           rm = visa.ResourceManager()
           print(ENA.rm.list_resources())
           
#           self = rm.open_resource('USB0::0x0957::0x1309::MY49406990::0::INSTR')
#           self.read_termination = '\n'
#           self.write_termination = '\n'
#           print(self.query("*IDN?"))
#           return self
    
    def connect():
        self = ENA.rm.open_resource('USB0::0x0957::0x1309::MY49406990::0::INSTR')
        self.read_termination = '\n'
        self.write_termination = '\n'
        return self
    
    
    def setup(self,v):
        self  = ENA.connect()
        for case in switch(v):
#             rm = visa.ResourceManager()
#             self = ENA.rm.open_resource('USB0::0x0957::0x1309::MY49406990::0::INSTR')
#             self.read_termination = '\n'
#             self.write_termination = '\n'
#             print(self.query("*IDN?"))
             
             
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
                 self.write(":CALC1:PAR1:SEL")
                 self.write(":CALC1:FORM SLIN") #smith chart! linear mag and phase
                 self.write(":CALC1:PAR2:SEL") 
                 self.write(":CALC1:FORM SLIN") #smith chart! linear mag and phase
                 self.write(":CALC1:PAR3:SEL")
                 self.write(":CALC1:FORM SLIN") #smith chart! linear mag and phase
                 self.write(":CALC1:PAR4:SEL")
                 self.write(":CALC1:FORM SLIN") #smith chart! linear mag and phase
                 self.write(":DISP:WIND1:TRAC1:Y:AUTO") #auto scales Y-axis trace1
                 self.write(":DISP:WIND1:TRAC2:Y:AUTO") #auto scales Y-axis trace2
                 self.write(":DISP:WIND1:TRAC3:Y:AUTO") #auto scales Y-axis trace3
                 self.write(":DISP:WIND1:TRAC4:Y:AUTO") #auto scales Y-axis trace4
                 
             if case('df'):
                 print("setup default values")
                 
             return self
             
    def measure(self):
        self  = ENA.connect()
#        self = rm.open_resource('USB0::0x0957::0x1309::MY49406990::0::INSTR')
#        self.read_termination = '\n'
#        self.write_termination = '\n'
#        time.sleep(5)
        freq = np.fromstring(self.query("SENS1:FREQ:DATA?"),dtype=float,sep=',')    
        self.write(":CALC1:PAR1:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"),dtype=float,sep=',')
        S11 = np.resize(np.resize(tmp,(1601,2)).T,(1,2,1601))
        S11 = np.resize(tmp,(1601,2))
        self.write(":CALC1:PAR2:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"),dtype=float,sep=',')
        S12 = np.resize(tmp,(1601,2))
        self.write(":CALC1:PAR3:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"),dtype=float,sep=',')
        S21 = np.resize(tmp,(1601,2))
        self.write(":CALC1:PAR4:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"),dtype=float,sep=',')
        S22 = np.resize(tmp,(1601,2))
        A = np.transpose(np.dstack([S11,S12]), axes=[0,2,1])
        B = np.transpose(np.dstack([S21,S22]), axes=[0,2,1])
        C = np.resize(np.hstack([A,B]),(1601,1,8))
#        D = np.dstack([C,freq])
#        plt.plot(freq,C[:,2,2])
        return C, freq
        
    def write_touchtone(self,C,freq):
        now = time.strftime("%c")
#        print ("Current time %s"  % now )
        with open('three_phase_2.s2p', 'w') as f:
            f.write('! TOUCHSTONE file generated by Niek Moonen Python script \n')
            f.write('! Current date & time %s \n' % now)
            f.write('! Project name: \n')
            f.write('! Header version: jan 2017 \n')
            f.write('! Port assignment regex:  !\s*Touchstone port\s*([0-9]+)\s*=\s*CST MWS port\s*([0-9]+)\s*\(\"(.*)\"\)(\s*mode\s*([0-9]+))?.* \n')
            f.write('! Touchstone port assignment: \n')
            f.write('! Touchstone port 1 = ENA E5061B port 1 ("") \n')
            f.write('! Touchstone port 2 = ENA E5061B port 2 ("") \n')
            f.write('# HZ S MA R 50 \n')
        with open('three_phase_2.s2p','ab') as f:
            i=-1
            for slice_2d in C:        
                i=i+1
                somestring = repr(freq[i])
                f.write(somestring.encode('ascii'))
                f.write(b'\t\t')
                np.savetxt(f, slice_2d, delimiter="\t ", fmt='%e',newline='\r\n')

         
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

#    
#    def ENA(): #program does nothing as written
#    print("Happy Birthday to you!")
#    print("Happy Birthday to you!")
#    print("Happy Birthday, dear Emily.")
#    print("Happy Birthday to you!")
#    
    

    
    
