import random

# CRC lookup tables for various CRC types
POLYNOMIALS = {
    "CRC-4": "11111",
    "CRC-8": "111010101",
    "CRC-16": "1100000000000101",
    "CRC-16R": "1010000000000011",
    "CRC-24": "1100000000101000100000001",
    "CRC-32": "10000100110000010001110110110111"
}

# These samples were generated using Random library: 
#     ''.join(random.choice('01') for _ in range(48)),
# and corresponding crc_type were also generated using:
#     print("(\"{}\", \"{}\")".format(i, random.choice(list(POLYNOMIALS.keys()))))
SAMPLES = [
    ("010101001011100111000111000000110100100110101110", "CRC-4"),
    ("110011101000011100110100101100011011110100110000", "CRC-16"),
    ("100010101001001101110001100000000000010000001101", "CRC-16"),
    ("000101110111101000001000100101110000110110000110", "CRC-32"),
    ("000101111101110000010001111101000010111010010110", "CRC-16"),
    ("000011101000011111000001111110110000011100001100", "CRC-4"),
    ("001110011110110111110000001010101011110100000010", "CRC-4"),
    ("011111011111001110000011011101100001001111001100", "CRC-16"),
    ("100101011110101011111110001000111000000100001000", "CRC-4"),
    ("101011111010100111111010010000111001101111001101", "CRC-8")
]

def xor(a, b):
    results = []
 
    # start from bit 1 to the last bit
    for i in range(1, len(a)):
        # xor operation
        if a[i] == b[i]:
            results.append('0')
        else:
            results.append('1')
 
    # create string from list of bits
    return ''.join(results)


def mod2div(dividend, divisor):
    p = len(divisor)
    selected_dividend = dividend[:p]

    while (p < len(dividend)):
        if (selected_dividend[0] == '1'):
            selected_dividend = xor(selected_dividend, divisor) + dividend[p]
        else:
            selected_dividend = xor(selected_dividend, '0' * p) + dividend[p]
        
        p += 1

    return xor(selected_dividend, (divisor if (selected_dividend[0] == '1') else ('0' * p)))


def generator(dataword, word_size, crc_type):
    if (crc_type not in POLYNOMIALS):
        raise ValueError("Unsupported crc_type: {}".format(crc_type))
    
    divisor = POLYNOMIALS[crc_type]
    dividend = dataword + ('0' * (len(divisor) - 1))
    return mod2div(dividend, divisor)


def checker(codeword, crc_type):
    if (crc_type not in POLYNOMIALS):
        raise ValueError("Unsupported crc_type: {}".format(crc_type))

    divisor = POLYNOMIALS[crc_type]
    return mod2div(codeword, divisor)


print("** 10 Correct cases **")
for i, sample in enumerate(SAMPLES):
    dataword = sample[0]
    crc_type = sample[1]
    remainder = generator(dataword, 48, crc_type)
    codeword = dataword + remainder
    print("CASE #{}:".format(i+1))
    print("\tDataword: {}".format(dataword))
    print("\tCRC-Type: {}".format(crc_type))
    print("\tRemainder: {}".format(remainder))
    print("\tCodeword: {}".format(codeword))
    print("\tSyndrome: {}".format(checker(codeword, crc_type)))

print("** 2 erroneous codewords cases **")
for i, sample in enumerate(SAMPLES[:2]):
    dataword = sample[0]
    crc_type = "CRC-4"
    remainder = generator(dataword, 48, crc_type)
    codeword = dataword + remainder
    error_codeword = ''.join(['0' if bit == '1' else '1' for bit in codeword[:4]]) + codeword[4:]
    print("ERROR CASE #{}:".format(i+1))
    print("\tDataword: {}".format(dataword))
    print("\tCRC-Type: {}".format(crc_type))
    print("\tRemainder: {}".format(remainder))
    print("\tCodeword: {}".format(codeword))
    print("\tSimulated error codeword: {}".format(error_codeword))
    print("\tSyndrome: {}".format(checker(error_codeword, crc_type)))