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

[A,f]=obj1.measure_Spar()
plt.semilogx(f,abs(A[:,:,1]))
plt.show()


# [Matrix,f] = obj1.measure_Zpar("2") # input is the port number in a string
# plt.semilogx(f,Matrix[:,:,1])
# plt.show()

# Two subplots, the axes array is 1-d
# fx, axarr = plt.subplots(2, sharex=True)
# axarr[0].loglog(f, Matrix[:,:,1])
# axarr[0].set_title('Sharing X axis')
# axarr[1].loglog(f, Matrix[:,:,2])
#plt.show()

#
# [Matrix2,f2] = obj1.measure_Zser("1") # input is the port number in a string
# plt.semilogx(f2,Matrix2[:,:,1])
# plt.show()
#obj1.write_touchtone(A,f,"measurements/3phase_center")

# obj1.write_csv(Matrix,f,"geenideeofhetwerkt2")
# plt.interactive(False)
