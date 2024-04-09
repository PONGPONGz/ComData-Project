def crc_remainder(dataword, polynomial):
    """Calculate the CRC remainder using polynomial division."""
    # Append zeros to dataword for polynomial degree - 1 times
    dataword_padded = dataword + '0' * (len(polynomial) - 1)
    data = list(dataword_padded)
    divisor = list(polynomial)
    for i in range(len(dataword)):
        if data[i] == '1':
            for j in range(len(divisor)):
                data[i + j] = str(int(data[i + j]) ^ int(divisor[j]))
    return ''.join(data)[-len(polynomial) + 1:]


def crc_gen(dataword, word_size, crc_type):
    """Generate CRC codeword for an input dataword."""
    # Define CRC polynomials
    crc_polynomials = {
        "CRC-4": "11111",
        "CRC-8": "111010101",
        "CRC-16": "1100000000000101",
        "CRC-16R": "1010000000000011",
        "CRC-24": "1100000000101000100000001",
        "CRC-32": "10000100110000010001110110110111"
    }
    polynomial = crc_polynomials.get(crc_type)
    if polynomial is None:
        raise ValueError("Unsupported CRC type")

    # Calculate CRC remainder
    crc_remainder_bits = crc_remainder(dataword, polynomial)

    # Append CRC remainder to dataword
    codeword = dataword + crc_remainder_bits
    return codeword


def crc_check(codeword, crc_type):
    """Verify the CRC codeword."""
    # Define CRC polynomials
    crc_polynomials = {
        "CRC-4": "11111",
        "CRC-8": "111010101",
        "CRC-16": "1100000000000101",
        "CRC-16R": "1010000000000011",
        "CRC-24": "1100000000101000100000001",
        "CRC-32": "10000100110000010001110110110111"
    }
    polynomial = crc_polynomials.get(crc_type)
    if polynomial is None:
        raise ValueError("Unsupported CRC type")

    # Calculate CRC remainder
    crc_remainder_bits = crc_remainder(codeword, polynomial)
    syndrome = int(crc_remainder_bits, 2)
    return syndrome


# Test the functions
def test_crc_functions():
    datawords = ['111001', '11001100', '1111000011110000', '1011010111', '110101001001']
    crc_types = ['CRC-4', 'CRC-8', 'CRC-16', 'CRC-32']

    for crc_type in crc_types:
        print(f"Testing CRC type: {crc_type}")
        for dataword in datawords:
            codeword = crc_gen(dataword, len(dataword), crc_type)
            syndrome = crc_check(codeword, crc_type)
            print(f"Dataword: {dataword}, Codeword: {codeword}, Syndrome: {syndrome}")

if __name__ == "__main__":
    test_crc_functions()
