import string
from NumericCore import numericCore

def numericStrCipher(word):
    if len(word) != 4: return -1
    letterToNum = dict([(string.ascii_lowercase[i], i+1) for i in range(len(string.ascii_lowercase))])
    word = word.lower()
    cipher = ""
    for letter in word[:-1]:
        cipher += str(letterToNum[letter]) + " "
    cipher += str(letterToNum[word[-1]])
    numCore = numericCore(cipher)
    return string.ascii_lowercase[numCore-1]

def multiNumericStrCipher(wordlist):
    result = ""
    for word in wordlist:
        result += numericStrCipher(word)
    return result