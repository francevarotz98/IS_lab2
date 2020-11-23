#task 1 lab. 2
# the input and output alphabets are the set of 7-bit
# words: X = Y = Z = {0; 1}^7
import random
import matplotlib.pyplot as plt
import numpy as np

def uniform_error_wiretap_channel(x):
    '''
    Input : x is a string binary number long 7 bits (e.g. '1001000')

    Output: y and z are string numbers (base 10) long 7 bits each
    
implementation of a wiretap channel s.t.:
  > the legitimate channel introduces at most 1 binary error per word
  > the eavesdropper channel introduces at most 3 binary error per word
  > y and z are conditionally uniform and independent of eache other given x
      so: Pyz|x = Py|x * Pz|x
    '''
    error_legitimate = ['0000000', '0000001', '0000010', '0000100', '0001000', '0010000', '0100000', '1000000']

    #at first error_eavesdropper is equal to error_legitimate, then I complete it adding numbers with two and three 1's
    error_eavesdropper = ['0000000', '0000001', '0000010', '0000100', '0001000', '0010000', '0100000', '1000000']

    tmp_2 = [] # it will contain the numbers with exactly two 1's
    tmp_3 = [] # it will contain the numbers with exactly three 1's

    #generating numbers with exactly two 1's
    for err_leg in error_legitimate:
        for err_eave in error_eavesdropper:
            error_2 = int(err_leg,2) | int(err_eave,2)
            num_1 = 0 # number of ones
            for i in bin(error_2)[2:]:
                if i == '1':
                    num_1 += 1
            if (num_1 == 2) and not(bin(error_2)[2:] in tmp_2):
                tmp_2.append(bin(error_2)[2:])
            num_1 = 0

    for num in tmp_2:
        error_eavesdropper.append(num)

    #generating numbers with exactly three 1's
    for err_leg in error_legitimate:
        for t in tmp_2:
            error_3 = int(err_leg,2) | int(t,2)
            num_1 = 0
            for i in bin(error_3)[2:]:
                if i =='1':
                    num_1+=1
            if (num_1 == 3) and not(bin(error_3)[2:] in tmp_3):
                tmp_3.append(bin(error_3)[2:])

    for num in tmp_3:
        error_eavesdropper.append(num)

    # >>>>>>> Legitimate channel <<<<<<<
                                                                                        #NOTE : the function random.randint() has/should have  a 'uniform behaviour'
    error_y = error_legitimate[ np.random.randint( low=0,high=len(error_legitimate) ) ]#error_y = error_legitimate[random.randint(0,len(error_legitimate))-1]
    y = int(x,2) ^ int(error_y,2)

    # >>>>>>> Eavesdropper channel <<<<<<<
    error_z = error_eavesdropper[ np.random.randint( low=0,high=len(error_eavesdropper) ) ]
    z = int(x,2) ^ int(error_z,2)

    return y,z

#################################################
'''
def generate_rand_input():

    #generate a number (type str) with 7 bits

    input = ''
    for i in range(7):
        input += str(random.randint(0,1))
    return input
'''
#################################################


if __name__ == '__main__':

    x = '1001000'

    print('input :'+x+'\n')

    arrY = [0]*int('1111111',2) #the index is the output number (= y); the value of the index is the number of times it comes out
    arrZ = [0]*int('1111111',2) #the index is the output number (= z); the value of the index is the number of times it comes out


    for i in range(0,10000):
        res = uniform_error_wiretap_channel(x)
        y=res[0]
        z=res[1]

        arrY[y] += 1
        arrZ[z] +=1

    print(arrY)
    print('------------')
    print(arrZ)

    fig = plt.figure()
    plt.plot(arrY)
    plt.xlabel('number')
    plt.ylabel('times')
    fig.suptitle('Number of times y comes out')
    plt.show()

    fig2 = plt.figure()
    plt.plot(arrZ)
    fig2.suptitle('Number of times z comes out')
    plt.xlabel('number')
    plt.ylabel('times')
    plt.show()
