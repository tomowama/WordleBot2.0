import main

words = main.wordList()

vowels = ["a","e","i","u","o"]

rawWordPatterns = []

for word in words:
  currentVowelCount = 0
  currentVowelPlacement = [0] * 5
  add = False
  for i in range(5):
    if word[i] in vowels:
      currentVowelCount +=1
      currentVowelPlacement[i] = word[i]
  if currentVowelCount >= 2:
    rawWordPatterns.append(currentVowelPlacement)


print(rawWordPatterns)

for pattern in rawWordPatterns:
  for i in range(5):
    
  