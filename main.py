import random
import sys, os

############################################# 

############## HOW TO USE #################

#### TO PLAY ONLINE, RUN THE ONLINEGAMELOOP FUNCTION.
## ENTER THE GUESS WORD THE COMPUTER GIVES IN THE CONSOLE.
## THEN ENTER THE LETTER STATES THAT YOU SEE ON THE WORDLE PAGE
## MEANING IF I GUESSED THE WORD "SLATE" AND THE S WAS YELLOW AND THE A 
### WAS GREEN THEN I WOULD ENTER "y g  " WHERE "y" IS IF A LETTER IS YELLOW
#### "g"  IS IF A LETTER IS GREEN AND " " IS FOR LETTERS NOT IN THE WORD.
## ONE MORE EXAMPLE: WORD ENTERED IS "TESTS". SAY FIRST S IS GREEN, AND E IS YELLOW.
## THEN YOU WOULD ENTER " yg  ".

## TO HAVE THE BOT PLAY BY ITSELF, WITH EITHER A RANDOM WORD FROM THE WORDLE ANSWER
## BASE OR WITH A WORD YOU PICK (MUST BE FROM WORDLE ANSWERBASE) RUN THE GAMELOOP 
## FUNCTION. 


##############################################################
################# NOTES ON THE BOT ########################

### THIS IS A HARD MODE BOT, SO IT WILL ALWAYS PLAY AS IT IS IS IN HARDMODE.
## AVERAGE NUMBER OF ROUNDS FOR THE BOT IS 3.6, WHICH IS BETTER THAN HUMAN PLAY

## IF ANY QUESTIONS, FEEL FREE TO CONTACT. THIS IS A GOOD BOT FOR BUILDING ON TOP OF AND ADDING MORE SHOPFISTICATION TO IT.


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def correctStringGen(guess, targetWord):
    i = 0
    string = ''
    for letter in guess:
        if letter == targetWord[i]:
            string += 'g'
        elif letter in targetWord:
            string += 'y'
        else:
            string += ' '
        i += 1

    return string


def inputReader(word, string):
    greenLetters = []
    yellowLetters = []
    wrongLetters = []
    i = 0
    for letter in string:
        if letter == ' ':
            wrongLetters.append(word[i])
        elif letter == 'y':
            yellowLetters.append(word[i])
        elif letter == 'g':
            g = [word[i], i]
            greenLetters += [g]
        i += 1

    res = []
    [res.append(x) for x in yellowLetters if x not in res]
    return [greenLetters, res, wrongLetters]


def wordList():
    file = open("WordleBot2.0/WordleAnswers.txt", "r")
    Words = []
    for word in file:
        word = word.replace('\n', '')
        Words.append(word)

    return Words


def mostCommonLetterByPosition(words, position):
    numOfLetters = [0] * 26
    for word in words:
        val = ord(word[position]) - 97
        numOfLetters[val] += 1

    return numOfLetters


def optimalGuess(words, letterStates, letterFrequency):
    mostCommonLetters = []
    for i in range(5):
        mostCommonLetters.append(mostCommonLetterByPosition(words, i))
    bestGuess = ''
    max = 0
    roughlyTiedWords = []
    

    for word in words:
        sum = 0
        i = 0
        guessedThisRound = []

                
        seenThisRound = {
          "a": 0,
          "b": 0,
          "c": 0,
          "d": 0,
          "e": 0,
          "f": 0,
          "g": 0,
          "h": 0,
          "i": 0,
          "j": 0,
          "k": 0,
          "l": 0,
          "m": 0,
          "n": 0,
          "o": 0,
          "p": 0,
          "q": 0,
          "r": 0,
          "s": 0,
          "t": 0,
          "u": 0,
          "v": 0,
          "w": 0,
          "x": 0,
          "y": 0,
          "z": 0
        }
        for letter in word:
            seenThisRound[letter] +=1
            sum += (letterFrequency[letter] * mostCommonLetters[i][ord(letter) - 97]) / (seenThisRound[letter])
            i += 1
            #guessedThisRound.append(letter)
        if sum > max:
          max = sum
          bestGuess = word
            
    return bestGuess


def updateWordList(words, letterStates, guessWord):

    removed = False
    greenLetters = [''] * 5

    for greenPair in letterStates[0]:

        greenLetters[greenPair[1]] = greenPair[0]

    yellowWords = words[:]
    tempwords = yellowWords[:]
    letPos = 0
    for letter in guessWord:
        if letter in letterStates[1]:
            for word in tempwords:
                if word[letPos] == letter and not letter == greenLetters[
                        letPos]:

                    yellowWords.remove(word)

            tempwords = yellowWords[:]
        letPos += 1

    for letter in letterStates[1]:
        for word in tempwords:
            removed = False
            if letter not in word:
                if not removed:
                    yellowWords.remove(word)

                    removed = True
        tempwords = yellowWords[:]

    tempwords = yellowWords[:]

    for word in tempwords:
        letterPosition = 0
        for letter in word:
            if letter in letterStates[2]:
                if not removed:
                    yellowWords.remove(word)
                    removed = True
            elif letter != greenLetters[letterPosition] and greenLetters[
                    letterPosition] != '':
                if not removed:
                    yellowWords.remove(word)
                    removed = True
            letterPosition += 1
        removed = False

    return yellowWords


