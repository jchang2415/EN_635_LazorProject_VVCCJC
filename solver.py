# Solver Code #

'''
Define the core logic that attempts to find a valid configuration of movable blocks to solve a given Lazor board.
Uses the bff.py(Board + parse_bff) & laser.py(laser_path simulation) modules.
'''

from itertools import product
from copy import deepcopy
from laser import laser_path


def check_solution(hit_paths, target_points):
    """
    Check whether all target points are hit by at least one laser.

    Parameters
    ----------
    hit_paths : list[set[(int,int)]]
        List of sets containing (x, y) coordinates hit by each laser.
    target_points : list[(int,int)]
        Coordinates that lasers must intersect.

    Returns
    -------
    bool
        True if all target points are hit.
    """
    all_hits = set().union(*hit_paths)
    return all(point in all_hits for point in target_points)


def get_open_slots(board):        # Doesn't seem like a function is necessary here; only use it once and the function is just one line of code - Jason
    """
    Return all coordinates (r, c) where movable blocks can be placed.
    """
    return board.placeable_slots()


def generate_block_combinations(board):
    """
    Generate all possible configurations of movable blocks.

    Parameters
    ----------
    board : Board
        Board object containing grid and movable block counts.

    Returns
    -------
    list[dict]
        Each dict maps (r, c) -> block type ('A', 'B', 'C', or None)
    """
    open_slots = get_open_slots(board)
    movable_counts = board.movable_counts

    #Create list of all movable block types to distribute
    block_pool = []
    for block_type, count in movable_counts.items():
        block_pool += [block_type] * count

    #Fill unused open slots with None
    while len(block_pool) < len(open_slots):
        block_pool.append(None)

    #Generate all possible combinations(Cartesian product)
    all_combos = product(block_pool, repeat=len(open_slots))

    valid_combos = []
    for combo in all_combos:
        used_counts = {'A': 0, 'B': 0, 'C': 0} #Track used blocks
        placement = {} #Map of (r, c) -> block type

        valid = True #Flag to check if combo is valid
        for slot, btype in zip(open_slots, combo):  #(slot is (r, c)
            if btype: #If a block is placed
                used_counts[btype] += 1 #Increment used count
                if used_counts[btype] > movable_counts[btype]:
                    valid = False #Exceeded available blocks
                    break
            placement[slot] = btype #Record placement

        if valid:
            valid_combos.append(placement) #Store valid placement

    return valid_combos #Return all valid configurations


def apply_blocks_to_board(base_board, placement):
    """
    Create a new board with a given placement of movable blocks.

    Parameters
    ----------
    base_board : Board
        Original parsed board.
    placement : dict
        Mapping of (r, c) -> block type.

    Returns
    -------
    Board
        Deep copy of the board with all blocks (fixed + movable) applied.
    """
    board_copy = deepcopy(base_board)
    grid = deepcopy(board_copy.grid)

    #Apply movable blocks
    for (r, c), btype in placement.items():
        if btype:
            grid[r][c] = btype

    #Collect all block positions (fixed + movable)
    blocks = {}
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val in ('A', 'B', 'C'):
                # Laser.py expects (type, x, y)
                blocks[((2*c) + 1, (2*r) + 1)] = val

    board_copy.blocks = blocks
    board_copy.grid = grid
    return board_copy


def solve(board):
    """
    Try all possible block configurations until one solves the board.

    Parameters
    ----------
    board : Board
        Parsed Lazor board object.

    Returns
    -------
    dict or None
        Mapping {(r, c): block type} for the valid solution,
        or None if no valid configuration found.
    """
    print("Generating possible configurations...")
    combos = generate_block_combinations(board)
    print(f"Total combinations to test: {len(combos)}")

    for i, placement in enumerate(combos, start=1): #1-indexed for user-friendly output
        test_board = apply_blocks_to_board(board, placement) #Apply current placement
        hit_paths = laser_path(test_board) #Simulate lasers

        if check_solution(hit_paths, board.targets): #Check if all targets are hit
            print(f"✔️ Solution found after {i} tries!") #Notify user
            return placement #Return valid placement

    print("❌ No valid solution found.") #Notify user
    return None



