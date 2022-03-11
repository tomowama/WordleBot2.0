

def vowelPatterns(words):
  
  
  
  vowels = ["a","e","i","u","o"]
  
  rawWordPatterns = []
  
  for word in words:
    currentVowelCount = 0
    currentVowelPlacement = [0] * 5
    #add = False
    for i in range(5):
      if word[i] in vowels:
        currentVowelCount +=1
        currentVowelPlacement[i] = word[i]
    if currentVowelCount >= 2:
      rawWordPatterns.append(currentVowelPlacement)
  
  
  
  numberedPatterns = [[],[]]
  for rawPattern in rawWordPatterns:
    seen = False 
    i = 0
    for pattern in numberedPatterns[0]:
      if rawPattern == pattern:
        numberedPatterns[1][i] +=1
        seen = True 
        break
      i+=1
    if not seen:
      numberedPatterns[0].append(rawPattern)
      numberedPatterns[1].append(1)
  
  
  # given vowel a in position 3, find the most likely pairs
  # x = 0
  # for pattern in numberedPatterns[0]:
  #   if pattern[3] == "a":
  #     print(f"out pattern is {pattern} and this shows up {numberedPatterns[1][x]} times")
  
  
  #   x+=1

  return numberedPatterns
    