import math
import time
from NumericCore import numericCore
from NumericStrCipher import numericStrCipher, multiNumericStrCipher
from MoraJai import MoraJai
from SolveMoraJai import solveMoraJai, solveMoraJaiPath, getMoraJaiAdjDict

class TestCase:
    def __init__(self, debug=False):
        self.debug = debug
        self.duration = 0.0
        self.total = 0
        self.succeeded = 0

    def prRed(self, skk): 
        """
        """
        print("\033[91m {}\033[00m" .format(skk))

    def prGreen(self, skk):
        """
        """
        print("\033[92m {}\033[00m" .format(skk))

    def prScore(self):
        """
        """
        print("{}/{} ({:%}) Passed over {:.2f}ms".format(self.succeeded, self.total, self.succeeded/self.total, self.duration/1000))

    def testCount(test):
        def wrapper(*args, **kwargs):
            args[0].total += 1
            val = test(*args, **kwargs)
            args[0].succeeded += val
            return val
        return wrapper
        
    @testCount
    def testFunc(self, func, args, output) -> bool:
        """
        """
        start = time.time()
        result = func(*args)
        delta = (time.time() - start) * 1000000
        self.duration += delta
        check = result == output
        stmt = "Ran func:{}({}) for {:.2f}µs, returned: {}; wanted: {}".format(func.__name__, args, delta, result, output)
        if self.debug:
            if check:
                self.prGreen(stmt)
            else:
                self.prRed(stmt)     
        return check
    
    @testCount
    def testResult(self, func, args, output, result) -> bool:
        """
        """
        start = time.time()
        func(*args)
        delta = (time.time() - start) * 1000000
        self.duration += delta
        check = result == output
        stmt = "Ran func:{}({}) for {:.2f}µs, returned: {}; wanted: {}".format(func.__name__, args, delta, result, output)
        if self.debug:
            if check:
                self.prGreen(stmt)
            else:
                self.prRed(stmt)     
        return check

def printBold(text):
    print("\033[1m{}\033[0m".format(text))

TestManager = TestCase(debug=True)
runTest = TestManager.testFunc
runResult = TestManager.testResult

def testNumericCore():
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

