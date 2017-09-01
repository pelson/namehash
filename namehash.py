import itertools
from pathlib import Path
import random


wordlist_dir = Path(__file__).parent / 'wordlist'


#: A mapping from class to words
wordlists = {}

#: A mapping from word to class
wordclasses = {}


def _populate_words():
    if wordlists:
        return

    for fname in wordlist_dir.glob('*.txt'):
        with fname.open('r') as fh:
            words = fh.read().split('\n')

            # TODO: Put this into the wordlists themselves.
            random.seed(4)
            random.shuffle(words)

            classification = str(fname.name[:-4])
            wordlists[classification] = words
            for word in words:
                # There may be some duplicates between nouns and adjectives.
                wordclasses.setdefault(word, classification)


# Unused: appearance, condition, time, touch
adjective_order = ['adjective.quantity',
                   #'adjective.quality',
                   'adjective.sound',
                   #'adjective.age',
                   'adjective.shape',
                   'adjective.color',
                    #Proper adjective (often nationality, other place of origin, or material)
                    #Purpose or qualifier,
                    'adjective.personality']
combinations = {1: list(itertools.combinations(adjective_order, 1)),
                2: list(itertools.combinations(adjective_order, 2)),
                3: list(itertools.combinations(adjective_order, 3)),
                }

def generate(n_words=3):
    rand = random.randint(0, 10000000)
    return encode(rand, n_words=n_words)


def encode(number, n_words=3):
    _populate_words()

    # TODO: Assert number below limit.

    n_adj = n_words - 1

    from collections import OrderedDict
    diagnostics = OrderedDict()

    n_nouns = len(wordlists['noun'])
    noun_ind = diagnostics['noun-index'] = number % n_nouns

    # Identify the noun for the given number.
    noun = wordlists['noun'][noun_ind]
    residual = number // n_nouns

    # Identify the structure for the given number
    struct_ind = diagnostics['structure-index'] = residual % len(combinations[n_adj])
    structure = combinations[n_adj][struct_ind]
    residual = residual // len(combinations[n_adj])

    list_lengths = [len(wordlists[cat]) for cat in structure]

    words = []
    for dim, word_class in reversed(list(zip(list_lengths, structure))):
        v = diagnostics['{}-index'.format(word_class)] = residual % dim
        residual = residual // dim
        words.insert(0, wordlists[word_class][v])

        # Dimension of structure

    words.append(noun)
    namehash = '-'.join(words)

    return namehash


def _identify_structure(words):
    # There are some words in the nouns and the adjectives list (e.g. orange)
    structure = [wordclasses[word] for word in words]
    return structure


def decode(namehash):
    _populate_words()

    words = namehash.split('-')
    structure = _identify_structure(words)
    print(structure)

    from collections import OrderedDict
    diagnostics = OrderedDict()

    positions = [wordlists[wordclasses[word]].index(word)
                 for word in words]

    list_lengths = [len(wordlists[cat]) for cat in structure]

    noun_posn = diagnostics['noun-index'] = wordlists['noun'].index(words[-1])

    list_lengths.insert(-1, len(combinations[len(words) - 1]))
    struct_posn = diagnostics['structure-index'] = combinations[len(words) - 1].index(tuple(structure[:-1]))
    positions.insert(-1, struct_posn)

    factor = 1
    number = 0
    for posn, length in reversed(list(zip(positions, list_lengths))):
        number += posn * factor
        factor *= length
    return number


if __name__ == '__main__':
    _populate_words()

    print(encode(10143))
    print(decode('sparse-orange-flax'))

    for i in range(120, 1880802 * 50, 10023):
        namehash = encode(i, 3)
        print(i)
        print(i, namehash, decode(namehash))

    print(encode(1880802))

    print(decode('abundant-zealous-pulley'))
