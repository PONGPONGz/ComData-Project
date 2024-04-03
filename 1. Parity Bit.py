from functools import reduce

CASES = [
    # these strings will be splitted into list later.
    [
        "10110001",
        "0000001",
        "10110000",
        "00011000"
    ]
]

# If some dataword has size < word_size, the dataword must be appended (padded) with bit ‘0’ until the
# size the dataword is word_size.
def generator(datawords, word_size=8, num_words=4):
    # In case some dataword has size < word_size, append bit '0' until len(dataword) == word_size
    for i in range(len(datawords)):
        if (len(datawords[i]) < word_size):
            datawords[i] = (['0'] * (word_size - len(datawords[i]))) + datawords[i]

    # column parities
    columns = list(zip(*datawords))         # transpose matrix
    datawords.append([])                    # append an empty list to store parities at the end
    for i in range(len(columns)):
        xor_result = reduce(lambda x, y: int(x) ^ int(y), columns[i])
        datawords[-1].append(str(xor_result))

    # row parities
    for i in range(len(datawords)):
        xor_result = reduce(lambda x, y: int(x) ^ int(y), datawords[i])
        datawords[i].append(str(xor_result))
    
    for i in range(len(datawords)):
        datawords[i] = ''.join(datawords[i])

    return datawords

def checker(codeword):
    pass

def test():    
    # Convert test cases into lists.
    for case in CASES:
        for i in range(len(case)):
            case[i] = list(case[i])

    # Execute test cases.
    for case in CASES:
        print(generator(case, len(case[0]), len(case)))

test()