def testMoraJai():
    # MoraJai

    # Test hash/eq
    printBold("Test hash/eq")
    s = set()
    test = MoraJai()
    test2 = MoraJai()
    test3 = MoraJai(board=[[2,3,4],[2,4,6],[6,5,4]])
    test4 = MoraJai(board=[[2,3,4],[2,4,6],[6,5,4]], corners=[4,4,3,2])
    s.add(test)
    s.add(test2)
    s.add(test3)
    s.add(test4)
    assert(len(s) == 2)
    assert(test == test2)
    assert(hash(test) == hash(test2))
    assert(test3 == test4)
    assert(hash(test3) == hash(test4))

    # Test isSolved
    printBold("Test isSolved")
    solved = MoraJai([[2,1,2],[1,1,1],[2,1,2]], corners=[2,2,2,2])
    runTest(solved.isSolved, [], True)
    solved.board = [[1,2,3],[4,5,6],[7,8,9]]
    solved.corners = [1,3,7,9]
    runTest(solved.isSolved, [], True)
    solved.board = [[1,3,1],[4,5,6],[2,8,2]]
    solved.corners = [1,1,2,2]
    runTest(solved.isSolved, [], True)
    solved.board = [[1,3,1],[4,5,6],[1,8,2]]
    solved.corners = [1,1,1,2]
    runTest(solved.isSolved, [], True)
    unsolved = MoraJai([[1,2,1],[4,5,6],[7,8,9]], corners=[1,1,1,1])
    runTest(unsolved.isSolved, [], False)
    unsolved.board = [[1,1,1],[1,1,1],[1,1,2]]
    runTest(unsolved.isSolved, [], False)
    unsolved.board = [[1,1,1],[1,1,1],[2,1,1]]
    runTest(unsolved.isSolved, [], False)
    unsolved.board = [[1,1,2],[1,1,1],[1,1,1]]
    runTest(unsolved.isSolved, [], False)
    unsolved.board = [[2,1,1],[1,1,1],[1,1,1]]
    runTest(unsolved.isSolved, [], False)

    # Test Grey
    printBold("Test Grey")
    Box = MoraJai([[7,2,7],
                   [2,1,3],
                   [7,3,7]])
    pressTile = Box.pressTile
    runResult(pressTile, [1,1], MoraJai([[7,2,7],
                                         [2,1,3],
                                         [7,3,7]]), Box)

    # Test Black
    printBold("Test Black")
    Box.board = [[2,1,3],[2,1,3],[2,1,3]]

    runResult(pressTile, [0,0], MoraJai([[3,2,1],[2,1,3],[2,1,3]]), Box)
    runResult(pressTile, [1,0], MoraJai([[3,2,1],[3,2,1],[2,1,3]]), Box)
    runResult(pressTile, [2,0], MoraJai([[3,2,1],[3,2,1],[3,2,1]]), Box)
    runResult(pressTile, [0,1], MoraJai([[1,3,2],[3,2,1],[3,2,1]]), Box)
    runResult(pressTile, [0,2], MoraJai([[2,1,3],[3,2,1],[3,2,1]]), Box)

    # Test Green
    printBold("Test Green")
    Box.board = [[3,3,3],[3,3,1],[1,1,1]]

    runResult(pressTile, [0,0], MoraJai([[1,3,3],[3,3,1],[1,1,3]]), Box)
    runResult(pressTile, [2,2], MoraJai([[3,3,3],[3,3,1],[1,1,1]]), Box)
    runResult(pressTile, [1,1], MoraJai([[3,3,3],[3,3,1],[1,1,1]]), Box)
    runResult(pressTile, [0,1], MoraJai([[3,1,3],[3,3,1],[1,3,1]]), Box)
    runResult(pressTile, [0,2], MoraJai([[3,1,1],[3,3,1],[3,3,1]]), Box)
    runResult(pressTile, [1,0], MoraJai([[3,1,1],[1,3,3],[3,3,1]]), Box)
    Box.pressTile(1,2)
    Box.pressTile(2,0)
    Box.pressTile(2,1)
    runResult(pressTile, [1,1], MoraJai([[3,3,3],[3,3,1],[1,1,1]]), Box)

    #Test Pink
    printBold("Test Pink")
    Box.board = [[1,2,3],
                 [8,4,4],
                 [7,6,5]]

    runResult(pressTile, [1,1], MoraJai([[8,1,2],
                                         [7,4,3],
                                         [6,5,4]]), Box)
    runResult(pressTile, [2,2], MoraJai([[8,1,2],
                                         [7,5,4],
                                         [6,3,4]]), Box)
    pressTile(1,2)
    pressTile(1,2)
    pressTile(1,2)
    runResult(pressTile, [1,2], MoraJai([[8,2,4],
                                         [7,1,4],
                                         [6,5,3]]), Box)
    runResult(pressTile, [0,2], MoraJai([[8,1,4],
                                         [7,4,2],
                                         [6,5,3]]), Box)
    Box.board = [[4,2,3],
                 [8,4,4],
                 [4,6,5]]
    runResult(pressTile, [0,0], MoraJai([[4,8,3],
                                         [4,2,4],
                                         [4,6,5]]), Box)
    runResult(pressTile, [2,0], MoraJai([[4,8,3],
                                         [6,4,4],
                                         [4,2,5]]), Box)
    pressTile(0,0)
    pressTile(0,0)
    runResult(pressTile, [0,1], MoraJai([[8,4,4],
                                         [6,4,3],
                                         [4,2,5]]), Box)
    Box.board = [[8,2,3],
                 [4,5,7],
                 [1,4,5]]
    runResult(pressTile, [1,0], MoraJai([[1,8,3],
                                         [4,2,7],
                                         [4,5,5]]), Box)
    Box.board = [[8,2,3],
                 [4,5,7],
                 [1,4,5]]
    runResult(pressTile, [2,1], MoraJai([[8,2,3],
                                         [1,4,5],
                                         [5,4,7]]), Box)
    # Test Yellow
    printBold("Test Yellow")
    Box.board = [[8,2,5],
                 [1,5,7],
                 [5,1,3]]
    runResult(pressTile, [2,0], MoraJai([[8,2,5],
                                         [5,5,7],
                                         [1,1,3]]), Box)
    runResult(pressTile, [1,0], MoraJai([[5,2,5],
                                         [8,5,7],
                                         [1,1,3]]), Box)
    runResult(pressTile, [0,0], MoraJai([[5,2,5],
                                         [8,5,7],
                                         [1,1,3]]), Box)
    runResult(pressTile, [1,1], MoraJai([[5,5,5],
                                         [8,2,7],
                                         [1,1,3]]), Box)
    runResult(pressTile, [0,1], MoraJai([[5,5,5],
                                         [8,2,7],
                                         [1,1,3]]), Box)
    runResult(pressTile, [0,2], MoraJai([[5,5,5],
                                         [8,2,7],
                                         [1,1,3]]), Box)

    # Test Violet
    printBold("Test Yellow")
    Box.board = [[8,2,6],
                 [1,6,7],
                 [6,1,3]]
    runResult(pressTile, [2,0], MoraJai([[8,2,6],
                                         [1,6,7],
                                         [6,1,3]]), Box)
    runResult(pressTile, [1,1], MoraJai([[8,2,6],
                                         [1,1,7],
                                         [6,6,3]]), Box)
    runResult(pressTile, [0,2], MoraJai([[8,2,7],
                                         [1,1,6],
                                         [6,6,3]]), Box)
    runResult(pressTile, [1,2], MoraJai([[8,2,7],
                                         [1,1,3],
                                         [6,6,6]]), Box)

    # Test White
    printBold("Test White")
    Box.board = [[1,1,1],
                 [1,7,1],
                 [1,1,1]]
    runResult(pressTile, [1,1], MoraJai([[1,7,1],
                                         [7,1,7],
                                         [1,7,1]]), Box)
    Box.board = [[7,2,7],
                 [2,7,3],
                 [7,3,7]]
    runResult(pressTile, [1,1], MoraJai([[7,2,7],
                                         [2,1,3],
                                         [7,3,7]]), Box)
    Box.board = [[7,7,7],
                 [7,7,7],
                 [7,7,7]]
    runResult(pressTile, [1,1], MoraJai([[7,1,7],
                                         [1,1,1],
                                         [7,1,7]]), Box)
    runResult(pressTile, [1,1], MoraJai([[7,1,7],
                                         [1,1,1],
                                         [7,1,7]]), Box)
    runResult(pressTile, [0,0], MoraJai([[1,7,7],
                                         [7,1,1],
                                         [7,1,7]]), Box)
    runResult(pressTile, [2,2], MoraJai([[1,7,7],
                                         [7,1,7],
                                         [7,7,1]]), Box)
    runResult(pressTile, [0,2], MoraJai([[1,1,1],
                                         [7,1,1],
                                         [7,7,1]]), Box)
    runResult(pressTile, [2,0], MoraJai([[1,1,1],
                                         [1,1,1],
                                         [1,1,1]]), Box)

    # Test Red
    printBold("Test Red")
    Box.board = [[7,7,7],
                 [7,8,7],
                 [7,7,7]]
    runResult(pressTile, [1,1], MoraJai([[2,2,2],
                                         [2,8,2],
                                         [2,2,2]]), Box)
    runResult(pressTile, [1,1], MoraJai([[8,8,8],
                                         [8,8,8],
                                         [8,8,8]]), Box)
    Box.board = [[7,7,1],
                 [7,8,2],
                 [1,2,2]]
    runResult(pressTile, [1,1], MoraJai([[2,2,1],
                                         [2,8,8],
                                         [1,8,8]]), Box)
    
    # Test Orange
    printBold("Test Orange")
    Box.board = [[9,1,9],
                 [1,9,1],
                 [9,1,9]]
    runResult(pressTile, [1,1], MoraJai([[9,1,9],
                                         [1,1,1],
                                         [9,1,9]]), Box)
    runResult(pressTile, [0,0], MoraJai([[1,1,9],
                                         [1,1,1],
                                         [9,1,9]]), Box)
    runResult(pressTile, [0,2], MoraJai([[1,1,1],
                                         [1,1,1],
                                         [9,1,9]]), Box)
    runResult(pressTile, [2,0], MoraJai([[1,1,1],
                                         [1,1,1],
                                         [1,1,9]]), Box)
    runResult(pressTile, [2,2], MoraJai([[1,1,1],
                                         [1,1,1],
                                         [1,1,1]]), Box)
    Box.board = [[1,1,1],
                 [1,9,3],
                 [1,3,1]]
    runResult(pressTile, [1,1], MoraJai([[1,1,1],
                                         [1,9,3],
                                         [1,3,1]]), Box)
    Box.board = [[1,1,1],
                 [3,9,3],
                 [1,3,1]]
    runResult(pressTile, [1,1], MoraJai([[1,1,1],
                                         [3,3,3],
                                         [1,3,1]]), Box)
    Box.board = [[9,3,9],
                 [2,1,2],
                 [9,3,9]]
    runResult(pressTile, [0,0], MoraJai([[9,3,9],
                                         [2,1,2],
                                         [9,3,9]]), Box)
    runResult(pressTile, [0,2], MoraJai([[9,3,9],
                                         [2,1,2],
                                         [9,3,9]]), Box)
    runResult(pressTile, [2,0], MoraJai([[9,3,9],
                                         [2,1,2],
                                         [9,3,9]]), Box)
    runResult(pressTile, [2,2], MoraJai([[9,3,9],
                                         [2,1,2],
                                         [9,3,9]]), Box)
    
    Box.board = [[1,3,2],
                 [1,10,9],
                 [1,3,4]]
    runResult(pressTile, [1,2], MoraJai([[1,3,2],
                                         [1,10,9],
                                         [1,3,4]]), Box)
    Box.board = [[1,3,2],
                 [1,10,9],
                 [1,9,4]]
    runResult(pressTile, [2,1], MoraJai([[1,3,2],
                                         [1,10,9],
                                         [1,9,4]]), Box)
    Box.board = [[1,9,2],
                 [1,10,9],
                 [1,3,4]]
    runResult(pressTile, [0,1], MoraJai([[1,9,2],
                                         [1,10,9],
                                         [1,3,4]]), Box)
    Box.board = [[2,3,2],
                 [9,10,9],
                 [1,3,4]]
    runResult(pressTile, [0,1], MoraJai([[2,3,2],
                                         [9,10,9],
                                         [1,3,4]]), Box)

    # Test Blue
    printBold("Test Blue")
    Box.board = [[9,3,9],
                 [2,1,2],
                 [10,3,9]]
    runResult(pressTile, [2,0], MoraJai([[9,3,9],
                                         [2,1,2],
                                         [10,3,9]]), Box)
    Box.board = [[9,3,9],
                 [1,2,2],
                 [10,3,9]]
    runResult(pressTile, [2,0], MoraJai([[9,3,9],
                                         [1,2,2],
                                         [9,10,3]]), Box)
    Box.board = [[9,3,9],
                 [2,3,2],
                 [10,3,9]]
    runResult(pressTile, [2,0], MoraJai([[9,3,10],
                                         [2,3,2],
                                         [9,3,9]]), Box)
    Box.board = [[9,3,9],
                 [2,4,2],
                 [10,3,9]]
    runResult(pressTile, [2,0], MoraJai([[9,3,9],
                                         [3,2,2],
                                         [10,4,9]]), Box)
    Box.board = [[9,3,9],
                 [2,5,2],
                 [10,3,9]]
    runResult(pressTile, [2,0], MoraJai([[9,3,9],
                                         [10,5,2],
                                         [2,3,9]]), Box)
    Box.board = [[9,3,9],
                 [10,6,2],
                 [2,3,9]]
    runResult(pressTile, [1,0], MoraJai([[9,3,9],
                                         [2,6,2],
                                         [10,3,9]]), Box)
    Box.board = [[1,3,9],
                 [10,7,2],
                 [1,3,9]]
    runResult(pressTile, [1,0], MoraJai([[10,3,9],
                                         [1,7,2],
                                         [10,3,9]]), Box)
    Box.board = [[1,7,9],
                 [10,8,5],
                 [1,2,9]]
    runResult(pressTile, [1,0], MoraJai([[1,2,9],
                                         [10,8,5],
                                         [1,8,9]]), Box)
    Box.board = [[1,3,2],
                 [10,9,10],
                 [1,3,4]]
    runResult(pressTile, [1,0], MoraJai([[1,3,2],
                                         [1,9,10],
                                         [1,3,4]]), Box)
    runResult(pressTile, [1,2], MoraJai([[1,3,2],
                                         [1,9,10],
                                         [1,3,4]]), Box)
    Box.board = [[1,3,2],
                 [10,10,1],
                 [5,3,4]]
    runResult(pressTile, [1,0], MoraJai([[1,3,2],
                                         [10,10,1],
                                         [5,3,4]]), Box)

    TestManager.prScore()

