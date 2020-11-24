from task2 import *
from uniform_error_channel import *
from decoder import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

possible_u = ['000', '001', '010', '011', '100', '101', '110', '111']
arrZ=[None]*8
arrY=[None]*8
arrZ_unique=[0]*128

for i in range(8):
    arrZ[i]=[0]*128 

for i in range(8):
    arrY[i]=[0]*128


for i in range(8):
    u=possible_u[i]
    for j in range(10000):
        x=rand_binning_enc(u)
        y,z=uniform_error_wiretap_channel(x)
        arrZ[i][z] +=1
        arrY[i][y] +=1
        arrZ_unique[z] +=1

print("End for")
#print(arrZ_unique)

#We derive the probability dividing each numbers in arrZ_unique[i] by the total repetitions (80000)
for i in range (128):
    arrZ_unique[i]=arrZ_unique[i]/(10000*8)

#We derive the probability dividing each numbers in arrZ[i][j] and in arrY[i][j] by the total repetitions (10000)
for i in range(8):
    for j in range(128):
        arrZ[i][j] = arrZ[i][j]/10000
        arrY[i][j] = arrY[i][j]/10000

fig1 = plt.figure(1)
plt.plot(arrZ_unique, 'ro', markersize=8)
plt.xlabel('z')
plt.ylabel('p(z)')
fig1.suptitle('pmd of z')
plt.xlim([0,128])
plt.ylim([0,0.1])
#plt.show()

fig, axs = plt.subplots(4, 2)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=1.1)

axs[0, 0].plot(arrZ[0], 'ro', markersize=2)
axs[0, 0].set_title('P(z | u=000)')

axs[0, 1].plot(arrZ[1], 'bo', markersize=2)
axs[0, 1].set_title('P(z | u=001)')

axs[1, 0].plot(arrZ[2], 'go', markersize=2)
axs[1, 0].set_title('P(z | u=010)')

axs[1, 1].plot(arrZ[3], 'co', markersize=2)
axs[1, 1].set_title('P(z | u=011)')

axs[2, 0].plot(arrZ[4], 'ko', markersize=2)
axs[2, 0].set_title('P(z | u=100)')

axs[2, 1].plot(arrZ[5], 'mo', markersize=2)
axs[2, 1].set_title('P(z | u=101)')

axs[3, 0].plot(arrZ[6], 'yo', markersize=2)
axs[3, 0].set_title('P(z | u=110)')

axs[3, 1].plot(arrZ[7], 'ro', markersize=2)
axs[3, 1].set_title('P(z | u=111)')

for i in range(4):
    for j in range(2):
        axs[i, j].set_xlim(0,128)
        axs[i, j].set_ylim(0,0.08)

plt.show()

