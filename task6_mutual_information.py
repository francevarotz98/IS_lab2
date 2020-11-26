from encoder import *
from decoder import *
import random
import matplotlib.pyplot as plt
import numpy as np
import math

def wiretapBSC_channel(epsilon,delta,input):
    '''
    epsilon = error rates legitimate channel. Number in [0,1]
    delta = error rates eavesdropper channel. Number in [0,1]
    input = encoded word. It is a str of seven binary digits
    return = the outputs for B and E
    '''
    #creation of the legitimate word through the BSC channel given epsilon
    leg_word = ''
    for d in input:
        r = random.random()
        if( r < epsilon ): # no error (think about epsilon = 0.7 and epsilon = 0.2 : it is more probable that
            leg_word += d  #  r is less than epsilon = 0.7 than equal to 0.2)
        else :
            leg_word += get_complement(d)


    eave_word = ''
    for d in input:
        r = random.random()
        if( r < delta ): #no error
            eave_word += d
        else :
            eave_word += get_complement(d)

    return leg_word,eave_word


if __name__ == '__main__':

    word_arr = ['000','001','010','011','100','101','110','111']
    epsilon_arr = [0,0.1,0.15,0.18,0.2,0.26,0.3,0.35,0.4,0.45,0.5,0.53,0.6,0.67,0.7,0.73,0.82,0.9,0.95,1] # long: 20
    delta_arr = epsilon_arr

    iter = 15000
    prob_correct = [0]*len(epsilon_arr) # array which will contain the probability the legitimate word is well decrypted using iter iterations
    prob_eaves = [0]*len(epsilon_arr)
    mut_inf_delta = [0]*len(epsilon_arr)

    pair_arr = [0]*len(epsilon_arr)

    for i in range(0,len(epsilon_arr)):
        epsilon = epsilon_arr[i]
        delta = delta_arr[i]
        real_pair = 0 # num pairs which will be really extracted on each iterations (useful to count the probability of z (pz))
        pair = {}
        count_u = {}
        count_z = {}
        for j in range(iter):
            word = word_arr[np.random.randint( low=0, high=len(word_arr) )]
            enc_word = rand_binning_enc(word)
            channel_word = wiretapBSC_channel(epsilon,delta,enc_word)
            leg_word = channel_word[0]
            eave_word = channel_word[1]

            if not((word,eave_word) in pair):
                pair[(word,eave_word)] = 1
                real_pair+=1
            else :
                if pair[(word,eave_word)] == 0:
                    real_pair += 1
                pair[(word,eave_word)]+=1
            ########################
            if not(word in count_u):
                count_u[word] = 1
            else:
                count_u[word]+=1
            #########################
            if not(eave_word in count_z):
                count_z[eave_word] = 1
            else:
                count_z[eave_word]+=1

        mutual_inf_uz = 0


        for p in pair:
            joint_prob = pair[p]/iter
            u = p[0]
            z = p[1]
            prob_u = count_u[u]/iter
            prob_z = count_z[z]/iter
            log = math.log(joint_prob/(prob_u*prob_z),2)
            mutual_inf_uz += joint_prob*log



        mut_inf_delta[i] = mutual_inf_uz
    print('\nmut_inf_delta :',mut_inf_delta,'\n----------------------------------')



    #  >>>>> point 2.3.5 <<<<<<
    fig = plt.figure()
    plt.scatter(delta_arr,mut_inf_delta)
    plt.xlabel('Delta')
    plt.ylabel('Mutual information')
    fig.suptitle('Mutual information as function of delta')
    plt.show()
