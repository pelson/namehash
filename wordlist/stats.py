# Remove duplicate adjectives.
# Remove all words with a '-'


# Compute total number of unique.

from .. import namehash

namehash._populate_words()



def n_combinations(n_words=3):
    combinations = namehash.combinations[n_words - 1]
    nouns = len(namehash.wordlists['noun'])

    wl_lengths = {wordclass: len(wordlist)
                  for wordclass, wordlist in namehash.wordlists.items()}

    lengths = [nouns, len(combinations)]
    n_all_combs = 0
    for comb in combinations:
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
        hash = namehash.encode(i, n_words=3)
        inverse = namehash.decode(hash)
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
