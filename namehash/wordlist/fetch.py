import requests
from bs4 import BeautifulSoup


url = 'http://www.gingersoftware.com/content/grammar-rules/adjectives/lists-of-adjectives/'

resp = requests.get(url)

soup = BeautifulSoup(resp.content, 'html.parser')

classes = {'Appearance adjectives': 'adjective.appearance.txt',
           'Color adjectives': 'adjective.color.txt',
           'Condition adjectives': 'adjective.condition.txt',
           'Personality adjectives – Positive': 'adjective.personality.txt',
           'Shape adjectives': 'adjective.shape.txt',
           'Size adjectives': 'adjective.size.txt',
           'Sound adjectives': 'adjective.sound.txt',
           'Time adjectives': 'adjective.time.txt',
           'Taste/Touch adjectives': 'adjective.taste.txt',
           'Touch adjectives': 'adjective.touch.txt',
           'Quantity adjectives': 'adjective.quantity.txt',
           }

for h2 in soup.select('h2'):
    words = []
    for li in h2.find_next_sibling('ul').find_all('li'):
        words.append(li.string)
    fname = classes.get(h2.string, None)
    if fname is None:
        print('Skipping {}'.format(h2.string))
    else:
        with open(fname, 'w') as fh:
            fh.write('\n'.join(words))
