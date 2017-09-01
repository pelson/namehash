from .namehash import *

if __name__ == '__main__':

    print(encode(9516072))
    print(decode('thundering-victorious-uncle'))
    for i in range(120, 1000, 1):
        namehash = encode(i, 3)
        print(i, end=' ')
        print(namehash, decode(namehash))

    print(encode(1880802))

    print(decode('abundant-zealous-pulley'))
