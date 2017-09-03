from namehash import *

def roundtrip(n, n_words=3):
    hash = encode(n, n_words)
    actual = decode(hash)
    if n != actual:
        next_hash = encode(actual, n_words)
        raise ValueError('{} -> {} -> {} -> {}'.format(n, hash, actual, next_hash))
    return hash


if __name__ == '__main__':
    roundtrip(0)
    roundtrip(1)
    roundtrip(2)
    roundtrip(4519)

    roundtrip(2012000)

    roundtrip(25161700)

    roundtrip(42343029)
    roundtrip(42343030)
    roundtrip(42343031)


    print(encode(25161700))
    print(decode('cooing-smooth-logic'))

    print(adj_combo_dim_sizes)

    print(encode(25161792))
    print(decode('quiet-yellow-behest'))
    print(encode(25161793))
    print(decode('quiet-yellow-week'))


    # for i in range(1000):
    #     encode(i)
