from functools import reduce
import numpy as np

# XOR the whole string/list
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

    # row validation
    for i in range(len(codewords)):
        xor_result = xor(codewords[i])
        codewords[i] = codewords[i] + str(xor_result)
        if (xor_result != 0 and err_loc[1] == -1):
            err_loc = (err_loc[0], i)

    columns = list(zip(*codewords))             # transpose matrix
    codewords.append("")                        # empty string at the end to contain parity bits.
    for i in range(len(columns)):
        xor_result = xor(columns[i])
        codewords[-1] = codewords[-1] + str(xor_result)
        if (xor_result != 0 and err_loc[0] == -1):
            err_loc = (i, err_loc[1])

    return codewords, err_loc

def test():    
    word_size = 8
    num_words = 4

    # print list elements with identation
    def printl(_list):
        for element in _list:
            print(f"\t{element}")

    # randomly generate bits of <word_size>
    def generate_bit_string():
        return list(np.random.choice(['0', '1'], size=word_size))

    for i in range(20):
        datawords = [generate_bit_string() for _ in range(num_words)]           # generate <num_words> of randomed bits of <word_size>
        print(f"Test #{i+1}")
        print("Input Datawords: ")
        printl(datawords)

        codewords = generator(datawords, word_size, num_words)
        print("Codewords:")
        printl(codewords)

        # For 10 incorrect cases
        if (i >= 10):
            # random error point
            error_row = np.random.randint(0, num_words)
            error_col = np.random.randint(0, word_size)
            codewords[error_row] = codewords[error_row][:error_col] + ('0' if codewords[error_row][error_col] == '1' else '1') + codewords[error_row][error_col+1:]

        syndrome, err_loc = checker(codewords)
        print("Syndrome:")
        printl(syndrome)

        if (err_loc == (-1, -1)):
            print("No error present.")
        else:
            print(f"Error occured at col {err_loc[0]} row {err_loc[1]} (index starts at 0).")
    
test()