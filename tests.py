import pytest
from integrated_merged import (Board, parse_bff, laser_paths, _is_edge, _adjacent_center)


def test_is_edge_and_adjacent_center():
    is_edge, vertical = _is_edge((1,0))
    assert is_edge is True and vertical is True   # x odd, y even - vertical edge

    is_edge, vertical = _is_edge((0,1))
    assert is_edge is True and vertical is False  # x even, y odd - horizontal edge

    is_edge, vertical = _is_edge((1,1))
    assert is_edge is False                       

    assert _adjacent_center((1,0)) in [(1,1), (1,-1)]
    assert _adjacent_center((0,1)) in [(1,1), (-1,1)]

def test_reflect_block_vertical_edge():
    grid = [['o']]
    counts = {'A':1,'B':0,'C':0}
    lasers = [(0,1, 1,-1)]
    targets = []

    board = Board(grid, counts, lasers, targets)
    placements = {(0,0): 'A'}

    paths = laser_paths(board, placements, max_steps=50)

    assert len(paths) == 1
    p = paths[0]
    assert (0,1) in p and (1,0) in p
    assert p[-1] == (0,-1)

def test_refract_block_branches():
    grid = [['o']]
    counts = {'A':0,'B':0,'C':1}
    lasers = [(0,1, 1,-1)]
    targets = []

    board = Board(grid, counts, lasers, targets)
    placements = {(0,0): 'C'}

    paths = laser_paths(board, placements, max_steps=50)
    assert len(paths) == 2

    all_points = set(pt for path in paths for pt in path)
    assert (1,0) in all_points
    assert any(path[-1] in {(2,-1),(0,-1)} for path in paths)

def test_opaque_block_stops():
    grid = [['o']]
    counts = {'A':0,'B':1,'C':0}
    lasers = [(0,1, 1,-1)]
    targets = []

    board = Board(grid, counts, lasers, targets)
    placements = {(0,0): 'B'}

    paths = laser_paths(board, placements, max_steps=50)
    assert len(paths) == 1
    assert paths[0][-1] == (1,0)
    assert (2,-1) not in paths[0]

def test_multiple_lasers_seed():
    grid = [['o','o']]
    counts = {'A':0,'B':0,'C':0}
    lasers = [(0,1, 1,-1), (2,1, -1,-1)]
    targets = []
    board = Board(grid, counts, lasers, targets)

    paths = laser_paths(board, placements={}, max_steps=50)
    assert len(paths) == 2
    assert all(len(p) >= 2 for p in paths)
