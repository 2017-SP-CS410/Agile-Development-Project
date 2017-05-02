import os
import random
# getLetterValue calculates the value of each letter then returns the sum
def getLetterValue(word):
    scrabbleVals = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
                    'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
                    'y': 4, 'z': 10}
    count = 0
    for char in word:
        for letter in scrabbleVals:
            if char == letter:
                count += scrabbleVals[letter]
    return count
    # getFinalValue calulates the final value by evaluating word length
    # then returns the word's letter point value + the word's length point value

def getFinalValue(word):
    wordLength = len(word)
    dif = 0
    letterValue = getLetterValue(word)

    if wordLength > 4:
        dif = wordLength - 4
    return letterValue + dif
    # changeWordFile grabs words from Txt file and calculates final point values
    # then pushes them into a second pre-made Txt file then closes both files

def makeWordList():
    list =[]
    package_directory = os.path.dirname(os.path.abspath(__file__))
    word_bank_unscored = os.path.join(package_directory, '..', 'assets', 'words', 'word_bank_unscored.txt')

    for word in open(word_bank_unscored, 'r'):
        list.append(str.lower(word.strip()))
    return list






