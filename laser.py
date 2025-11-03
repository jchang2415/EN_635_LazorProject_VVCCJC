# Laser Simulation #
"""
Simulate lazor paths over a half-grid board using block interaction rules
defined in blocks (2).py (BLOCKS registry). This module exports a single
function: laser_path(board) -> list[set[(int,int)]].
"""
from typing import Dict, Tuple, List, Set
# Prefer a normal module import; if unavailable, fall back to a local filename with spaces.
try:
    from blocks import BLOCKS  # Uses ReflectBlock/OpaqueBlock/RefractBlock via .interact
except Exception:  # pragma: no cover - fallback for filenames like 'blocks (2).py'
    import importlib.util, pathlib, types
    _bp = pathlib.Path(__file__).with_name("blocks (2).py")
    spec = importlib.util.spec_from_file_location("blocks2", str(_bp))
    _mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader, "Unable to load blocks (2).py"
    spec.loader.exec_module(_mod)  # type: ignore[attr-defined]
    BLOCKS = getattr(_mod, "BLOCKS")

# Type aliases
Pos = Tuple[int, int]        # half-grid coordinate (x,y)
Dir = Tuple[int, int]        # lazor direction (vx, vy) where vx,vy ∈ {-1, +1}
BlockMap = Dict[Pos, str]    # {(cx,cy) at odd,odd -> 'A'|'B'|'C'}


def _board_dims(board) -> Tuple[int, int]:
    """Return (rows, cols) from the board.grid."""
    rows = len(board.grid)
    cols = len(board.grid[0]) if rows else 0
    return rows, cols


def _grid_to_blockmap(board) -> BlockMap:
    """Build a block map from board.grid where cell centers are (2*c+1, 2*r+1)."""
    rows, cols = _board_dims(board)
    mp: BlockMap = {}
    for r in range(rows):
        for c in range(cols):
            cell = board.grid[r][c]
            if cell in ('A', 'B', 'C'):
                cx, cy = 2*c + 1, 2*r + 1
                mp[(cx, cy)] = cell
    return mp


def _edge_hit(blocks: BlockMap, x: int, y: int, vx: int, vy: int) -> Tuple[str, bool]:
    """
    If (x,y) is exactly at a block edge center, return (block_kind, vert_edge?).
    Otherwise return (None, None).

    Rules (half-grid geometry):
      - Vertical edge centers are at (even, odd). The adjacent cell center is (x+vx, y).
      - Horizontal edge centers are at (odd, even). The adjacent cell center is (x, y+vy).
    """
    # Vertical edge center
    if x % 2 == 0 and y % 2 == 1:
        # cell just across the edge in the direction of travel
        target = (x + vx, y)
        kind = blocks.get(target)
        if kind:
            return kind, True

    # Horizontal edge center
    if x % 2 == 1 and y % 2 == 0:
        target = (x, y + vy)
        kind = blocks.get(target)
        if kind:
            return kind, False

    return None, None


def laser_path(board) -> List[Set[Pos]]:
    """
    Trace each lazor from board.lasers over the half-grid, applying block interactions
    from `blocks.BLOCKS`. Returns a list of sets; each set contains every (x,y) position
    that the corresponding lazor (including refracted branches) visits.

    Expectations (per assignment + user constraints):
      - Lazors move only at 45°: (vx,vy) ∈ {(+1,+1), (+1,-1), (-1,+1), (-1,-1)}.
      - Starts are never at cell centers or vertices (so we only land on edges or free lattice points).
      - A hit can only occur at the center of a vertical or horizontal block edge.
    """
    rows, cols = _board_dims(board)
    if rows == 0 or cols == 0:
        return [set() for _ in getattr(board, "lasers", [])]

    max_x, max_y = 2*cols, 2*rows  # inclusive bounds for the half-grid perimeter

    # Build a fast block lookup from the current board state (includes placed movables).
    blocks = _grid_to_blockmap(board)

    results: List[Set[Pos]] = []

    for (sx, sy, svx, svy) in board.lasers:
        # Active rays for this source: list of (pos, dir)
        active: List[Tuple[Pos, Dir]] = [((sx, sy), (svx, svy))]
        visited_states: Set[Tuple[int,int,int,int]] = set()
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
                kind, is_vert = _edge_hit(blocks, x, y, vx, vy)
                if kind is not None:
                    # Opaque: absorb ray (stop here).
                    if kind == 'B':
                        break

                    # Reflect/refract using the Block class' interact definition.
                    # It returns a list of (pos, dir) pairs for new rays starting at the *same* edge position.
                    interactions = BLOCKS[kind].interact((x, y), (vx, vy), is_vert)

                    # Any refracted (pass-through) ray has the same direction; to avoid re-processing the same
                    # edge immediately, step each spawned ray forward by one unit.
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
