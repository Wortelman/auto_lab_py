# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:59:11 2017

@author: Niek
"""
import niek_functions as n
import matplotlib.pyplot as plt

naam = 'singlePhase'

obj1 = n.ENA(); # creation of ENA object
obj1.setup_display('First')
n.time.sleep(1)
obj1.setup_display('Mutual')
n.time.sleep(1)

[A,f]=obj1.measure_Spar()
plt.loglog(f,abs(n.meas2comp(A[:,:,4],A[:,:,5])))
plt.show()

obj1.write_touchtone(A,f,naam+'_Spar')

M = n.Mutual_coupling(f,A,50)
plt.loglog(f, M)
plt.show()
obj1.write_csv(M,f,naam+'_mut')

n.time.sleep(2)
[Matrix,f] = obj1.measure_Zpar("2") # input is the port number in a string
plt.loglog(f,Matrix[:, :, 0])
plt.show()
obj1.write_csv(Matrix,f,naam+'_imp')

# Two subplots, the axes array is 1-d
fx, axarr = plt.subplots(3, sharex=True)
axarr[0].loglog(f,abs(n.meas2comp(A[:,:,4],A[:,:,5])))
axarr[0].set_title('Sharing X axis')
axarr[1].loglog(f, M)
axarr[2].loglog(f,Matrix[:, :, 1])
plt.show()

#
# [Matrix2,f2] = obj1.measure_Zser("1") # input is the port number in a string
# plt.semilogx(f2,Matrix2[:,:,1])
# plt.show()
#obj1.write_touchtone(A,f,"measurements/3phase_center")

# obj1.write_csv(Matrix,f,"geenideeofhetwerkt2")
# plt.interactive(False)
