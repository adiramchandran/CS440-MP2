# -*- coding: utf-8 -*-
import numpy as np
#               F  I  L  N  P  T  U  V  W  X  Y  Z
orientations = [8, 2, 8, 8, 8, 4, 4, 4, 4, 1, 8, 4]
final_board = None
const_choices = {}
const_constraints = {}

def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is
    the coordinate of the upper left corner of pi in the board (lowest row and column index
    that the tile covers).

    -Use np.flip and np.rot90 to manipulate pentominos.

    -You can assume there will always be a solution.
    """

    # set up bipartite graph to begin (one for constraint, the other for all possible choices)
    board[board==1] = float('inf')

    choices = {}                    # maps from (pentomino idx, unique orientation) to # of different coordinates an orientation can go
    constraints = {}                # maps from potential top left (row, col) coordinate to list of tuples (pent idx, unique orientation)

    for pent in pents:
        pent_idx = get_pent_idx(pent)
        for orient in findOrientations(pent, pent_idx):                 # each orientation in the orientation list for a certain pentonmino
            for row in range(board.shape[0]):
                for col in range(board.shape[1]):
                    if can_add_pentomino(board, orient, (row, col)):    # check if we can add a pentomino starting at the given (row, col)
                        # if we can add pent, then add to constraints dict
                        if (row, col) not in constraints.keys():
                            constraints[(row,col)] = []
                        constraints[(row, col)].append((pent_idx, orient))

                        choice = (pent_idx, orient)
                        if choice not in choices.keys():
                            choices[choice] = []

                        choices[choice].append((row, col))

    # now we should have our choices and constraints dictionaries filled and we can backtrack



def alg_x(board, choices, constraints, pents):
    """
    base cases:
    1) constraints[(row, col)] is empty list (invalid so return false)
    2) all choices[orient] for one pent idx is empty (no more places to place a certain pentomino), return false
    3) if it's solved (choices and constraints are both empty), return true
    """

    """
    def _solve(self):
        if not self.unsatisfied:
            # No remaining unsatisfied constraints.
            yield list(self.solution)
            return

        # Pick the constraint with the fewest remaining choices
        # (Knuth's "S heuristic").
        best = min(self.unsatisfied, key=lambda j:len(self.choices[j]))
        choices = list(self.choices[best])
        if self.random:
            shuffle(choices)

        # Try each choice in turn and recurse.
        for i in choices:
            self._choose(i)
            yield from self._solve()
            self._unchoose(i)

    def _choose(self, i):
        Make choice i; mark constraints satisfied; and remove any
        choices that clash with it.

        self.solution.append(i)
        for j in self.constraints[i]:
            self.unsatisfied.remove(j)
            for k in self.choices[j]:
                for l in self.constraints[k]:
                    if l != j:
                        self.choices[l].remove(k)

    def _unchoose(self, i):
        Unmake choice i; restore constraints and choices.
        last = self.solution.pop()
        assert i == last
        for j in self.constraints[i]:
            self.unsatisfied.add(j)
            for k in self.choices[j]:
                for l in self.constraints[k]:
                    if l != j:
                        self.choices[l].add(k)
    """
    
    for coord in constraints.keys():
        

    # base case, once every constraint has been satisfied
    if (len(constraints) == 0):
        return assignment

    # var is a constraint (could be pentomino or (row,col) of board)
    var = getNextVar(constraints)
    for choice in constraints.get(var):

        if var not in temp:
            temp[var] = []

        coords = getCoords(board)
        orient = choice[1]
        # add pentomino to the board and assignment
        add_pentomino(board, orient, coords)
        tuple = (orient, coords)
        assignment.append(tuple)

        # temporarily save (key,val)
        temp[var].append(choice)
        # remove from constraints list
        if (len(constraints[var]) == 0):
            del constraints[var]
        else:
            constraints[var].remove(choice)

        backtrack(constraints, assignment, temp)
    # for val in orderValues(var, assignment, pents):

    
    

# find next pentomino
def getNextVar(list):
    # sort based on MRV
    list = sorted(list, key=lambda key: len(list.get(key)))

    if len(list) != 0:
        return list[0]

    return None

def mrvSort(elem):
    print(self.get(elem))
    return len(elem[1])


def orderValues(var, assignment, pents):
    return None

def findOrientations(pent, pent_idx):
    positions = []
    numofOrient = orientations[pent_idx]

    # F,L,N,P,Y (4 rotations, 4 flipped)
    if numofOrient == 8:
        for i in range(4):
            positions.append(np.rot90(pent, i))
        pent = np.flip(pent, 0)
        for i in range(4):
            positions.append(np.rot90(pent, i))

    elif numofOrient == 4:
        # Z (1 rotation, 1 flipped)
        if pent_idx == len(orientations) - 1:
            for i in range(2):
                positions.append(np.rot90(pent, i))
            pent = np.flip(pent, 0)
            for i in range(2):
                positions.append(np.rot90(pent, i))

        # T, U, V, W (4 rotations)
        else:
            for i in range(4):
                positions.append(np.rot90(pent, i))
    # I (2 rotations)
    elif numofOrient == 2:
        for i in range(2):
            positions.append(np.rot90(pent, i))
    # X (no rotations/flips)
    else:
        positions.append(pent)

    return positions


def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1


def getCoords(board):
    """
    Returns the next available square on the board.
    """
    found = False
    coord = (0,0)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == -1:
                found = True
                coord = (i, j)
                break
        if found == True:
            break
    if found == False:
        return -1
    return coord


def can_add_pentomino(board, pent, coord):
    """
    Checks if the pentomino can be placed at the coordinate on the board.
    """
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]:
                    return False
                if board[coord[0]+row][coord[1]+col] != -1: # Overlap
                    return False
    return True


def add_pentomino(board, pent, coord):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the board and coord[1] is the lowest
    column index.
    """
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]:
                    print("error1")
                    remove_pentomino(board, get_pent_idx(pent))
                    return False
                if board[coord[0]+row][coord[1]+col] != -1: # Overlap
                    print("error")
                    remove_pentomino(board, get_pent_idx(pent))
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True

def remove_pentomino(board, pent_idx):
    board[board==pent_idx+1] = -1












# # -*- coding: utf-8 -*-
# import numpy as np
# #               F  I  L  N  P  T  U  V  W  X  Y  Z
# orientations = [8, 2, 8, 8, 8, 4, 4, 4, 4, 1, 8, 4]

# def solve(board, pents):
#     """
#     This is the function you will implement. It will take in a numpy array of the board
#     as well as a list of n tiles in the form of numpy arrays. The solution returned
#     is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
#     where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
#     the coordinate of the upper left corner of pi in the board (lowest row and column index 
#     that the tile covers).
    
#     -Use np.flip and np.rot90 to manipulate pentominos.
    
#     -You can assume there will always be a solution.
#     """
    
#     raise NotImplementedError
