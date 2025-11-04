# Laser Simulation (integrated with blocks.Block) #
"""
Simulate lazor paths over a half-grid board using the interaction rules
encapsulated in :mod:`blocks` Block classes. This module exports a single
function:

    laser_path(board) -> list[set[(int, int)]]
"""
from __future__ import annotations

from typing import Dict, Tuple, List, Set, Optional, Iterable, Union

# Use the official blocks module and its Block classes
from blocks import BLOCKS, Block  # type: ignore

# Type aliases
Pos = Tuple[int, int] # half-grid coordinate (x, y)
Dir = Tuple[int, int] # lazor direction (vx, vy) where vx, vy ∈ {-1, +1}
BlockMap = Dict[Pos, Block] # {(cx,cy) at odd,odd -> Block instance}


def _board_dims(board) -> Tuple[int, int]: 
    """
    Returns (rows, cols) from the board.grid.

    Parameters
        Board

    Returns
        tuple[int, int]
            (rows, cols) of `board.grid`. If grid is empty, returns (0, 0) for cols.
    """
    rows = len(board.grid)
    cols = len(board.grid[0]) if rows else 0
    return rows, cols


def _value_to_block(val: Union[str, Block, None]) -> Optional[Block]:
    """
    Converts a grid/board value into a Block instance (or None).

    Parameters
        val : str | Block | None
            Cell value such as 'A'/'B'/'C', an actual Block, or None.
            
    Returns
        Block | None
            Block instance if recognized, else None.
    """
    if val is None:
        return None
    if isinstance(val, Block):
        return val
    if isinstance(val, str):
        return BLOCKS.get(val)
    return None


def _grid_to_blockmap(board) -> BlockMap:
    """
    Build a block map from either:
      - board.blocks (if present), or
      - board.grid (fallback)
    The returned map uses cell centers at (2*c+1, 2*r+1) and concrete Block objects.

    Parameters
        Board

    Returns
        dict[Pos, Block]
            Mapping from cell centers (2*c+1, 2*r+1) to concrete Block objects.
    """
    mp: BlockMap = {}

    # Prefer an explicit mapping supplied by the solver
    maybe_map = getattr(board, "blocks", None)
    if isinstance(maybe_map, dict):
        for pos, val in maybe_map.items():
            blk = _value_to_block(val)
            if blk is not None:
                mp[pos] = blk
        return mp

    # Fallback: derive from the grid itself
    rows, cols = _board_dims(board)
    for r in range(rows):
        row = board.grid[r]
        for c in range(cols):
            val = row[c]
            blk = _value_to_block(val)
            if blk is not None:
                cx, cy = 2 * c + 1, 2 * r + 1
                mp[(cx, cy)] = blk

    return mp


def _edge_hit(blocks: BlockMap, x: int, y: int, vx: int, vy: int) -> Tuple[Optional[Block], Optional[bool]]:
    """
    If (x,y) is exactly at a block edge center, return (block, vert_edge?).
    Otherwise return (None, None).

    Half-grid geometry:
      - Vertical edge centers are at (even, odd). The adjacent cell center is (x+vx, y).
      - Horizontal edge centers are at (odd, even). The adjacent cell center is (x, y+vy).

    Parameters
        blocks : dict[Pos, Block]
            Lookup of block centers at odd,odd coordinates.
        x, y : int
            Current half-grid position of the ray.
        vx, vy : int
            Current direction components (±1).

    Returns
        tuple[Block | None, bool | None]
            (block, is_vertical_edge). If no edge hit, returns (None, None).
    """
    # Vertical edge center
    if x % 2 == 0 and y % 2 == 1:
        target = (x + vx, y)  # just across the edge in the travel direction
        blk = blocks.get(target)
        if blk is not None:
            return blk, True

    # Horizontal edge center
    if x % 2 == 1 and y % 2 == 0:
        target = (x, y + vy)
        blk = blocks.get(target)
        if blk is not None:
            return blk, False

    return None, None


def laser_path(board) -> List[Set[Pos]]:
    """
    Trace each lazor from board.lasers over the half-grid, applying the
    `.interact()` logic implemented by Block classes from :mod:`blocks`.

    Assumptions
    
    - Lazor directions are 45° diagonals: (vx,vy) ∈ {(+1,+1), (+1,-1), (-1,+1), (-1,-1)}.
    - Board boundaries are the rectangle [0, 2*cols] × [0, 2*rows].

    Parameters
        Board 
    
    Returns
        list[set[(int,int)]]:
            For each lazor source in `board.lasers`, the set of all half-grid
            coordinates visited by that lazor and any of its refracted branches.
    """
    rows, cols = _board_dims(board)
    if rows == 0 or cols == 0:
        return [set() for _ in getattr(board, "lasers", [])]

    max_x, max_y = 2 * cols, 2 * rows  # inclusive bounds of the half-grid perimeter

    # Build a fast block lookup from the current board state
    blocks = _grid_to_blockmap(board)

    results: List[Set[Pos]] = []

    for (sx, sy, svx, svy) in board.lasers:
        # Active rays for this source: list of (pos, dir)
        active: List[Tuple[Pos, Dir]] = [((sx, sy), (svx, svy))]
        visited_states: Set[Tuple[int, int, int, int]] = set()
        hits: Set[Pos] = set()

        while active:
            (x, y), (vx, vy) = active.pop()

            # Advance until this ray dies (out of bounds or absorbed) or branches.
            while 0 <= x <= max_x and 0 <= y <= max_y:
                hits.add((x, y))

                state = (x, y, vx, vy)
                if state in visited_states:
                    break  # loop detected for this ray
                visited_states.add(state)

                # If we're centered on a block-edge, check for interaction.
                blk, is_vert = _edge_hit(blocks, x, y, vx, vy)
                if blk is not None:
                    # Let the block drive the physics.
                    interactions = blk.interact((x, y), (vx, vy), bool(is_vert))

                    # No interactions means absorption (opaque)
                    if not interactions:
                        break

                    # Spawn children rays. To avoid immediately re-processing
                    # the same edge, step each spawned ray forward by one unit.
                    for (px, py), (rx, ry) in interactions:
                        nx, ny = px + rx, py + ry
                        if 0 <= nx <= max_x and 0 <= ny <= max_y:
                            active.append(((nx, ny), (rx, ry)))
                    break  # stop advancing this current ray; spawned children continue instead.

                # No interaction at this node -> advance diagonally by one
                x += vx
                y += vy

        results.append(hits)

    return results
