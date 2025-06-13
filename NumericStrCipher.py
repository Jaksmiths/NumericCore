import string
from NumericCore import numericCore

def numericStrCipher(word):
    """
    Given a 4 letter word, converts them into their numerical position in the alphabet. Then performs
    a Numeric Core calculation and using the result to return the letter at the position of the Numeric Core.

    Args:
        word (str): 
    
    Return:
        str: letter at the position of the numeric core, o/w "*" if invalid/impossible
    """
    if len(word) != 4: return "*"
    letterToNum = dict([(string.ascii_lowercase[i], i+1) for i in range(len(string.ascii_lowercase))])
    word = word.lower()
    cipher = ""
    for letter in word[:-1]:
        cipher += str(letterToNum[letter]) + " "
    cipher += str(letterToNum[word[-1]])
    numCore = numericCore(cipher)
    return "*" if numCore-1 > 25 else string.ascii_lowercase[numCore-1]

def multiNumericStrCipher(wordList):
    """
    Preforms multiple numericStrCipher operations and concatenates the results together.

    Args:
        wordList (List): List of 4 letter words
    
    Return:
        str: concatenated results of each word's numericStrcipher()
    """
    result = ""
    for word in wordList:
        result += numericStrCipher(word)
    return result