def testMoraJaiSolve():
    i = 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[3,2,3],[2,2,2],[3,5,3]],[2,2,2,2]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[1,3,1],[9,8,9],[7,3,2]],[8,8,8,8]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[2,5,1],[5,3,5],[1,5,2]],[5,5,5,5]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[5,6,5],[3,8,2],[6,6,6]],[6,6,6,6]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[9,2,9],[9,9,9],[6,3,6]],[9,9,9,9]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[5,5,5],[7,4,7],[1,1,1]],[7,7,7,7]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[4,4,1],[1,1,1],[9,9,9]],[4,4,4,4]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    with open("SolveMoraJaiSol/Sol" + str(i) + ".out", "w") as f:
        for box in getMoraJaiAdjDict(MoraJai([[3,1,3],[1,9,9],[1,2,6]],[3,3,3,3]))[1]:
            for b in box:
                f.write(str(b))
            f.wirte("\n")
    i += 1
    # solveMoraJaiPath(MoraJai([[3,2,3],[2,2,2],[3,5,3]],[2,2,2,2]))
    # solveMoraJaiPath(MoraJai([[1,3,1],[9,8,9],[7,3,2]],[8,8,8,8]))
    # solveMoraJaiPath(MoraJai([[2,5,1],[5,3,5],[1,5,2]],[5,5,5,5]))
    # solveMoraJaiPath(MoraJai([[5,6,5],[3,8,2],[6,6,6]],[6,6,6,6]))
    # solveMoraJaiPath(MoraJai([[9,2,9],[9,9,9],[6,3,6]],[9,9,9,9]))
    # solveMoraJaiPath(MoraJai([[5,5,5],[7,4,7],[1,1,1]],[7,7,7,7]))
    # solveMoraJaiPath(MoraJai([[4,4,1],[1,1,1],[9,9,9]],[4,4,4,4]))
    # solveMoraJaiPath(MoraJai([[3,1,3],[1,9,9],[1,2,6]],[3,3,3,3]))

testMoraJaiSolve()