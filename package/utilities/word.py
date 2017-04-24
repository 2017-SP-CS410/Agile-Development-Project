import os
import random
# getLetterValue calculates the value of each letter then returns the sum
def getLetterValue(word):
    scrabbleVals = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
                    'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                    'Y': 4, 'Z': 10}
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