def gameLoop(words, targetWord, letterStates, letterFrequency):
    done = False
    round = 1
    print(f"Target word is {targetWord}")
    print('')
    print('-----------------')
    print('')
    while not done:
        print(f"It is round {round}")
        print('')
        print('-----------------')
        print('')
        guessWord = optimalGuess(words, letterStates, letterFrequency)
        correctString = correctStringGen(guessWord, targetWord)
        letterStates = inputReader(guessWord, correctString)

        if len(words) < 50:
            print("Remaing Words are")
            print('')
            print('-----------------')
            print('')
            print(words)

        print('')
        print(f"there are {len(words)} remaining")
        print(f"Computers guess is {guessWord}")
        print(f"yellow letters are {letterStates[1]}")
        print(f"green letters are {letterStates[0]}")
        print('')
        print('-----------------')
        print('')

        words = updateWordList(words, letterStates, guessWord)

        if guessWord == targetWord:
            print('')
            print('-----------------')
            print('')

            print("YOU WIN!!!!!!!!!!!!")

            print('')
            print('-----------------')
            print('')
            done = True
            return [round, guessWord]
        round += 1
        if round > 6:
            print("you have failed")
            done = True
            return [round, targetWord]


def runner(letterFrequency):
    words = wordList()

    letterStates = [[], [], []]
    

    
  
    wins = 0
    losses = 0
    roundsSum = 0
    loseWords = []
    fastWinWords = []
    distribution = [0] * 7
    for i in range(len(words)):
        targetWord = words[i]
        blockPrint()
        gameInfo = gameLoop(words, targetWord, letterStates, letterFrequency)
        enablePrint()
        word = gameInfo[1]
        roundScore = gameInfo[0]
        if roundScore <= 2:
            wins += 1
            distribution[roundScore] += 1
            fastWinWords.append(word)
        elif roundScore <= 6:
            wins += 1
            distribution[roundScore] += 1
        else:
            losses += 1
            loseWords.append(word)
        roundsSum += roundScore
        if i % 100 == 0:
            print(f"we have completed {i} runs")
            print("")

    print(f"we won {wins} times. With a winrate of {wins/len(words)}")
    print("")
    print(f"we lost {losses} times. With a lossrate of {losses/len(words)}")
    print("")
    print(f"the average round number was {roundsSum/len(words)}")
    print('')
    print(f"we lost on the words {loseWords}")
    print('')
    print(f"fast winning words are {fastWinWords}")
    print('')
    distribution.pop(0)
    print(f"our distribution is {distribution}")



def onlineGameLoop(words, letterStates, letterFrequency):
    done = False
    round = 1

    while not done:
        print(f"It is round {round}")
        print('')
        print('-----------------')
        print('')
        guessWord = optimalGuess(words, letterStates, letterFrequency)
        print(f"guess word is {guessWord}")
        
        correctString = input("Enter the correct string ")
        letterStates = inputReader(guessWord, correctString)

        if len(words) < 50:
            print("Remaing Words are")
            print('')
            print('-----------------')
            print('')
            print(words)


        words = updateWordList(words, letterStates, guessWord)

        if len(letterStates[0]) == 5:
            print('')
            print('-----------------')
            print('')

            print("YOU WIN!!!!!!!!!!!!")

            print('')
            print('-----------------')
            print('')
            done = True
            return [round, guessWord]
        round += 1
        if round > 6:
            print("you have failed")
            done = True
            return [round]


words = wordList()

letterStates = [[], [], []]



letterFrequency = {
  "a": 7.8,
  "b": 2,
  "c": 4,
  "d": 5.8,
  "e": 11,
  "f": 1.4,
  "g": 3,
  "h": 2.3,
  "i": 8.2,
  "j": 0.03,
  "k": 2.5,
  "l": 5.3,
  "m": 3.2,
  "n": 7.2,
  "o": 6.1,
  "p": 2.8,
  "q": 0.24,
  "r": 7.3,
  "s": 8.7,
  "t": 6.7,
  "u": 3.3,
  "v": 1,
  "w": 0.91,
  "x": 0.27,
  "y": 1.6,
  "z": 0.44
}

## RUN THIS TO PLAY ONLINE ON THE WORDLE SITE
onlineGameLoop(words, letterStates, letterFrequency)

### RUN THIS TO PLAY OFFLINE
# gameLoop(words, random.choice(words), letterStates, letterFrequency)
