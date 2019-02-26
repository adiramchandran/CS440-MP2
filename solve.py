# -*- coding: utf-8 -*-
import numpy as np
#   
final_board = None
prev_constraints = {}
prev_choices = {}
pent_orients = []
orientation_types = ['F', 'I', 'L', 'N', 'P', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']            
orientations = [8, 2, 8, 8, 8, 4, 4, 4, 4, 1, 8, 4]


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
    board[board==1] = -1

    choices = {}                    # maps from (pentomino idx, unique orientation) to # of different coordinates an orientation can go
    constraints = {}                # maps from potential top left (row, col) coordinate to list of tuples (pent idx, unique orientation)
    
    for pent in pents:
        pent_orients.append(find_orientations(pent, get_pent_idx(pent)))
    # pent_orients should have all the possible pentominoes for the given pent_idx

    i = 0 
    for pent in pents:
        pent_idx = get_pent_idx(pent)
        for orient in find_orientations(pent, pent_idx):                 # each orientation in the orientation list for a certain pentonmino
            for row in range(board.shape[0]):
                for col in range(board.shape[1]):
                    if can_add_pentomino(board, orient, (row, col)):    # check if we can add a pentomino starting at the given (row, col)
                        # if we can add pent, then add to constraints dict
                        if (row, col) not in constraints.keys():
                            constraints[(row,col)] = []
                        constraints[(row, col)].append((pent_idx, orient))

                        orient_idx = i
                        choice = (pent_idx, orient_idx)
                        if (pent_idx, orient_idx) not in choices.keys():
                            choices[(pent_idx, orient_idx)] = []

                        choices[choice].append((row, col))
            i += 1     # moving forward in pent_orients
        i = 0      # new set of orient_idx's 
    # now we should have our choices and constraints dictionaries filled and we can backtrack
    # print(constraints)
    # print(choices)
    flag, ret_board = alg_back(board, choices, constraints)
    return ret_board

def place_pent(board, pent, pent_idx, coord, constraints, choices): # does add pentomino while changing choices and constraints

    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
                    constraints[(row, col)] = None

    for tup in choices.keys():
        if tup[0] == pent_idx:
            choices[tup] = None

    return True

def rem_pent(board, pent, pent_idx, coord, constraints, choices):
    board[board==pent_idx+1] = -1
    choices = prev_choices
    constraints = prev_constraints


def alg_back(board, choices, constraints):
    """
    base cases:
    1) constraints[(row, col)] is empty list (invalid so return false)
    2) all choices[orient] for one pent idx is empty (no more places to place a certain pentomino), return false
    3) if it's solved (choices and constraints are both empty), return true
    - remove all coordinates in constraints that are taken up by a move
    """
    
    # change true base case check to go through full dicts and confirm everything is None
    choice_flag = True
    const_flag = True
    for key in choices.keys():
        if choices[key] is not None:
            choice_flag = False 
            break
    for key in constraints.keys():
        if constraints[key] is not None:
            const_flag = False 
            break

    if choice_flag and const_flag:
        return True, board

    """
    temp_min = [(key, len(choices[tup])) for tup in choices.keys()]
    temp_min.sort(key=lambda x: x[1])
    chosen = choices[temp_min[0][0]]  # MOST RECENT ERROR <-- this is failing for a reason; it's printing a list of tuples instead of a tuple with pent idx and orient idx 
    """

    minimum = float('inf')
    chosen = None 
    for tup in choices.keys():
        if choices[tup] == None:
            continue
        if len(choices[tup]) < minimum:
            minimum = len(choices[tup])
            chosen = tup

    # chosen = min(choices.keys(), key=lambda tup:len(choices[tup])) <-- error for choices[tup] being None
    # print(chosen)
    if len(choices[chosen]) == 0:
        return False, board

    ret = False
    board_ret = None

    for coord in choices[chosen]:
        # print(coord)
        if not coord:
            continue
        prev_choices = choices
        prev_constraints = constraints
        place_flag = place_pent(board, pent_orients[chosen[0]][chosen[1]], chosen[0], coord, constraints, choices)
        if not place_flag:
            continue
        ret, board_ret = alg_back(board, choices, constraints)
        rem_pent(board, pent_orients[chosen[0]][chosen[1]], chosen[0], coord, constraints, choices)

    return ret, board_ret

def find_orientations(pent, pent_idx):
    orients = []
    pent_orients_num = orientations[pent_idx]

    if pent_orients_num == 1:
        orients.append(pent)
    elif pent_orients_num == 2:
        for i in range(2):
            orients.append(np.rot90(pent, i))
    elif pent_orients_num == 4:
        if pent_idx == len(orientations) - 1:
            for i in range(2):
                orients.append(np.rot90(pent, i))
            pent = np.flip(pent, 0)
            for i in range(2):
                orients.append(np.rot90(pent, i))

        else:
            for i in range(4):
                orients.append(np.rot90(pent, i))
    elif pent_orients_num == 8:
        for i in range(4):
            orients.append(np.rot90(pent, i))
        pent = np.flip(pent, 0)
        for i in range(4):
            orients.append(np.rot90(pent, i))

    return orients


def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    index = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                index = pent[i][j]
                break
        if index != 0:
            break
    if index == 0:
        return -1
    return index - 1


def can_add_pentomino(board, pent, coord):
    """
    Checks if the pentomino can be placed at the coordinate on the board.
    """
    if np.ndim(pent) == 1:
        for row in range(pent.shape[0]):
            if pent[row] != 0:
                if coord[0]+row >= board.shape[0] or coord[1] >= board.shape[1]:
                    return False
                if board[coord[0]+row][coord[1]] != -1: # Overlap
                    return False
    else:
        for row in range(pent.shape[0]):
            for col in range(pent.shape[1]):
                if pent[row][col] != 0:
                    if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]:
                        return False
                    if board[coord[0]+row][coord[1]+col] != -1: # Overlap
                        return False
    return True
