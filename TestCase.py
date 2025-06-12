import math
from NumericCore import numericCore
from NumericStrCipher import numericStrCipher, multiNumericStrCipher

class TestCase:
    def __init__(self):
        self.total = 0
        self.succeeded = 0

    def prRed(self, skk): print("\033[91m {}\033[00m" .format(skk))

    def prGreen(self, skk): print("\033[92m {}\033[00m" .format(skk))

    def testCount(test):
        def wrapper(self, func, input, output):
            self.total += 1
            val = test(self, func, input, output)
            self.succeeded += val
            return val
        return wrapper
        
    @testCount
    def testFunc(self, func, input, output) -> bool:
        result = func(input)
        check = result == output
        stmt = "Ran func:{}({}), returned: {}; wanted: {}".format(func, input, result, output)
        if check:
            self.prGreen(stmt)
        else:
            self.prRed(stmt)     
        return check

TestManager = TestCase()
runTest = TestManager.testFunc

# NumericCore
runTest(numericCore, "86455", 18)
runTest(numericCore, "864555", 5)
runTest(numericCore, "864555245691", 4)
runTest(numericCore, "12335084", math.inf)
runTest(numericCore, "12", math.inf)
runTest(numericCore, "", math.inf)
runTest(numericCore, "12094082", 336)
runTest(numericCore, "0984", math.inf)
runTest(numericCore, "09842453", math.inf)
runTest(numericCore, "9827648462837", 125) # NOTE: due to floating point numbers, the "correct" numeric core is 982764 ÷ 84 − 6283 × 7 = 37916 -> 3 ÷ 7 × 91 − 6 = 33
runTest(numericCore, "982764846283720527423849723626427923487483743473647", 11) # NOTE: due to the openess of Numeric Core, you can either look for the smallest result for all possible branches or you go through each layers smallest and compute.
runTest(numericCore, "0984", math.inf)

runTest(numericCore, "12 32 4 2", 94)
runTest(numericCore, "0 32 4 2", math.inf)
runTest(numericCore, "12 02 4 22", 2)

# NumericStrCipher
runTest(numericStrCipher, "Pigs", "s")
runTest(numericStrCipher, "SAnd", "t")
runTest(numericStrCipher, "MAIL", "i")
runTest(numericStrCipher, "Date", "l")
runTest(numericStrCipher, "head", "l")
runTest(multiNumericStrCipher, ["Pigs", "sand", "MAIL", "Date", "head"], "still")
print("{}/{} = {:%} Passed".format(TestManager.succeeded, TestManager.total, TestManager.succeeded/TestManager.total))