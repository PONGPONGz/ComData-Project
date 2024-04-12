def convert_to_binary(ascii_values):
    # Convert ASCII values to 8-bit binary
    return ['{0:08b}'.format(value) for value in ascii_values]

def binary_addition(binary_values):
    # Initialize the sum with 8 bits
    total_sum = '00000000'
    # Iterate over each binary value in the list
    for binary_value in binary_values:
        result = ''
        carry = 0
        # Iterate over each bit position from right to left
        for i in range(7, -1, -1): 
            bit_sum = int(total_sum[i]) + int(binary_value[i]) + carry
            # Append the sum of bits to the result
            result = str(bit_sum % 2) + result  
             # Calculate carry for the next bit
            carry = bit_sum // 2 
        # Take only the last 8 bits of the result
        total_sum = result[-8:]  
        if carry:
            # If there's a carry after processing all bits, add 1 to the next addition
            total_sum = bin(int(total_sum, 2) + 1)[2:].zfill(8)
    return total_sum

def binary_complement(binary_string):
    return ''.join('1' if bit == '0' else '0' for bit in binary_string)

# Sender Side
def checksum_gen(file_name):
    # Open the file and read the data
    with open(file_name, 'r') as file:
        data = file.read()

    print("\nData from", file_name + ":", data + "\n")

    # Convert data to ASCII values
    ascii_values = []
    for char in data:
        if char == ' ':
            # Skip space character
            print("Skipping space character.")
            continue
        # Get ASCII value of the character
        value = ord(char)  
        ascii_values.append(value)
        print(f"ASCII value for '{char}': {value}")

    # Convert ASCII values to 8-bit binary
    binary_values = convert_to_binary(ascii_values)
    print("\nBinary values of data:\n", binary_values)

    # Perform binary addition in chunks of 8 bits
    total_binary_sum = binary_addition(binary_values)
    print("\nSum of binary values:", total_binary_sum)

    # Calculate the checksum by taking the binary complement of the total sum
    checksum = binary_complement(total_binary_sum)
    print("Checksum:", checksum)

    return checksum


# Receiver Side
def checksum_check(file_name, checksum_value):
    with open(file_name, 'r') as file:
        data = file.read()
    
    print("\nData from", file_name + ":", data + "\n")

    ascii_values = []
    for char in data:
        if char == ' ':
            print("Skipping space character.")
            continue
        value = ord(char) 
        ascii_values.append(value)
        print(f"ASCII value for '{char}': {value}")

    binary_values = convert_to_binary(ascii_values)
    print("\nBinary values of data:\n", binary_values)

    total_binary_sum = binary_addition(binary_values)
    print("\nSum of binary values:", total_binary_sum)

    # Add the checksum value to the total sum 
    total_binary_sum = binary_addition([total_binary_sum, checksum_value])
    print("\nTotal sum of data with checksum:", total_binary_sum)

    # Calculate the checksum validity
    validity = 0 if int(total_binary_sum, 2) == 255 else -1

    complement = binary_complement(total_binary_sum)
    print("Complement:", complement)

    return validity

# File names
file1_name = "file1.txt"
file2_name = "file2.txt"

# Sender Side
print("\n\nChecksum Generator:")
checksum_value = checksum_gen(file1_name)

# Receiver Side
print("\n\nChecksum Checker:")
validity = checksum_check(file2_name, checksum_value)

print("\nChecksum Validation:", "PASS\n" if validity == 0 else "FAIL\n")