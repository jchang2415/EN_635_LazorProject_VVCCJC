"""
tests.py — Unit tests for the Lazor Project

Structure Overview:

1. Imports
   - pytest for test execution
   - Core modules from the main branch:
       bff.py     → parse_bff() handles .bff file parsing
       solver.py  → Board class & laser_paths() logic
       laser.py   → internal laser geometry helpers

2. Geometry Tests
   - test_is_edge_and_adjacent_center()
       Ensures edge detection and adjacency logic works.
   - test_reflect_block_vertical_edge()
       Validates reflection behavior on vertical edges.
   - test_refract_block_branches()
       Confirms refracted beams correctly branch.
   - test_opaque_block_stops()
       Checks that opaque blocks terminate beams.

3. Parser Test
   - test_parse_bff()
       Confirms .bff files are parsed correctly into
       grid, counts, lasers, and targets.

4. Solver Test
   - test_solver_with_simple_board()
       Runs a small solvable board configuration to verify
       that Board + laser_paths() integration behaves properly.

Usage:

Run all tests with:
    pytest tests.py
or from the project root:
    pytest 
"""

import pytest
from bff import parse_bff # bff.py contains parse_bff
from solver import Board, laser_paths # solver.py contains Board and laser_paths
from laser import _is_edge, _adjacent_center    # laser.py contains these helper functions


def test_is_edge_and_adjacent_center(): #pytest.mark.unit
    is_edge, vertical = _is_edge((1,0)) # x odd, y even
    assert is_edge is True and vertical is True   # x odd, y even - vertical edge

    is_edge, vertical = _is_edge((0,1))
    assert is_edge is True and vertical is False  # x even, y odd - horizontal edge

    is_edge, vertical = _is_edge((1,1)) # x odd, y odd
    assert is_edge is False                       

    assert _adjacent_center((1,0)) in [(1,1), (1,-1)]
    assert _adjacent_center((0,1)) in [(1,1), (-1,1)]


def test_reflect_block_vertical_edge(): #pytest.mark.unit
    grid = [['o']] # single empty cell
    counts = {'A':1,'B':0,'C':0} # one reflect block
    lasers = [(0,1, 1,-1)] # laser coming in towards vertical edge
    targets = [] # no targets

    board = Board(grid, counts, lasers, targets) # create board
    placements = {(0,0): 'A'} # place reflect block

    paths = laser_paths(board, placements, max_steps=50) # get laser paths

    assert len(paths) == 1 # only one path should exist
    p = paths[0]
    assert (0,1) in p and (1,0) in p
    assert p[-1] == (0,-1)


def test_refract_block_branches(): #pytest.mark.unit
    grid = [['o']]
    counts = {'A':0,'B':0,'C':1}
    lasers = [(0,1, 1,-1)]
    targets = []

    board = Board(grid, counts, lasers, targets) # create board
    placements = {(0,0): 'C'}

    paths = laser_paths(board, placements, max_steps=50) # get laser paths
    assert len(paths) == 2

    all_points = set(pt for path in paths for pt in path) # combine all points from both paths
    assert (1,0) in all_points
    assert any(path[-1] in {(2,-1),(0,-1)} for path in paths) # check that one path goes to (2,-1) and the other to (0,-1)


def test_opaque_block_stops(): 
    grid = [['o']]
    counts = {'A':0,'B':1,'C':0}
    lasers = [(0,1, 1,-1)]
    targets = []

    board = Board(grid, counts, lasers, targets) # create board
    placements = {(0,0): 'B'}

    paths = laser_paths(board, placements, max_steps=50) # get laser pathsq
    assert len(paths) == 1


def test_parse_bff(tmp_path):
    # Create a simple mock .bff file for parsing
    bff_text = """GRID START 
o o 
o o
GRID STOP

A 1
B 1
C 1

L 0 0 1 1
P 1 1
"""
    bff_file = tmp_path / "test.bff"
    bff_file.write_text(bff_text) # write mock data to file

    grid, counts, lasers, targets = parse_bff(str(bff_file)) # parse the file
    assert grid == [['o', 'o'], ['o', 'o']]
    assert counts == {'A': 1, 'B': 1, 'C': 1}
    assert lasers == [(0, 0, 1, 1)]
    assert targets == [(1, 1)]


def test_solver_with_simple_board(tmp_path): 
    # Small grid where one reflection solves target
    grid = [['o', 'o']]
    counts = {'A': 1, 'B': 0, 'C': 0}
    lasers = [(0, 1, 1, -1)]
    targets = [(1, 0)]
 
    board = Board(grid, counts, lasers, targets) # create board
    placements = {(0, 0): 'A'} # place reflect block

    paths = laser_paths(board, placements, max_steps=100)# get laser paths
    all_points = set(pt for path in paths for pt in path)# combine all points from paths
    assert (1, 0) in all_points # check target is hit
 
