import operator
import math

def numericCore(digits):
    """
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

                    for op in operands:
                        # prevent division by 0
                        if(op[0] == operator.truediv and numB == 0):
                            continue
                        if(op[1] == operator.truediv and numC == 0):
                            continue
                        if(op[2] == operator.truediv and numD == 0):
                            continue

                        numCore = op[2](op[1](op[0](numA, numB), numC), numD)
                        if numCore % 1 == 0 and numCore > 0:
                                # print("{} | {} {} {} {}".format(numCore, numA, numB, numC, numD))
                            result = min(result, int(numCore))

    if result != math.inf and len(str(int(result))) > 3:
        result = numericCore(str(int(result)))

    return result

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))

def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

def testFunc(func, input, output) -> bool:
    result = func(input)
    check = result == output
    if check:
        prGreen("Ran func:{}({}), returned: {}; wanted: {}".format(func, input, result, output))
    else:
        prRed("Ran func:{}({}), returned: {}; wanted: {}".format(func, input, result, output))     
    return check

testFunc(numericCore, "86455", 18)
testFunc(numericCore, "864555", 5)
testFunc(numericCore, "864555245691", 4)
testFunc(numericCore, "12335084", math.inf)
testFunc(numericCore, "12", math.inf)
testFunc(numericCore, "", math.inf)
testFunc(numericCore, "12094082", 336)
testFunc(numericCore, "0984", math.inf)
testFunc(numericCore, "09842453", math.inf)
testFunc(numericCore, "9827648462837", 125) # NOTE: due to floating point numbers, the "correct" numeric core is 982764 ÷ 84 − 6283 × 7 = 37916 -> 3 ÷ 7 × 91 − 6 = 33
testFunc(numericCore, "982764846283720527423849723626427923487483743473647", 11)