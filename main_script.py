# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:59:11 2017

@author: Niek
"""
import niek_functions as n
import matplotlib.pyplot as plt
obj1 = n.ENA();

object2 = obj1.setup('Mutual')
n.time.sleep(1)
[A,f]=obj1.measure()


plt.semilogx(f,A[:,:,0])

#
##plt.pyplot.semilogx(f,A[:)
#
#plt.