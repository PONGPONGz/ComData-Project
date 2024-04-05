from functools import reduce

# XOR the whole string/list
def xor(*args):
    return reduce(lambda x, y: int(x) ^ int(y), args)

# This function translates the input dataword from ASCII text to 8 bits of binary. After
# removing the most significant bit (most left), there will be 7 bits. From these 7 bits,
# calculates the redundancy bit(s) for the dataword and output the 11-bit codeword for Hamming code.
# dataword: Dataword, which is an alphabet letter (a-z, A-Z)
# Output: A codeword based on Hamming code
def generator(_dataword):
    dataword = format(ord(_dataword), "08b")[1:]         # string to binary and remove most significant bit
    print("Generating codeword for dataword: {} ({})".format(_dataword, dataword))
    
    # 1000001
    # 100_000_1__
    r1 = xor(dataword[-1], dataword[-2], dataword[-4], dataword[-5], dataword[0])       # 1, 3, 5, 7, 9, 11
    r2 = xor(dataword[-1], dataword[-3], dataword[-4], dataword[-6], dataword[-7])      # 2, 3, 6, 7, 10, 11
    r4 = xor(dataword[-2], dataword[-3], dataword[-4])                                  # 4, 5, 6, 7
    r8 = xor(*dataword[:3])                                                             # 8, 9, 10, 11

    codeword = "{}{}{}{}{}{}{}".format(dataword[:3], r8, dataword[3:6], r4, dataword[-1], r2, r1)
    return codeword

# This function verifies the Hamming codeword 
# and report the location of error for the case of single bit error.
# codeword: A 11-bit codeword as such 1100100110.
# Output: Position of error (in case of a single bit error, but return 0 if there is no error found)
def checker(codeword):
    r1 = xor(*codeword[::-1][::2])
    r2 = xor(codeword[-2], codeword[-3], codeword[-6], codeword[-7], codeword[-10], codeword[-11])
    r4 = xor(*codeword[4:8])
    r8 = xor(*codeword[0:4])

    err_pos = int(str(r8) + str(r4) + str(r2) + str(r1), 2)
    return err_pos


def test():
    codeword = generator('A')
    err_pos = checker(codeword)
    if (err_pos):
        print("Error occured at bit {}".format(err_pos))
    else:
        print("No error present.")

    print("Simulate error at bit 1")
    codeword = codeword[:-1] + str(int(codeword[-1]) ^ 1) 
    err_pos = checker(codeword)
    if (err_pos):
        print("Error occured at bit {}".format(err_pos))
    else:
        print("No error present.")

test()