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


fig1 = plt.figure(2)
plt.plot(arrZ_unique, 'ro')
plt.xlabel('z')
plt.ylabel('numbers of times')
fig1.suptitle('z')
plt.xlim([0,128])
plt.ylim([0,10000])
#plt.show()

fig, axs = plt.subplots(4, 2)

axs[0, 0].plot(arrZ[0], 'ro')
axs[0, 0].set_title('z | u=000')

axs[0, 1].plot(arrZ[1], 'bo')
axs[0, 1].set_title('z | u=001')

axs[1, 0].plot(arrZ[2], 'go')
axs[1, 0].set_title('z | u=010')

axs[1, 1].plot(arrZ[3], 'co')
axs[1, 1].set_title('z | u=011')

axs[2, 0].plot(arrZ[4], 'ko')
axs[2, 0].set_title('z | u=100')

axs[2, 1].plot(arrZ[5], 'mo')
axs[2, 1].set_title('z | u=101')

axs[3, 0].plot(arrZ[6], 'yo')
axs[3, 0].set_title('z | u=110')

axs[3, 1].plot(arrZ[7], 'ro')
axs[3, 1].set_title('z | u=111')

for i in range(4):
    for j in range(2):
        axs[i, j].set_xlim(0,128)
        axs[i, j].set_ylim(0,400)

plt.show()

