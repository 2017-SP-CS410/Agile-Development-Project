import random


#Dictionary of scrable values
scrabbleVals = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
                'M': 3,'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                'Y': 4, 'Z': 10}

#getLetterValue calculates the value of each letter then returns the sum
def getLetterValue(word):
    count = 0

    for char in word:
        for letter in scrabbleVals:
            if char == letter:
                count += scrabbleVals[letter]

    return count

#getFinalValue calulates the final value by evaluating word length
    # then returns the word's letter point value + the word's length point value
def getFinalValue(word):
    wordLength = len(word)
    dif = 0
    letterValue = getLetterValue(word)

    if wordLength > 4:
        dif = wordLength - 4

    return letterValue + dif

#changeWordFile grabs words from Txt file and calculates final point values
    # then pushes them into a second pre-made Txt file then closes both files
def changeWordFile(self):
    unscored = open("../assets/words/word_bank_unscored.txt", 'r+')
    scored = open("../assets/words/word_bank_scored.txt", 'r+')

    for word in unscored:
        pointValue = getFinalValue(word)
        scored.write(word + str(pointValue) + '\n')

    scored.close()
    unscored.close()

changeWordFile("")

#ranWord pulls a random word from the word bank and returns the word and score
def randWord(self):
    linesWord = []
    wordStr = open('../assets/words/word_bank_unscored.txt')
    for lineStr in wordStr:
        linesWord.append(lineStr)

    length = len(linesWord)
    ran = random.randint(0, length)

    word = linesWord[ran]
    value = getFinalValue(word)

    return word, value

#Example to grab values out of return in method ranWord
tup = (randWord(""))
w = tup[0]
v = tup[1]
print(w,v)
