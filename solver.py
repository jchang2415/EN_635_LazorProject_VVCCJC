# Solver Code #

'''
Define the core logic that attempts to find a valid configuration of movable blocks to solve a given Lazor board.
Use the bff.py(Board + parse_bff) & laser.py(laser_path simulation) modules.
'''

from itertools import combinations, combinations_with_replacement
from copy import deepcopy
from laser import laser_path


def check_solution(hit_paths, target_points):
    """
    Check whether all target points are hit by at least one laser.
    With added optimization to make stop checking if a target is missed. (increases speed)

    Parameters
        hit_paths : list[set[(int,int)]]
            List of sets containing (x, y) coordinates hit by each laser.
        target_points : list[(int,int)]
            Coordinates that lasers must intersect.

    Returns
        bool
            True if all target points are hit.
    """
    all_hits = set().union(*hit_paths)

    # Check each target one by one
    for point in target_points:

        # If a target is missed, stop checking early, as the solution already
        # cannot be valid
        if point not in all_hits:

            return False

    return True


def generate_block_combinations(board):
    """
    Generate a possible configurations of movable blocks, one at a time. Returns one configuration at a time. Will eventually generate all possible configurations if needed.

    Parameters
        board : Board
            Board object containing grid and movable block counts.

    Returns
        placement: dict
            Dictionary showing one possible placement of blocks in the grid. Maps (r, c) -> block type ('A', 'B', 'C', or None)
    """
    open_slots = board.placeable_slots()
    movable_counts = board.movable_counts

    # Generate list of indices indicating each open slot
    n_slots = len(open_slots)
    slots_idx = range(n_slots)

    # Use a combination method to generate all possible COMBOS of slot
    # placements (since order doesn't matter between blocks of same type)

    # Generate all possible placements of all the A blocks
    for a_slots in combinations(slots_idx, movable_counts.get('A', 0)):

        # For all of those possibilities, use the remaining open slots
        remaining_after_a = [i for i in slots_idx if i not in a_slots]

        # For the remaining open slots, generate all possible placement of B
        # blocks
        for b_slots in combinations(
            remaining_after_a,
            movable_counts.get(
                'B',
                0)):

            # Repeat for blocks of type C
            remaining_after_b = [
                i for i in remaining_after_a if i not in b_slots]
            for c_slots in combinations(
                remaining_after_b,
                movable_counts.get(
                    'C',
                    0)):

                # Generate the placement dictionary mapping blocks to the found
                # slots
                placement = {}
                for i, slot in enumerate(open_slots):

                    # If the index has been set aside for an A block, fill it
                    # in as such
                    if i in a_slots:
                        placement[slot] = 'A'

                    # Repeat for B and C blocks
                    elif i in b_slots:
                        placement[slot] = 'B'
                    elif i in c_slots:
                        placement[slot] = 'C'

                    # Otherwise, indicate that the slot is blank
                    else:
                        placement[slot] = None

                # Return the generated possibilites one at a time
                yield placement


def apply_blocks_to_board(base_board, placement):
    """
    Create a new board with a given placement of movable blocks.

    Parameters
        base_board : Board
            Original parsed board.
        placement : dict
            Mapping of (r, c) -> block type.

    Returns
        Board
            Deep copy of the board with all blocks (fixed + movable) applied.
    """
    board_copy = deepcopy(base_board)
    grid = deepcopy(board_copy.grid)

    # Apply movable blocks
    for (r, c), btype in placement.items():
        if btype:
            grid[r][c] = btype

    # Collect all block positions (fixed + movable)
    blocks = {}
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val in ('A', 'B', 'C'):
                # Laser.py expects (type, x, y)
                blocks[((2 * c) + 1, (2 * r) + 1)] = val

    board_copy.blocks = blocks
    board_copy.grid = grid
    return board_copy


def solve(board):
    """
    Try all possible block configurations until one solves the board.

    Parameters
        board : Board
            Parsed Lazor board object.

    Returns
        dict or None
            Mapping {(r, c): block type} for the valid solution,
            or None if no valid configuration found.
    """
    test_combo = generate_block_combinations(board)

    for i, placement in enumerate(
            test_combo, start=1):  # 1-indexed for user-friendly output
        test_board = apply_blocks_to_board(
            board, placement)  # Apply current placement
        hit_paths = laser_path(test_board)  # Simulate lasers

        if check_solution(
                hit_paths,
                board.targets):  # Check if all targets are hit
            print(f"Solution found after {i} tries!")  # Notify user
            return placement  # Return valid placement

    print("No valid solution found.")  # Notify user
    return None


