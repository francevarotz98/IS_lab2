import random as rd

# Gets the complement of the binary given as input
def get_complement(bin_string):
    complement = ''
    for x in bin_string :
        if ( x == '0' ):
            complement += '1'
        else :
            complement += '0'
    return complement

# Performs the encoding of our 3 bit word
def rand_binning_enc(mex_u):
    
    # The prefix of the codeword is this
    prefix = '0' + mex_u

    # Calculating the corresponding codeword
    codeword = prefix + ham_code[prefix]
    
    # Two choices, 1/2 probability ti have the initial one, and 1/2 for the complement 
    choise = rd.random()
    if ( choise < 0.5 ) :
        return codeword

    return get_complement(codeword)


# Generate only once the table that works with all the inputs

ham_code = {}
ham_code['0000'] = '000'
ham_code['0100'] = '101'
ham_code['0010'] = '011'
ham_code['0001'] = '111'
ham_code['0110'] = '110'
ham_code['0101'] = '010'
ham_code['0011'] = '100'
ham_code['0111'] = '001'



if __name__ == '__main__':
    
    word = '001'
    print(rand_binning_enc(word))
