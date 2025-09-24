
class MoraJai:
    def __init__(self, board=[[1,1,1],[1,7,1],[1,1,1]], corners=[7,7,7,7]):
        """
        Build a Mora Jai board with given tiles and corners.

        args:
        board (list(list)): 3x3 grid of colored tiles, described below  
            1	Grey	No effect  
            2	Black	Horizontal rotation - shifts entire row to the right, and the right-most tile to the left  
            3	Green	Swaps with the opposite tile on the far side of the box; no effect in the center  
            4	Pink	All adjacent tiles (including diagonally-adjacent tiles) rotate around the pressed tile clockwise, teleporting around to the next valid position when they would otherwise up outside the box edge  
            5	Yellow	Tile moves north (Swaps place with the tile above); no effect on the top row  
            6	Violet	Tile moves south (Swaps place with the tile bellow); no effect on the bottom row  
            7	White	Turns itself grey, all adjacent grey tiles white, and all adjacent white tiles grey  
            8	Red	    Turns all white tiles black, and all black tiles red  
            9	Orange	If the majority of the adjacent tiles share a color, then the pressed tile will change to that color  
            10	Blue	Behaves the same way as the center tile; No effect if the center tile is blue  

        corners (list): the 4 corners (topLeft, topRight, botLeft, botRight) of the board which can be the colors 2-10
        """
        self.board = board
        self.corners = corners

    def pressTile(self, row, col):
        if self.board[row][col] == 10:
            # pressBlue()
            color = self.board[1][1]
        else:
            color = self.board[row][col]

        match color:
            case 2:
                self.pressBlack(row)
            case 3:
                self.pressGreen(row, col)
            case 4:
                self.pressPink(row, col)
            case 5:
                self.pressYellow(row, col)
            case 6:
                self.pressViolet(row, col)
            case 7:
                self.pressWhite(row, col)
            case 8:
                self.pressRed()
            case 9:
                self.pressOrange(row, col)

    def pressBlack(self, row):
        self.board[row][0], self.board[row][1], self.board[row][2] = self.board[row][2], self.board[row][0], self.board[row][1] 
    
    def pressGreen(self, row, col):
        self.board[row][col], self.board[abs(row-2)][abs(col-2)] = self.board[abs(row-2)][abs(col-2)] , self.board[row][col]

    def pressPink(self, row, col):
        prev = -1
        head = -1

        # top
        currR = row-1
        for currC in range(col-1, col+1):
            if self.inRange(currR,currC):
                if head == -1:
                    head = (currR,currC)
                self.board[currR][currC], prev = prev, self.board[currR][currC]

        # right
        currC = col+1
        for currR in range(row-1, row+1, 1):
            if self.inRange(currR,currC):
                if head == -1:
                    head = (currR,currC)
                self.board[currR][currC], prev = prev, self.board[currR][currC]

        # bot
        currR = row+1
        for currC in range(col+1, col-1, -1):
            if self.inRange(currR,currC):
                if head == -1:
                    head = (currR,currC)
                self.board[currR][currC], prev = prev, self.board[currR][currC]

        # left
        currC = col-1
        for currR in range(row+1, row-1, -1):
            if self.inRange(currR,currC):
                if head == -1:
                    head = (currR,currC)
                self.board[currR][currC], prev = prev, self.board[currR][currC]

        self.board[head[0]][head[1]] = prev

    def pressYellow(self, row, col):
        if self.inRange(row-1, col):
            self.board[row][col], self.board[row-1][col] = self.board[row-1][col], self.board[row][col]
            
    def pressViolet(self, row, col):
        if self.inRange(row+1, col):
            self.board[row][col], self.board[row+1][col] = self.board[row+1][col], self.board[row][col]

    def pressWhite(self, row, col):
        # could hardcode for better performance
        dir = [(1,0),(-1,0),(0,1),(0,-1)]
        color = self.board[row][col]
        for d in dir:
            r = row + d[0]
            c = col + d[1]
            if self.inRange(r, c):
                if self.board[r][c] == 1:
                    self.board[r][c] = color
                elif self.board[r][c] == color:
                    self.board[r][c] = 1
        self.board[row][col] = 1

    def pressRed(self):
        # could hardcode for better performance
        for r in range(3):
            for c in range(3):
                match self.board[r][c]:
                    case 7:
                        self.board[r][c] = 2
                    case 2:
                        self.board[r][c] = 8

    def pressOrange(self, row, col):
        dir = [(1,0),(-1,0),(0,1),(0,-1)]
        majority = self.board[row][col]
        count = 0
        total = 0
        for d in dir:
            r = row + d[0]
            c = col + d[1]
            if self.inRange(r, c):
                total += 1
                if count == 0:
                    count = 1
                    majority = self.board[r][c]
                elif self.board[r][c] == majority:
                    count += 1
                else:
                    count -= 1

        count = 0
        for d in dir:
            r = row + d[0]
            c = col + d[1]
            if self.inRange(r, c):
                if self.board[r][c] == majority:
                    count += 1

        if count >= 2 and count > (total // 2):
            self.board[row][col] = majority

    def inRange(self, r, c) -> bool:
        return r < 3 and r >= 0 and c < 3 and c >= 0

    def isSolved(self) -> bool:
        return (
            self.corners[0] == self.board[0][0] and
            self.corners[1] == self.board[0][2] and
            self.corners[2] == self.board[2][0] and
            self.corners[3] == self.board[2][2]
        )

    def __str__(self):
        # return str(self.board)
        return (
            "[" + str(self.board[0]) + "\n " + str(self.board[1]) + "\n " + str(self.board[2]) + "]"
        )

    def __eq__(self, other):
        return (
            self.board[0][0] == other.board[0][0] and 
            self.board[0][1] == other.board[0][1] and 
            self.board[0][2] == other.board[0][2] and 
            self.board[1][0] == other.board[1][0] and 
            self.board[1][1] == other.board[1][1] and 
            self.board[1][2] == other.board[1][2] and
            self.board[2][0] == other.board[2][0] and 
            self.board[2][1] == other.board[2][1] and 
            self.board[2][2] == other.board[2][2]
        )
    
    def __hash__(self):
        return hash(
            (self.board[0][0],self.board[0][1],self.board[0][2],
             self.board[1][0],self.board[1][1],self.board[1][2],
             self.board[2][0],self.board[2][1],self.board[2][2])
        )