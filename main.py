import random
import sys, os
import vowel

#######################
#######################
###      ADD A VOWEL PATTERN CHECKER     ####
#######################
#######################


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
    file = open("WordleAnswers.txt", "r")
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


def optimalGuess(words, numberedPatterns, letterStates):
    mostCommonLetters = []
    for i in range(5):
        mostCommonLetters.append(mostCommonLetterByPosition(words, i))
    bestGuess = ''
    max = 0
    roughlyTiedWords = []
    vowels = ["a", "i", "e", "o","u"]

    #print(f"letter values are {mostCommonLetters}")

    for word in words:
        sum = 0
        i = 0
        guessedThisRound = []
        for letter in word:
            if letter not in guessedThisRound:
                sum += mostCommonLetters[i][ord(letter) - 97]
            i += 1
            guessedThisRound.append(letter)
        if sum - 10 > max:
            roughlyTiedWords = [word]
            max = sum
            bestGuess = word
        elif sum in range(max, max + 10):
            max = sum
            bestGuess = word
            roughlyTiedWords.append(word)
        elif sum in range(max - 10, max):
            roughlyTiedWords.append(word)



    ####### THIS CURRENTLY MAKES THE BOT SLOWER. NEED TO FIX IT SO THAT IT ONLY CHECKS VOWELS IF WE HAVE ONE OF THEM BEING GREEN. 
    greenVowelPosition = [0] *5
    numV = 0
    for greenPair in letterStates[0]:
      if greenPair[0] in vowels:
        greenVowelPosition[greenPair[1]] = greenPair[0]
        numV += 1
    if numV == 1:
      for word in roughlyTiedWords:
        vowelCount = 0
        vowelPattern = [0] * 5
        i = 0
        max =0
        for letter in word:
          if letter in vowels:
            vowelCount +=1
            vowelPattern[i] = letter
          i +=1
        if vowelCount >=2:
          # now we want to check which pattern our word is
  
  
  
          ## NEED TO ADD  SO THAT WE CHECK TO MAKE SURE THAT ONE OF THESE VOWELS IS GREEN. 
          x = 0
          for numberedPat in numberedPatterns[0]:
            if numberedPat == vowelPattern:
              check = numberedPatterns[1][x]
              if check >= max:
                bestGuess = word
                max = check 
            x+=1


        ### NEED TO MAKE SURE THAT WE ARE ADDING A CONSTANT TO THE BEST GUESS VALUE INSTEAD OF JUST MAKING THE BEST GUESS THE ONE WITH THE BEST VOWEL PLACEMENT. 
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


def gameLoop(words, targetWord, letterStates, numberedPatterns):
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
        guessWord = optimalGuess(words, numberedPatterns, letterStates)
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


def runner(runs):
    words = wordList()

    letterStates = [[], [], []]
    numberedPatterns = vowel.vowelPatterns(words)

    wins = 0
    losses = 0
    roundsSum = 0
    loseWords = []
    fastWinWords = []
    distribution = [0] * 7
    for i in range(runs):
        targetWord = random.choice(words)
        blockPrint()
        gameInfo = gameLoop(words, targetWord, letterStates, numberedPatterns)
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

    print(f"we won {wins} times. With a winrate of {wins/runs}")
    print("")
    print(f"we lost {losses} times. With a lossrate of {losses/runs}")
    print("")
    print(f"the average round number was {roundsSum/runs}")
    print('')
    print(f"we lost on the words {loseWords}")
    print('')
    print(f"fast winning words are {fastWinWords}")
    print('')
    distribution.pop(0)
    print(f"our distribution is {distribution}")


#runner(1000)

#gameLoop(wordList(), "union", [[],[],[]])

# test = ['amaze', 'awake', 'chafe', 'inane', 'peace', 'quake']

# print(optimalGuess(test))
#words = updateWordList(words, letterStates, guessWord)

# for word in wordList():
#   checkLetters=['l', 'e', 't']

#   if 'l' in word and 'e' in word

# print(optimalGuess(updateWordList(wordList(), [[['t', 3],['h',4], ['o',1]], [], ['c','a','r','e','s', 'u']], "tooth")))


def onlineGameLoop(words, letterStates):
    done = False
    round = 1

    while not done:
        print(f"It is round {round}")
        print('')
        print('-----------------')
        print('')
        guessWord = optimalGuess(words)
        print(f"guess word is {guessWord}")
        #correctString = correctStringGen(guessWord, targetWord)
        correctString = input("Enter the correct string ")
        letterStates = inputReader(guessWord, correctString)

        if len(words) < 50:
            print("Remaing Words are")
            print('')
            print('-----------------')
            print('')
            print(words)

        # print('')
        # print(f"there are {len(words)} remaining")
        # print(f"Computers guess is {guessWord}")
        # print(f"yellow letters are {letterStates[1]}")
        # print(f"green letters are {letterStates[0]}")
        # print('')
        # print('-----------------')
        # print('')

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

numberedPatterns = vowel.vowelPatterns(words)
print(numberedPatterns)


# onlineGameLoop(words, letterStates)

#targetWord = random.choice(words)

#gameLoop(words, targetWord, letterStates, numberedPatterns)


runner(1000)