import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            CORNERS =[(0,0),(0,7),(7,0),(7,7)]
            if not self.board[i][j] and (i,j) not in CORNERS:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        arr = set()
        for i in self.cells:
            if i == True:
                arr.add(i)
        return arr

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        arr = set()
        for i in self.cells:
            if i == False:
                arr.add(i)
        return arr

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        i,j = cell
        self.cells[i][j] = True

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        i,j = cell
        self.cells[i][j] = False


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = {}

        # Stuff to use
        self.forcedMoves = set()
        self.nextMove = []
        self.depth = 0

        self.map = set()
        for i in range(height):
            for j in range(height):
                self.map.add((i,j))
    
    def neighboursthatarentflaggedoramove(self,cell):
        arr = self.neighbours(cell)
        n = 0
        for i in arr:
            if i not in self.moves_made and i in self.mines:
                print('')

    # All neighbours that are hidden and not a mine
    def hiddenneighboursNotMine(self,cell):
        n = 0
        arr = self.neighbours(cell)
        for i in arr:
            if i not in self.moves_made and i not in self.mines:
                n += 1
        return n

    # All neighbours that are hidden
    def hiddenneighbours(self,cell):
        n = 0
        arr = self.neighbours(cell)
        for i in arr:
            if i not in self.moves_made:
                n += 1
        if n != 0:
            return n
        return -1

    # All neighbours
    def neighbours(self, cell):
        """Returns a list of neighbouring cells for some cell."""
        arr = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    arr.append((i,j))
        return arr
    
    # All neighbours that are bombs
    def flaggedneighbours(self,cell):
        """Returns how many neighbouring cells are flagged as a mine."""
        closeMines = 0
        arr = self.neighbours(cell)
        for i in arr:
            if i in self.mines:
                closeMines += 1
        return closeMines
    

    def mineProbe(self,tile,depth):
        """Looks for a new safe tile among the neighbouring cells of a specific cell."""
        if depth > 3:
            return
        neighbours = self.neighbours(tile)
        for cell in neighbours:
            if cell in self.knowledge:
                count = self.knowledge[cell]
                closeFlags = self.flaggedneighbours(cell)
                if count == closeFlags:
                    for i in self.neighbours(cell):
                        if i not in self.mines:
                            self.mark_safe(i)
        depth += 1
        self.mineProbe(cell,depth)
    
    def tileProbe(self,depth):
        """Looks for safe tiles among the neighbouring cells of found mines."""
        if depth > 3:
            return
        temporaryMines = set()
        for temp in self.mines:
            temporaryMines.add(temp)

        for cell in temporaryMines:
            neighbours = self.neighbours(cell)
            for i in neighbours:
                if i in self.knowledge:
                    count = self.knowledge[i]
                    closeFlags = self.flaggedneighbours(i)
                    if count == closeFlags:
                        for j in self.neighbours(i):
                            if j not in self.mines:
                                self.mark_safe(i)
        depth += 1
        self.tileProbe(depth)
    

    def generalProbe(self,depth):
        """"""
        if depth > 3:
            return
        for cell in self.moves_made:
            count = self.knowledge[cell]
            closeHiddens = self.hiddenneighbours(cell)
            if count == closeHiddens:
                for newCell in self.neighbours(cell):
                    if newCell not in self.safes:
                        self.mark_mine(newCell)
                        self.mineProbe(newCell,0)
        depth += 1
        self.generalProbe(depth)

    def mark_mine(self, cell):
        self.mines.add(cell)
        if cell in self.safes:
            self.safes.remove(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        if cell in self.mines:
            self.mines.remove(cell)


    def add_knowledge(self, cell, count):
        self.knowledge[cell] = count
        self.moves_made.add(cell)
        self.mark_safe(cell)

        self.mineProbe(cell,0)
        self.tileProbe(0)
        self.generalProbe(0)

    def make_safe_move(self):
        # Force moves with 0's first. This isn't very efficient at all, but,
        # It really bothered me that the 0 tiles weren't being done first, the same as normal mine sweeper.
        for cell in self.moves_made:
            if self.knowledge[cell] == 0:
                for k in self.neighbours(cell):
                    if k not in self.knowledge:
                        return k
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

    def make_random_move(self):
        # Genereate a board
        board = []
        for i in range(8):
            for j in range(8):
                board.append((i, j))

        # Try a tile with no neighbours, it's the highest probability of being safe.
        for i in board:
            if i not in self.moves_made:
                tempBool = True
                for j in self.neighbours(i):
                    if j in self.knowledge:
                        tempBool = False
                        break
                if tempBool == True:
                    return i

        
        move = None
        best = -3

        # Bomb probability:
        # A played cell contains a count of how many mines are neighbouring it. The probability of there being a mine among its neighbouring cells
        # is self.knowledge[cell] / (neighbouring cells not in self.moves_made + neighbouring cells not in self.mines)
        # The acceptable limit here is 2.
        for i in self.moves_made:
            k = self.knowledge[i]
            bombsNear = self.flaggedneighbours(i)
            if (-1 * (k + bombsNear)) > best:
                best = (-1 * (k + bombsNear))
                tempNeighbours = self.neighbours(i)
                for j in tempNeighbours:
                    if j not in self.moves_made and j not in self.mines:
                        move = j
                        break
        if move is not None:
            return move
        else:
            # Check if game win
            temporaryArray = []
            num_mines = 0
            for i in board:
                if i not in self.moves_made:
                    temporaryArray.append(i)
                    num_mines += 1
            if num_mines == 8:
                self.mines = set()
                for i in temporaryArray:
                    self.mines.add(i)
                return None

            # Actual Random bomb
            tempVar = 0
            while True:
                if tempVar > 80:
                    if (i,j) not in self.moves_made:
                        return (i,j)
                i = random.randrange(8)
                j = random.randrange(8)
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    return (i,j)
                tempVar += 1
        return None