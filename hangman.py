#!/usr/bin/env python3
"""
A terminal based game of Hangman.

1. Install Python 3
2. Open Terminal
3. To play, execute this file by typing: python3 hangman.py
"""

import urllib.request
import random
import time
import json
from copy import copy


pic = {}
pic[0] = """
Lovely Day!

  \\/ \\/\\/
   \\/ \\//
    \\ //
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

for k, v in list(pic.items())[1:]:
    pic[k] = '\n'.join(v)


def get_dictionary_word(full_list=False):
    """Return a random word, or a full list if needed.

    Download a dictionary and cache it locally.
    """
    url = 'https://raw.githubusercontent.com/fmalina/richardsgames/refs/heads/master/dictionary.txt'

    with open('dictionary.txt', 'a+') as f:
        f.seek(0)
        words = f.read()
        if not words:
            response = urllib.request.urlopen(url)
            words = response.read().decode('utf-8')
            f.write(words)
            f.truncate()
        else:
            # make it appear, that it's thinking for a sec...
            time.sleep(random.random() * 1.5 + random.random())
    words = words.splitlines()
    if full_list:
        return words
    return random.choice(words).upper()


def get_word_definition(word):
    """Get word definition failing silently."""
    url = 'https://api.urbandictionary.com/v0/define?term=%s' % word
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data['list'][0]['definition']
    except Exception as e:
        return


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
    """Play hangman."""
    tried = []
    bad_guesses = []
    while True:
        print()
        letter = input(
            "Enter one character to guess the word. Press Enter: ").upper()
        print()
        tried.append(letter.upper())
        if letter not in word:
            bad_guesses.append(letter)
            print('Wrong, try again. (%sx)' % len(bad_guesses))
            print(pic[len(bad_guesses)])
        else:
            print('👍 Correct, guess another.')
            if len(bad_guesses) == 0 and len(tried) == 1:
                print(pic[0])
        rendered = render_word(word, tried)
        render_bad_guesses = ''
        if bad_guesses:
            render_bad_guesses = '    NOT: ' + ', '.join(bad_guesses)
        print()
        print(rendered + render_bad_guesses)
        lost = len(bad_guesses) >= 8
        won = '_' not in rendered
        if lost:
            print()
            print('⚰️  You died.')
            print('The word was: %s' % word)
        if won:
            print()
            print('🎉 You win!')
            print()
        if won or lost:
            definition = get_word_definition(word)
            if definition:
                print()
                print(word.upper())
                print('~' * len(word))
                print(definition)
                print()
            return


if __name__ == '__main__':
    try:
        play_again = True
        print("Hey, let's play hangman.")
        while play_again:
            word = get_dictionary_word()
            print()
            print("I have a word in mind. It has %s characters." % len(word))
            print()
            print(render_word(word, []))
            print()
            play(word)
            print()
            print("Would you like to play again? y/yes + Enter")
            response = input("> ").lower()
            if response not in ("yes", "y"):
                play_again = False
    except KeyboardInterrupt:
        print()
        print()
        print('Scared of death? Ha Ha Ha Ha Ha')
