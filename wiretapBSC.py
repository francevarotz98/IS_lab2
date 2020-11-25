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

    iter = 1000
    prob_correct = [0]*len(epsilon_arr) # array which will contain the probability the legitimate word is well decrypted using iter iterations
    prob_eaves = [0]*len(epsilon_arr)
    #print('Input :',word,' <---> epsilon :',epsilon,' <---> delta :',delta)
    correct_leg = 0
    correct_eav = 0
    count_pair = 0
    pair_arr = [0]*len(epsilon_arr)

    pair = {} # all the pairs (u,z) will be inserted here as value and as key number of times counted
    for i in range(0,len(epsilon_arr)):
        epsilon = epsilon_arr[i]
        delta = delta_arr[i]
        word = word_arr[np.random.randint( low=0, high=len(word_arr))]
        for j in range(iter):
            enc_word = rand_binning_enc(word)
            #print('[+] Encoded word :',enc_word)
            channel_word = wiretapBSC_channel(epsilon,delta,enc_word)
            leg_word = channel_word[0]
            eave_word = channel_word[1]
            #print('[+] Encoded Word legitimate channel :',leg_word)
            #print('[+] Encoded Word eavesdropper channel :',eave_word)
            dec_leg = rand_binning_dec(leg_word)
            dec_eav = rand_binning_dec(eave_word)
            #print('[+] Decrypted legitimate word :',dec_leg)
            #print('[+] Decrypted eavesdropper word :',dec_eav)
            if dec_leg == word:
                correct_leg += 1
            if dec_eav == word:
                correct_eav += 1
            #if (word == '110') and (dec_eav == '001'):
            #    count_pair += 1
            if not((word,dec_eav) in pair):
                pair[(word,dec_eav)] = 1
            else :
                pair[(word,dec_eav)]+=1
        prob_correct[i] = correct_leg/iter
        prob_eaves[i] = correct_eav/iter
        pair_arr[i] = count_pair
        correct_leg = 0
        correct_eav = 0
        #count_pair = 0

    print('Probability correct legitimate :',prob_correct)
    #print(len(pair))
    print(pair)

    #Calculating I(u;z)
    mutual_inf_uz = 0
    for p in pair :
        #print(p)
        joint_prob = pair[p]/(iter*len(epsilon_arr))
        log = math.log(joint_prob*64,2) #pu(u)=pz(z)=1/8
        tmp = joint_prob*log
        mutual_inf_uz += tmp

    print(mutual_inf_uz)
    #print('Pair times :',pair_arr)
    #total_times_pair = 0
    #for i in pair_arr:
    #    total_times_pair+= i
    #joint_prob = total_times_pair/(iter*len(epsilon_arr))
    #print('\nJoint probability u, z :',joint_prob)
    #plot probability correctness varying epsilon
    fig = plt.figure()
    plt.scatter(epsilon_arr,prob_correct)
    plt.xlabel('Epsilon')
    plt.ylabel('Correctness')
    fig.suptitle('Correctness legtimate decryption varying epsilon')
    #plt.show()
