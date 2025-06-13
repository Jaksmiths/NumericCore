import operator
import math

def numericCore(digits):
    """
    given a number with 4 or more digits, split digits into 4 numbers without changing the order
    apply operators - * / in the order that produces the smallest whole (natural) result.
    If result has more than 3 digits, repeat from the top.
    Final number with less than four digits is the numeric core of the larger number

    Args:
        digits (str): a string of numbers/digits either spaced into 4 numbers or one whole number.
    
    Return:
        int: the Numeric Core result of the digits
    """
    result = math.inf
    # first number is + (addition)
    operands = [[operator.sub, operator.mul, operator.truediv],
                [operator.sub, operator.truediv, operator.mul],
                [operator.mul, operator.sub, operator.truediv],
                [operator.mul, operator.truediv, operator.sub],
                [operator.truediv, operator.mul, operator.sub],
                [operator.truediv, operator.sub, operator.mul],]
    numSize = len(digits)

    def checkLeadingZero(digits, frontIndx, endIndex):
        return digits[frontIndx] == "0" and len(digits[frontIndx:endIndex]) > 1
    
    def computeNumericCore(numA, numB, numC, numD, leadingZero=True):
        result = [math.inf]
        for op in operands:
            # prevent division by 0
            if leadingZero:
                if(op[0] == operator.truediv and numB == 0):
                    continue
                if(op[1] == operator.truediv and numC == 0):
                    continue
                if(op[2] == operator.truediv and numD == 0):
                    continue

            numCore = op[2](op[1](op[0](numA, numB), numC), numD)
            if numCore % 1 == 0 and numCore > 0:
                result.append(int(numCore))
        return result


    if len(digits.split(" ")) == 4:
        sections = list(map(int, digits.split(" ")))
        return min(result, *computeNumericCore(*sections, leadingZero=False))

    # split a num into 4 sections: a, b, c, d
    for a in range(1, numSize-2):
        for b in range(a+1, numSize-1):
            for c in range(b+1, numSize):
                    # skip if leading zero
                    if (checkLeadingZero(digits, 0, a) or checkLeadingZero(digits, a, b) 
                        or checkLeadingZero(digits, b, c) or checkLeadingZero(digits, c, numSize)):
                        continue

                    numA = int(digits[0:a])
                    numB = int(digits[a:b])
                    numC = int(digits[b:c])
                    numD = int(digits[c:numSize])

                    result = min(result, *computeNumericCore(numA, numB, numC, numD))

    if result != math.inf and len(str(int(result))) > 3:
        result = numericCore(str(int(result)))

    return result