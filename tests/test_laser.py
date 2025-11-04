# Unit Test for laser.py #

import pytest
from laser import laser_path
from blocks import BLOCKS
from types import SimpleNamespace

# Make a fake Board class object for testing with grid and laser attributes


def make_board(grid, lasers):
    '''
    Helper function to create a mock Board object
    grid: list[list[str]]
    lasers: list[(x, y, vx, vy)]
    '''

    return SimpleNamespace(grid=grid, lasers=lasers)

# Test physics of Type A blocks to ensure it reflects laser beams properly


def test_btype_A():
    '''
    '''

    # Make a sample grid for testing
    grid = [
        ["x", "x", "x"],
        ["x", "A", "x"],
        ["x", "x", "x"]
    ]

    # Make a sample laser moving towards the A block for testing
    lasers = [(1, 0, -1, -1)]

    # Use helper function to make a grid with the sample grid and laser
    test_board = make_board(grid, lasers)

    # Use the function to generate the path of coordinates hit by the laser in
    # the sample board
    hit_paths = laser_path(test_board)

    # Obtain the hit_path of the first element (laser) returned
    hits = hit_paths[0]

    # Check results for expected result
    assert (3, 2) in hits  # Hitting block before reflection
    assert (4, 1) in hits  # After reflection

# Test physics of Type B blocks to ensure it absorbs laser properly


def test_btype_B():
    '''
    Test that B block absorbs the laser (beam stops).
    '''
    # Make a sample grid for testing
    grid = [
        ["x", "x", "x"],
        ["x", "B", "x"],
        ["x", "x", "x"]
    ]

    # Make a sample laser moving towards the A block for testing
    lasers = [(1, 0, -1, -1)]

    # Use helper function to make a grid with the sample grid and laser
    test_board = make_board(grid, lasers)

    # Use the function to generate the path of coordinates hit by the laser in
    # the sample board
    hit_paths = laser_path(test_board)

    # Obtain the hit_path of the first element (laser) returned
    hits = hit_paths[0]

    # Check results for expected result
    assert (4, 1) not in hits  # Absorbed before it hits this point


# Test physics of Type C blocks to make sure it properly refracts lasers
def test_btype_C():
    '''
    Test that C block splits the laser into two beams, and that the beams are correct.
    '''
    # Make a sample grid for testing
    grid = [
        ["x", "x", "x"],
        ["x", "C", "x"],
        ["x", "x", "x"]
    ]

    # Make a sample laser moving towards the A block for testing
    lasers = [(1, 0, -1, -1)]

    # Use helper function to make a grid with the sample grid and laser
    test_board = make_board(grid, lasers)

    # Use the function to generate the path of coordinates hit by the laser in
    # the sample board
    hit_paths = laser_path(test_board)

    # Obtain the hit_path of the first element (original laser + any lasers it
    # creates) returned
    hits = hit_paths[0]

    # Check results for expected result

    # Laser should hit C block top edge
    assert (3, 2) in hits

    # Laser should reflect off top edge
    assert (4, 1) in hits

    # Laser should continue through to hit right edge of block
    assert (4, 3) in hits

    # Laser should have 2 distinct trajectories
    assert (4, 3) in hits and (4, 1) in hits
