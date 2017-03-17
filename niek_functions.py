# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:57:50 2017

@author: Niek
#"""
import visa
import numpy as np
import time


            
            
class ENA(object):
    rm = visa.ResourceManager()

    def __init__(self): 
           print(ENA.rm.list_resources())
           a = ENA.rm.list_resources()
           if ('USB0::0x0957::0x1309::MY49406990::INSTR' in a): #check if the ENA is connected
               print('ENA E5061B Detected')
           else:
               print('ENA E5061B not Detected')
               raise ValueError
           
    
    def connect():
        self = ENA.rm.open_resource('USB0::0x0957::0x1309::MY49406990::0::INSTR')
        self.read_termination = '\n'
        self.write_termination = '\n'
        return self
    
    
    def setup(self,v):
        self  = ENA.connect()
        for case in switch(v):
                    
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
                 
             elif case():
                 print("setup default values")
                 
             return self
             
    def measure_Spar(self):
        self  = ENA.connect()
        self.write(":DISP:WIND1:TRAC1:Y:AUTO") #auto scales Y-axis trace1
        self.write(":DISP:WIND1:TRAC2:Y:AUTO") #auto scales Y-axis trace2
        self.write(":DISP:WIND1:TRAC3:Y:AUTO") #auto scales Y-axis trace3
        self.write(":DISP:WIND1:TRAC4:Y:AUTO") #auto scales Y-axis trace4
        freq = np.fromstring(self.query("SENS1:FREQ:DATA?"),dtype=float,sep=',')    
        self.write(":CALC1:PAR1:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"),dtype=float,sep=',')
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
        return C, freq
    
    def measure_Zpar(self,port):
        self = ENA.connect()
        ENA.imp(self, "1", "S11", "P"+port+"R", "Z",'MLOG')
        ENA.imp(self, "2", "S11", "P"+port+"R", "CP",'MLIN')
        ENA.imp(self, "3", "S11", "P"+port+"R", "LP",'MLIN')
        ENA.imp(self, "4", "S11", "P"+port+"R", "Z",'PHASE')
        time.sleep(2)
        [data,f]=ENA.get_data(self)
        return data,f

    def measure_Zser(self,port):
        self = ENA.connect()
        ENA.imp(self, "1", "S11", "P"+port+"R", "Z",'MLOG')
        ENA.imp(self, "2", "S11", "P"+port+"R", "Cs",'MLIN')
        ENA.imp(self, "3", "S11", "P"+port+"R", "Ls",'MLIN')
        ENA.imp(self, "4", "S11", "P"+port+"R", "Z",'PHASE')
        time.sleep(2)
        [data,f]=ENA.get_data(self)
        return data,f

    def imp(self,trace,port,refl,zpara,form):
        self = ENA.connect()
        self.write(":CALC1:PAR"+trace+":SEL")
        self.write(":CALC1:PAR" + trace + ":DEF " + port ) #(S11,S22,S21 or S12)
        self.write(":SENS:Z:METH " + refl ) #(P1Reflection or "P2Reflection", "TSERies", "TSHunt")
        self.write(":CALC1:PAR"+trace+":DEF Z") #
        self.write(":CALC1:SEL:ZPAR:DEF " + zpara )
        self.write(":CALC1:SEL:FORM " + form) #NOT sure if auto selection is ok?
        self.write(":DISP:WIND1:TRAC"+trace+":Y:AUTO")  # auto scales Y-axis trace1

    def get_data(self):
        freq = np.fromstring(self.query("SENS1:FREQ:DATA?"), dtype=float, sep=',')
        self.write(":CALC1:PAR1:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"), dtype=float, sep=',')
        S11 = np.resize(tmp, (1601, 2))
        self.write(":CALC1:PAR2:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"), dtype=float, sep=',')
        S12 = np.resize(tmp, (1601, 2))
        self.write(":CALC1:PAR3:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"), dtype=float, sep=',')
        S21 = np.resize(tmp, (1601, 2))
        self.write(":CALC1:PAR4:SEL")
        tmp = np.fromstring(self.query(":CALC1:DATA:FDAT?"), dtype=float, sep=',')
        S22 = np.resize(tmp, (1601, 2))
        A = np.transpose(np.dstack([S11, S12]), axes=[0, 2, 1])
        B = np.transpose(np.dstack([S21, S22]), axes=[0, 2, 1])
        C = np.resize(np.hstack([A, B]), (1601, 1, 8))
        return C, freq


    def write_csv(self,Z,freq,m_str):
#        now = time.strftime("%c")
#        name = m_str + "csv"
        print('to be created')
    
        
    def write_touchtone(self,C,freq,m_str):
        now = time.strftime("%c")
        name = m_str + ".s2p"
        with open(name, 'w') as f:
            f.write('! TOUCHSTONE file generated by Niek Moonen Python script \n')
            f.write('! Current date & time %s \n' % now)
            f.write('! Project name: \n')
            f.write('! Header version: jan 2017 \n')
            f.write('! Port assignment regex:  !\s*Touchstone port\s*([0-9]+)\s*=\s*CST MWS port\s*([0-9]+)\s*\(\"(.*)\"\)(\s*mode\s*([0-9]+))?.* \n')
            f.write('! Touchstone port assignment: \n')
            f.write('! Touchstone port 1 = ENA E5061B port 1 ("") \n')
            f.write('! Touchstone port 2 = ENA E5061B port 2 ("") \n')
            f.write('# HZ S MA R 50 \n')
        with open(name,'ab') as f:
            i=-1
            for slice_2d in C:        
                i=i+1
                somestring = repr(freq[i])
                f.write(somestring.encode('ascii'))
                f.write(b'\t\t')
                np.savetxt(f, slice_2d, delimiter="\t ", fmt='%e',newline='\r\n')

#place holders for future equipment to be added
class ESS(object): 
    rm = visa.ResourceManager()

    def __init__(self): 
           print(ENA.rm.list_resources())
           a = ENA.rm.list_resources()
           if ('' in a): #check if the ENA is connected
               print('ENA E5061B Detected')
           else:
               print('ENA E5061B not Detected')
               raise ValueError

class LCR(object):
    rm = visa.ResourceManager()
    
class WGEN(object):
    rm = visa.ResourceManager()
    
class MM(object):
    rm = visa.ResourceManager()
##################################################

         










# additional classes    
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

    

    
    
