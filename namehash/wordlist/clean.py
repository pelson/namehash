# Remove duplicate adjectives.
# Remove all words with a '-'


# Compute total number of unique.

from .. import wordlists, _populate_words

_populate_words()

seen = {}

for wordclass, words in wordlists.items():
    for word in words:
        seen.setdefault(word, []).append(wordclass)

for word, classes in sorted(seen.items()):
    if len(classes) > 1:
        print(len(classes), word, sorted(classes))


for word, classes in sorted(seen.items()):
    if '-' in word:
        print(word, seen[word])
