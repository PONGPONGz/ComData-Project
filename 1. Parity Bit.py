from functools import reduce
import numpy as np

# CASES = [
#     # these strings will be splitted into list later.
#     [
#         "10110001",
#         "10000001",
#         "10110000",
#         "00011000"
#     ]
# ]

def xor(str_list):
    return reduce(lambda x, y: int(x) ^ int(y), str_list)

# If some dataword has size < word_size, the dataword must be appended (padded) with bit ‘0’ until the
# size the dataword is word_size.
def generator(datawords, word_size, num_words):
    # In case some dataword has size < word_size, append bit '0' until len(dataword) == word_size
    for i in range(len(datawords)):
        if (len(datawords[i]) < word_size):
            datawords[i] = datawords[i] + (['0'] * (word_size - len(datawords[i])))

    # column parities
    columns = list(zip(*datawords))         # transpose matrix
    datawords.append([])                    # append an empty list to store parities at the end
    for i in range(len(columns)):
        xor_result = xor(columns[i])
        datawords[-1].append(str(xor_result))

    # row parities
    for i in range(len(datawords)):
        xor_result = xor(datawords[i])
        datawords[i].append(str(xor_result))
    
    for i in range(len(datawords)):
        datawords[i] = ''.join(datawords[i])

    return datawords

def checker(codewords):
    err_loc = (-1, -1)

    # row
    for i in range(len(codewords)):
        xor_result = xor(codewords[i])
        codewords[i] = codewords[i] + str(xor_result)
        if (xor_result != 0 and err_loc[1] == -1):
            err_loc = (err_loc[0], i)

    columns = list(zip(*codewords))
    codewords.append("")
    for i in range(len(columns)):
        xor_result = xor(columns[i])
        codewords[-1] = codewords[-1] + str(xor_result)
        if (xor_result != 0 and err_loc[0] == -1):
            err_loc = (i, err_loc[1])

    return codewords, err_loc

def test():    
    word_size = 8
    num_words = 4

    def generate_bit_string():
        return list(np.random.choice(['0', '1'], size=word_size))

    # 10 correct cases
    for i in range(10):
        datawords = [generate_bit_string() for _ in range(num_words)]
        print(f"Test #{i}")
        print("Input Datawords: ")
        for dataword in datawords:
            print(f"\t{dataword}")

        codewords = generator(datawords, word_size, num_words)
        print("Codewords:")
        for codeword in codewords:
            print(f"\t\'{codeword}\'")

        syndrome, err_loc = checker(codewords)
        print("Syndrome:")
        for row in syndrome:
            print(f"\t\'{row}\'")

        if (err_loc == (-1, -1)):
            print("No error found.")
        else:
            print(f"Error occured at col {err_loc[0]} row {err_loc[1]}")

    # 10 incorrect cases
    for i in range(10):
        datawords = [generate_bit_string() for _ in range(num_words)]
        print(f"Test #{10+i}")
        print("Input Datawords: ")
        for dataword in datawords:
            print(f"\t{dataword}")

        codewords = generator(datawords, word_size, num_words)
        print("Codewords:")
        for codeword in codewords:
            print(f"\t\'{codeword}\'")

        # random error point
        error_row = np.random.randint(0, num_words)
        error_col = np.random.randint(0, word_size)
        codewords[error_row] = codewords[error_row][:error_col - 1] + ('0' if codewords[error_row][error_col] == '1' else '1') + codewords[error_row][error_col:]

        syndrome, err_loc = checker(codewords)
        print("Syndrome:")
        for row in syndrome:
            print(f"\t\'{row}\'")

        if (err_loc == (-1, -1)):
            print("No error found.")
        else:
            print(f"Error occured at col {err_loc[0]} row {err_loc[1]}")
    # for i in range(10):
    #     datawords = [generate_bit_string() for _ in range(num_words)]
    #     codewords = generator(datawords, word_size, num_words)

    #     # random error point
    #     error_row = np.random.randint(0, num_words)
    #     error_col = np.random.randint(0, word_size)
    #     codewords[error_row][error_col] = '0' if codewords[error_row][error_col] == '1' else '1'

    #     syndrome, err_loc = checker(codewords)
    #     print(syndrome)
    #     print("Error is found at", err_loc)

test()