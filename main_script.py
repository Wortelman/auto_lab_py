# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:59:11 2017

@author: Niek
"""
import niek_functions as n
import matplotlib.pyplot as plt
obj1 = n.ENA(); # creation of ENA object

#### Only use this part for first setup, since it does a total reset!
#obj1.setup('Mutual') # setup the standard <-- watch out with this, callibration is deleted!!
#n.time.sleep(1) # to fast execution of setup and measure gives error

[A,f]=obj1.measure()
obj1.write_touchtone(A,f,"measurements/naam")


plt.semilogx(f,A[:,:,0])
