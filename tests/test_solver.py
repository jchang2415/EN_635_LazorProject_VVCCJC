# Unit Testing for solver.py #

import pytest
from solver import (
    check_solution,
    generate_block_combinations,
    apply_blocks_to_board,
    solve,
)

# Create a fake Board class for testing our solver in isolation


class TestBoard:
    """Minimal fake Board class for testing solver logic in isolation from the rest of our code."""

    # Define attributes for test Board class
    def __init__(self):

        # Define a sample grid for testing
        self.grid = [
            ['o', 'x', 'o'],
            ['B', 'o', 'o'],
            ['o', 'o', 'o']
        ]

        # Define a sample pool of movable blocks for testing
        self.movable_counts = {'A': 2, 'B': 0, 'C': 1}

        # Define sample lasers for testing
        self.lasers = [(1, 0, 1, 1), (4, 5, -1, -1)]

        # Define sample targets for testing
        self.targets = [(1, 6), (6, 3)]

    # Define a method for determining the number of open slots that blocks can
    # be placed at (in (r, c) notation)
    def placeable_slots(self):
        """Simulate open 'o' cells correctly."""
        return [(0, 0), (0, 2), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

    # Define method for returning the size of the grid
    def size(self):
        return (len(self.grid), len(self.grid[0]))


# Test that our helper function for checking solutions works correctly
def test_check_solution_all_targets_hit():
    '''
    Testing to ensure that our solution checker works.
     Ensure that if targets are in the hit_path, checker should return True.
    '''
    # Define a sample hit_path for testing
    hit_paths = [{(1, 1), (2, 2), (3, 3)}]

    # Define a sample target
    targets = [(3, 3)]

    # Check that the checker correctly identifies that a solution was found
    assert check_solution(hit_paths, targets) is True

# Test that our helper function for checking solutions works correctly in
# negative case


def test_check_solution_target_missed():
    '''
    Testing to ensure that our solution checker works when a solution is NOT found.
    Ensure that if a target is missed, it returns false early to terminate checking.
    '''

    # Define a sample hit_path for testing
    hit_paths = [{(1, 1), (2, 2)}]

    # Define a sample target for testing
    targets = [(3, 3), (5, 5)]

    # Check that checker correctly identifies that a target was missed
    assert check_solution(hit_paths, targets) is False


# Test that our helper function for checking solutions works correctly
# when hit_paths is emtpy
def test_check_solution_empty_hits():
    '''
    Test to ensure that an empty hit_path returns that the configuration is not a solution.
    '''
    assert not check_solution([], [(1, 1)])


# Test that generation of possible solutions are consistent with number of
# movable objects fed in
def test_generate_block_combinations_counts_and_types():
    '''
    Testing to ensure that all generated placements possibilities match expected movable_counts.
    '''

    # Generate a test Board classo object for testing
    board = TestBoard()

    # Use block combo generator function on that test object
    combos = list(generate_block_combinations(board))

    # Verify that there are multiple possible placements
    assert len(combos) > 0

    # For all the combinations generated,
    for placement in combos:

        # Ensure each placement has correct keys and valid block types
        assert set(placement.keys()) == set(board.placeable_slots())

        # Ensure that the correct block types are maintained
        for btype in placement.values():
            assert btype in (None, 'A', 'B', 'C')

        # Ensure correct total number of A and B blocks are being generated
        count_A = sum(1 for v in placement.values() if v == 'A')
        count_C = sum(1 for v in placement.values() if v == 'C')
        assert count_A <= board.movable_counts['A']
        assert count_C <= board.movable_counts['C']


# Test that the generation of possible solutions reacts correctly to there
# being no movable blocks
def test_generate_block_combinations_zero_blocks():
    '''
    Testing to ensure that if no movable blocks are fed into the combo generation function, all placements should be None.
    '''
    # Generate a test Board class object
    board = TestBoard()

    # Set the movable counts of that test Board class object to none
    board.movable_counts = {'A': 0, 'B': 0, 'C': 0}

    # Use that test Board class object to generate possible placements
    combos = list(generate_block_combinations(board))

    # Check that the results are as expected

    # Check that only one possibility is generated (order doesn't matter)
    assert len(combos) == 1

    # Check that the possibility is filled with None
    assert all(v is None for v in combos[0].values())


# Test that our "apply_blocks_to_board" function works correctly in
# mapping the placement to a grid
def test_apply_blocks_to_board_adds_blocks_correctly():
    '''
    Testing to ensure block placements are correctly applied to a grid and block dictionary.
    '''

    # Generate a test Board class object
    board = TestBoard()

    # Generate a sample placement
    placement = {(0, 0): 'A', (0, 2): None, (1, 1): 'B', (1, 2): None}

    # Use the function to apply the placement to the Board class object
    modified = apply_blocks_to_board(board, placement)

    # Check that the generated grid has A and B in the correct positions
    assert modified.grid[0][0] == 'A'
    assert modified.grid[1][1] == 'B'

    # Check that blocks dict contains only valid (odd, odd) positions and
    # valid types
    for (pos, kind) in modified.blocks.items():
        x, y = pos
        assert x % 2 == 1 and y % 2 == 1
        assert kind in ('A', 'B', 'C')

# Test to ensure that the function does not alter the original Board class
# object


def test_apply_blocks_to_board_does_not_modify_original():
    '''
    Ensure original board is not mutated by apply_blocks_to_board().
    '''

    # Generate a test Board class object
    board = TestBoard()

    # Generate a sample placement for testing
    placement = {(0, 0): 'A'}

    # Use the apply blocks function on the board
    modified = apply_blocks_to_board(board, placement)

    # Check that the original Board object is not changed
    assert board.grid[0][0] == 'o'
    assert modified.grid[0][0] == 'A'
    assert board is not modified


# Test that the solver can find a solution correctly
def test_solve_finds_solution(monkeypatch):
    '''
    Check that our solver function can correctly find a solution that exists.
    '''
    # Generates a test Board class object
    board = TestBoard()

    # Force generate_block_combinations to yield one placement
    fake_placement = {(0, 0): 'A'}
    monkeypatch.setattr(
        'solver.generate_block_combinations',
        lambda b: [fake_placement])

    # Force apply_blocks_to_board (just returns same board)
    monkeypatch.setattr('solver.apply_blocks_to_board', lambda b, p: b)

    # Force laser_path to return hits that include all targets
    monkeypatch.setattr('solver.laser_path', lambda b: [{(3, 3)}])

    # Force check_solution to always return True
    monkeypatch.setattr('solver.check_solution', lambda hits, targets: True)

    # Solve the test board using our solver function
    placement = solve(board)

    # Check that the found solution using the solver function matches what was
    # expected
    assert placement == fake_placement


# Test that our solver function doesn't find a solution when one doesn't exist
def test_solve_no_solution(monkeypatch):
    '''
    Test to ensure that the solver returns None when no solution to a board is possible.
    '''
    # Generate a test Board
    board = TestBoard()

    # Force the attributes to yield an unsolvable board
    monkeypatch.setattr('solver.generate_block_combinations',
                        lambda b: [{(0, 0): 'A'}])
    monkeypatch.setattr('solver.apply_blocks_to_board', lambda b, p: b)
    monkeypatch.setattr('solver.laser_path', lambda b: [{(0, 0)}])
    monkeypatch.setattr('solver.check_solution', lambda h, t: False)

    # Use our solver function to attempt to solve the board
    result = solve(board)

    # Check to ensure that no solution is found as expected
    assert result is None
