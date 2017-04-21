import random


class Word:
    def __init__(self,linesWord):
        self.linesWord = linesWord

    #getLetterValue calculates the value of each letter then returns the sum



    def getLetterValue(word):
        scrabbleVals = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
                        'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                        'Y': 4, 'Z': 10}
        # Dictionary of scrable values
        count = 0

        for char in word:
            for letter in scrabbleVals:
                if char == letter:
                    count += scrabbleVals[letter]

        return count

    #getFinalValue calulates the final value by evaluating word length
        # then returns the word's letter point value + the word's length point value
    def getFinalValue(self, word):
        wordLength = len(word)
        dif = 0
        letterValue = self.getLetterValue(word)

        if wordLength > 4:
            dif = wordLength - 4

        return letterValue + dif

    #changeWordFile grabs words from Txt file and calculates final point values
        # then pushes them into a second pre-made Txt file then closes both files
    def changeWordFile(self):
        #self.linesWord
        # unscored = open("../assets/words/word_bank_unscored.txt", 'r')
        # scored = open("../assets/words/word_bank_scored.txt", 'w')

        #writes new file with word value to words_bank_scored
        '''for word in unscored:
            pointValue = self.getFinalValue(word.strip())
            scored.write(word + pointValue + '\n')'''

        wordStr = open('../assets/words/word_bank_unscored.txt', "r+")
        for lineStr in wordStr:
            self.linesWord.append(lineStr)

        # scored.close()
        # unscored.close()
        wordStr.close()
        #print(self.linesWord)
        return self.linesWord

    # changeWordFile("")

    #ranWord pulls a random word from the word bank and returns the word and score
    def randWord(self):


        length = len(self.linesWord)
        ran = random.randint(0, length)

        word = self.linesWord[ran]
        value = self.getFinalValue(word)

        return word, value

    #Example to grab values out of return in method ranWord
    '''tup = randWord("")
    w = tup[0]
    v = tup[1]
    print(w, v)'''

