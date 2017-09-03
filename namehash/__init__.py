from collections import OrderedDict
import itertools
from pathlib import Path
import random
import logging


log = logging.getLogger(__name__)
logging.basicConfig()
#log.setLevel(logging.DEBUG)

wordlist_dir = Path(__file__).parent / 'wordlist'


#: A mapping from class to words.
wordlists = {}

#: A mapping from word to class.
wordclasses = {}

#: A mapping from n_words to length of the adjective dimension.
adj_combo_dim_sizes = {}


def _populate_words():
    if wordlists:
        return

    for fname in sorted(wordlist_dir.glob('*.txt')):
        with fname.open('r') as fh:
            words = fh.read().split('\n')
            words = [word for word in words if word]

            # TODO: Put this into the wordlists themselves.
            random.seed(4)
            random.shuffle(words)

            classification = str(fname.name[:-4])
            wordlists[classification] = words
            for word in words:
                # There may be some duplicates between nouns and adjectives.
                wordclasses.setdefault(word, classification)

    for n_words, combos in combinations.items():
        combination_lengths[n_words] = OrderedDict()
        for combo in combos:
            p = 1
            for wordclass in combo:
                p *= len(wordlists[wordclass])
            combination_lengths[n_words][combo] = p

        adj_combo_dim_sizes[n_words] = sum(combination_lengths[n_words].values())


adjective_order = ['adjective.quantity',
                   'adjective.condition',
                   'adjective.appearance',
                   'adjective.sound',
                   'adjective.time',
                   'adjective.shape',
                   'adjective.touch',
                   'adjective.color',
                    #Proper adjective (often nationality, other place of origin, or material)
                    #Purpose or qualifier,
                    'adjective.personality']
combinations = {1: list(itertools.combinations(adjective_order, 1)),
                2: list(itertools.combinations(adjective_order, 2)),
                3: list(itertools.combinations(adjective_order, 3)),
                }

#: As combinations, but with each combination's # of unique values computed.
combination_lengths = {}


def generate(n_words=3):
    rand = random.randint(0, 10000000)
    return encode(rand, n_words=n_words)


def encode(number, n_words=3):
    _populate_words()

    # TODO: Assert number below limit.

    n_adj = n_words - 1

    diagnostics = OrderedDict()

    n_nouns = len(wordlists['noun'])
    rem, noun_i =  divmod(number, n_nouns)
    diagnostics['noun-index'] = noun_i

    factor = 1
    factor = n_nouns

    # Identify the noun for the given number.
    noun = wordlists['noun'][noun_i]

    # Identify the structure for the given number
    n_struct = len(combinations[n_adj])
    # rem, struct_i = divmod(rem, n_struct)

    struct_index = 0
    for struct, struct_len in combination_lengths[n_adj].items():
        if rem < struct_len:
            structure = struct
            break
        else:
            struct_index += 1
            rem -= struct_len
    else:
        if rem < struct_len:
            structure = struct
            rem -= struct_len
        else:
            raise ValueError('Check overflow.')

    diagnostics['structure-index'] = struct_index

    adj_dim_len = adj_combo_dim_sizes[n_adj]

    # For each item in the structure, compute the available words.
    list_lengths = [len(wordlists[cat]) for cat in structure]

    # Put together the wordlist, working from right to left.
    words = [noun]
    for dim, word_class in reversed(list(zip(list_lengths, structure))):
        rem, adj_i = divmod(rem, dim)
        diagnostics['{}-index'.format(word_class)] = adj_i
        words.append(wordlists[word_class][adj_i])
        factor *= dim

    if rem != 0:
        raise OverflowError('Overflow.')

    namehash = '-'.join(reversed(words))
    log.debug('Encode {}: "{}".\n  Diagnostics: {}'.format(number, namehash, diagnostics))

    return namehash


def _identify_structure(words):
    # There are some words in the nouns and the adjectives list (e.g. orange)
    structure = tuple(wordclasses[word] for word in words[:-1]) + ('noun', )
    return tuple(structure)


def decode(namehash):
    _populate_words()

    words = namehash.split('-')
    structure = _identify_structure(words)

    n_adj = len(structure) - 1
    adj_dim_offset = 0
    # TODO: Pre-compute, or functionise.
    for struct, struct_len in combination_lengths[n_adj].items():
        if structure[:-1] == struct:
            break
        else:
            adj_dim_offset += struct_len
    else:
        # Should never get here...
        assert False
    adj_dim_len = adj_combo_dim_sizes[n_adj]

    diagnostics = OrderedDict()

    positions = [wordlists[wordclass].index(word)
                 for word, wordclass in zip(words, structure)]

    list_lengths = [len(wordlists[cat]) for cat in structure]

    noun_posn = diagnostics['noun-index'] = wordlists['noun'].index(words[-1])

    struct_names = structure[:-1]
    diagnostics['structure-index'] = combinations[len(words) - 1].index(tuple(structure[:-1]))

    factor = 1
    number = adj_dim_offset
    for posn, length, name in reversed(list(zip(positions[:-1], list_lengths[:-1], struct_names))):
        if name:
            diagnostics[name + '-index'] = posn

        number += posn * factor
        factor *= length

    noun_len = len(wordlists['noun'])
    diagnostics ['noun-len'] = noun_len
    diagnostics['adjective-dim-len'] = adj_dim_len
    diagnostics['adjective-posn'] = number

    number = (noun_posn +
               noun_len *
                (number))

    log.debug('Decode "{}": {}.\n  Diagnostics: {}'.format(namehash, number, diagnostics))

    return number
