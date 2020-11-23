import numpy as np
import uniform_error_channel as t1
import task2 as t2

# H is the parity check matrix
H = np.array([[1, 1, 0, 1, 1, 0, 0],
              [1, 0, 1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0, 0, 1]], dtype='i1')

# (syndrome, coset leader) look-up table. the value at row i corresponds to the coset leader of the syndrome i
coset_leader = np.array([[0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0, 1, 0],
                         [0, 0, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0]], dtype='i1')

# accepts as input a string of 7 bits that represents the received sequence of Bob
# returns a string of 3 bits that represents the decoded message


def rand_binning_dec(input):

    input = np.array([1 if x == '1' else 0 for x in input], dtype='i1')

    # compute the syndrome of the received word
    s = np.dot(H, input) % 2

    # convert the syndrome in dec
    s = s[0]*4 + s[1]*2 + s[2]

    codeword = (input + coset_leader[s]) % 2
    # print(codeword)

    if codeword[0] == 0:
        # u is the decoded message
        u = codeword[1:4]
    else:
        # take the complement of the bits in pos. 2,3,4
        u = ([1, 1, 1] + codeword[1:4]) % 2

    # produce the bitstring (for simmetry, the input was a bitstring)
    out = ''
    for bit in u:
        out += str(bit)

    return out


if __name__ == '__main__':

    # number of cycles through the message space
    N = 3
    # message space
    test = ['000', '001', '010', '011', '100', '101', '110', '111']
    err1, err2 = 0, 0

    for i in range(N * len(test)):

        u = test[i % len(test)]

        # encode the message
        x = t2.rand_binning_enc(u)

        # decode the message directly w/o passing through the channel
        u_hat = rand_binning_dec(x)

        print("enc -> dec: ", u, " -> ", u_hat)

        if u != u_hat:
            err1 += 1

    for i in range(N * len(test)):

        u = test[i % len(test)]

        # encode the message
        x = t2.rand_binning_enc(u)

        # simulate tx over uniform channel
        y, z = t1.uniform_error_wiretap_channel(x)  # returns int values
        y = "{:7b}".format(y)

        # decode the message received from Bob
        u_hat = rand_binning_dec(y)

        print("A -> B    : ", u, " -> ", u_hat)
        if u != u_hat:
            err2 += 1

    print("errors on the encoder/decoder chain: ", err1)
    print("errors over the channel: ", err2)
