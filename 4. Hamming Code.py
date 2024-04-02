# This function translates the input dataword from ASCII text to 8 bits of binary. After
# removing the most significant bit (most left), there will be 7 bits. From these 7 bits,
# calculates the redundancy bit(s) for the dataword and output the 11-bit codeword for Hamming code.
def generator(dataword):
    # dataword: Dataword, which is an alphabet letter (a-z, A-Z)
    # Output: A codeword based on Hamming code
    pass

# This function verifies the Hamming codeword 
# and report the location of error for the case of single bit error.
def checker(codeword):
    # codeword: A 11-bit codeword as such 1100100110.
    # Output: Position of error (in case of a single bit error, but return 0 if there is no error found)
    pass