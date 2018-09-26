#!/usr/bin/python3
"""
A terminal based game of Hangman.

1. Install Python 3
2. Open Terminal
3. To play, execute this file by typing: python3 hangman.py
"""

import urllib.request
import random
from copy import copy


pic = {}
pic[0] = """
Lovely Day!

  \/ \/\/
   \/ \//
    \ //
     ||
     |}
     ||
"""
pic[1] = [''] + 6 * ['|']
pic[2] = copy(pic[1])
pic[2][1] = '__________'
pic[2][2] = '|       |'
pic[3] = copy(pic[2])
pic[3][3] = '|       O'
pic[4] = copy(pic[3])
pic[4][4] = '|       |'
pic[5] = copy(pic[4])
pic[5][4] = '|      /|'
pic[6] = copy(pic[5])
pic[6][4] = '|      /|\\'
pic[7] = copy(pic[6])
pic[7][5] = '|      /'
pic[8] = copy(pic[7])
pic[8][5] = '|      / \\'
pic[8][3] = '|       😵'

for k,v in list(pic.items())[1:]:
    pic[k] = '\n'.join(v)


def get_dictionary():
    """Download a dictionary and get a list of words."""
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

    response = urllib.request.urlopen(word_site)
    return response.read().splitlines()


def render_word(word, tried_letters):
    """Render a word in a game of hangman.

    >>> render_word('ABCDEF', ['a', 'd', 'm'])
    'A _ _ D _ _'
    >>> render_word('ABCDEF', ['a', 'd', 'e'])
    'A _ _ D E _'
    """
    word = word.upper()
    tried_letters = [x.upper() for x in tried_letters]
    unguessed = [x for x in word if x not in tried_letters]
    for missing in unguessed:
        word = word.replace(missing, '_')
    return ' '.join(word)


def play(word):
    """Play hangman"""
    tried = []
    bad_guesses = 0
    while True:
        print()
        letter = input("Enter one character to guess the word: ").upper()
        print()
        tried.append(letter.upper())
        if letter not in word:
            bad_guesses += 1
            print('Wrong, try again. (%sx)' % bad_guesses)
        else:
            print('👍 Currect, try again.')

        print(pic[bad_guesses])
        print()
        rendered = render_word(word, tried)
        print(rendered)
        if bad_guesses >= 8:
            print()
            print('⚰️  You died.')
            print('The word was: %s' % word)
            exit()
        if '_' not in rendered:
            print()
            print('🎉 You win!')
            print()
            exit()


if __name__ == '__main__':
    print("Hey, let's play hangman.")
    print()
    words = get_dictionary()
    guess = random.choice(words).decode().upper()
    print("I have a word in mind. It has %s characters." % len(guess))
    play(guess)
