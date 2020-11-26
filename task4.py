from task2 import *
from uniform_error_channel import *
from decoder import *
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math

# Variables that define the dimensions of the spaces
message_space = 8
code_word_space = 128

# Creation of the dict that contains the joint probabilities
joint_probability = {}
for u in range(message_space):
    for z in range(code_word_space) :
        joint_probability[f"{u,z}"] = 0


# Calculation of the different probabilities
possible_u = ['000', '001', '010', '011', '100', '101', '110', '111']
iterations = 10000

arrZ=[None]*message_space
arrY=[None]*message_space
arrZ_unique=[0]*code_word_space

for i in range(message_space):
    arrZ[i]=[0]*code_word_space 
    arrY[i]=[0]*code_word_space
    

for i in range(message_space):
    u=possible_u[i]
    for j in range(iterations):
        x=rand_binning_enc(u)
        y,z=uniform_error_wiretap_channel(x)
        arrZ[i][z] +=1
        arrY[i][y] +=1
        arrZ_unique[z] +=1
        joint_probability[f"{i,z}"] += 1

#print("End for")
#print(arrZ_unique)

#We derive the probability dividing each numbers in arrZ_unique[i] by the total repetitions (80000)
for i in range (code_word_space):
    arrZ_unique[i]=arrZ_unique[i]/(iterations*message_space)

#We derive the probability dividing each numbers in arrZ[i][j] and in arrY[i][j] by the total repetitions (10000)
for i in range(message_space):
    for j in range(code_word_space):
        arrZ[i][j] = arrZ[i][j]/iterations
        arrY[i][j] = arrY[i][j]/iterations

fig1 = plt.figure(1)
plt.plot(arrZ_unique, 'ro', markersize=message_space)
plt.xlabel('z')
plt.ylabel('p(z)')
fig1.suptitle('pmd of z')
plt.xlim([0,code_word_space])
plt.ylim([0,0.1])
#plt.show()

fig, axs = plt.subplots(4, 2)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=1.1)

axs[0, 0].plot(arrZ[0], 'ro', markersize=2)
axs[0, 0].set_xlabel('z')
axs[0, 0].set_title('P(z | u=000)')

axs[0, 1].plot(arrZ[1], 'bo', markersize=2)
axs[0, 1].set_xlabel('z')
axs[0, 1].set_title('P(z | u=001)')

axs[1, 0].plot(arrZ[2], 'go', markersize=2)
axs[1, 0].set_xlabel('z')
axs[1, 0].set_title('P(z | u=010)')

axs[1, 1].plot(arrZ[3], 'co', markersize=2)
axs[1, 1].set_xlabel('z')
axs[1, 1].set_title('P(z | u=011)')

axs[2, 0].plot(arrZ[4], 'ko', markersize=2)
axs[2, 0].set_xlabel('z')
axs[2, 0].set_title('P(z | u=100)')

axs[2, 1].plot(arrZ[5], 'mo', markersize=2)
axs[2, 1].set_xlabel('z')
axs[2, 1].set_title('P(z | u=101)')

axs[3, 0].plot(arrZ[6], 'yo', markersize=2)
axs[3, 0].set_xlabel('z')
axs[3, 0].set_title('P(z | u=110)')

axs[3, 1].plot(arrZ[7], 'ro', markersize=2)
axs[3, 1].set_xlabel('z')
axs[3, 1].set_title('P(z | u=111)')

for i in range(4):
    for j in range(2):
        axs[i, j].set_xlim(0,code_word_space)
        axs[i, j].set_ylim(0,0.08)

#plt.show()


# Calculation of the joint probability based on the dict defined above
for u_z in joint_probability :
    joint_probability[u_z] = joint_probability[u_z] / (iterations * message_space)

#print(joint_probability)

# Uniform for obvoious reasons
prob_u = 1 / message_space
 
# I expected the distribution to be uniform,
# the values is costant so I don't need to repeat the calculations, it doesnt depend on u
prob_z = 0
for x in arrZ[0] :
    prob_z += x


# Do the average to take a more stable value
prob_z = prob_z/code_word_space


#  The joint probability can be calculated as the product between the conditional probability and the probability of the conditioning event
Iuz = 0
for u in range(message_space) :
    for z in range(code_word_space) :
        Iuz += joint_probability[f"{u,z}"] * math.log2(joint_probability[f"{u,z}"] /(prob_u * prob_z))

print(f"The mutual information is : {Iuz}")

plt.show()

