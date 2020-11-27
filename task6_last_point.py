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
    epsilon_arr = np.linspace(0,1,num=15) # start,end,numbers
    delta_arr = epsilon_arr

    iter = 2000
    prob_correct = [0]*len(epsilon_arr) # array which will contain the probability the legitimate word is correctly decoded using iter iterations
    mut_inf_arr = [0]*len(epsilon_arr)
    pair_arr = [0]*len(epsilon_arr)

    max_upperbound_disting = -1
    dist_matrix = []

    for i in range(0,len(epsilon_arr)):
        #fix epsilon
        epsilon = epsilon_arr[i]
        row_matrix = []
        for k in range(0,len(epsilon_arr)):
            #fix delta
            delta = delta_arr[k]
            pair = {}
            count_u = {}
            corr_err_u = {}#this will be a dict like this : {'101': [2, 3], '000': [1, 2]}, where, for example, word 101 is correctly decoded twice and uncorrectly three times
            count_z = {}
            correct_leg = {}
            for j in range(iter):
                word = word_arr[np.random.randint( low=0, high=len(word_arr) )]

                #encoding
                enc_word = rand_binning_enc(word)

                #channel
                channel_word = wiretapBSC_channel(epsilon,delta,enc_word)
                leg_word = channel_word[0]
                eave_word = channel_word[1]

                #decoding
                dec_leg = rand_binning_dec(leg_word)


                if not((word,eave_word) in pair):
                    pair[(word,eave_word)] = 1
                else :
                    pair[(word,eave_word)]+=1
                ########################
                #is the word correctly decoded by the receiver?
                if not(word in corr_err_u):
                    if(word == dec_leg):
                        corr_err_u[word] = [1,0]
                    else:
                        corr_err_u[word] = [0,1]
                else:
                    if(word == dec_leg):
                        corr_err_u[word][0]+=1
                    else:
                        corr_err_u[word][1]+=1
                #########################
                count_z.setdefault(eave_word,0)
                count_z[eave_word] += 1

                #########################
                count_u.setdefault(word,0)
                count_u[word] +=1


            # calculation of I(u;z)
            mutual_inf_uz = 0

            for p in pair:
                joint_prob = pair[p]/iter
                u = p[0]
                z = p[1]
                prob_u = count_u[u]/iter
                prob_z = count_z[z]/iter
                log = math.log(joint_prob/(prob_u*prob_z),2)
                mutual_inf_uz += joint_prob*log

            mut_inf_arr[k] = mutual_inf_uz


            #calculation of P(u~ =/= u | u = a)
            # >>>>> Now, in corr_err_u, I put the error probability instead of the number of times the word u is correctly or not decoded
            for u in corr_err_u:
                corr_err_u[u] = 1-(corr_err_u[u][0]/(corr_err_u[u][0]+corr_err_u[u][1]))

            #Let's calculate the max security upper bound I can have for THIS iteration

            max_key_u = max(corr_err_u,key=corr_err_u.get)
            max_value_u = corr_err_u[max_key_u]
            row_matrix.append(max_value_u+0.5*math.sqrt(mut_inf_arr[k]))

        dist_matrix.append(row_matrix)

    # -------------------- END for -------------------------
    print('\nmut_inf_arr :',mut_inf_arr,'\n','-'*35)
    print('\n\n',dist_matrix)

    #  >>>>> point 2.3.6 <<<<<<
    fig = plt.figure()
    CS = plt.contourf(delta_arr,epsilon_arr,dist_matrix,cmap = plt.get_cmap('rainbow'))
    plt.xlabel(r'$\delta$')
    plt.ylabel(r'$\epsilon$')
    fig.suptitle('Security distinguishability as function of '+r'$\epsilon$ '+'and '+r'$\delta$ ')

    fig.colorbar(CS,shrink=0.8)
    plt.show()
