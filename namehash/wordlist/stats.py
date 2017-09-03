# Remove duplicate adjectives.
# Remove all words with a '-'


# Compute total number of unique.

from .. import encode, decode, combinations, _populate_words, wordlists

_populate_words()


def n_combinations(n_words=3):
    combos = combinations[n_words - 1]
    nouns = len(wordlists['noun'])

    wl_lengths = {wordclass: len(wordlist)
                  for wordclass, wordlist in wordlists.items()}

    lengths = [nouns, len(combos)]
    n_all_combs = 0
    for comb in combos:
        p = 1
        for wordclass in comb:
            p *= wl_lengths[wordclass]
        n_all_combs += p

    return nouns * n_all_combs


print('Combinations: 2: {}; 3: {}; 4: {};'.format(
    n_combinations(2), n_combinations(3), n_combinations(4)))


if False:
    i = 25100950
    fail_count = 0
    while True:
        hash = encode(i, n_words=3)
        inverse = decode(hash)
        if i != inverse:
            print('Failed on i={}. Hash: {}; decoded: {}'.format(i, hash, inverse))
            fail_count += 1

        if fail_count > 3:
            break


        if i % 1000 == 0:
            print(i, end=', ')
        if i % 100000 == 0:
            print()

        i += 1
