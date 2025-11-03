class Board(object):
    """
    Wrapper for a parsed .bff file.

    Attributes
    ----------
    expan_grid : list[list[str]]
        The expanded grid of size (2*rows+1) x (2*cols+1), with 'x' spacers
        between every original cell and as a border around the grid.
    grid : list[list[str]]
        The original grid from the .bff (rows x cols).
    counts : dict
        {'A': int, 'B': int, 'C': int} available movable blocks by type.
    lasers : list[tuple[int,int,int,int]]
        Each item is (x, y, vx, vy).
    targets : list[tuple[int,int]]
        Each item is (x, y) target coordinate.
    """

    def __init__(self, expan_grid, grid, counts, lasers, targets):
        self.expan_grid = expan_grid
        self.grid = grid
        self.counts = counts
        self.lasers = lasers
        self.targets = targets

    def size(self) -> Tuple[int, int]:
        """Return (rows, cols) of the original block grid."""
        return (len(self.grid), len(self.grid[0]) if self.grid else 0)

    def size_expan(self) -> Tuple[int, int]:
        """Return (rows, cols) of the expanded grid."""
        return (len(self.expan_grid), len(self.expan_grid[0]) if self.expan_grid else 0)

    def fixed_blocks(self) -> Dict[Tuple[int, int], str]:
        """Return a dict {(r,c): 'A'/'B'/'C'} for fixed blocks present in the ORIGINAL grid."""
        fixed: Dict[Tuple[int, int], str] = {}
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell in ('A', 'B', 'C'):
                    fixed[(r, c)] = cell
        return fixed

    def placeable_slots(self) -> List[Tuple[int, int]]:
        """Return a list of (r,c) indices in the ORIGINAL grid where movable blocks can be placed ('o' cells)."""
        slots: List[Tuple[int, int]] = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'o':
                    slots.append((r, c))
        return slots


def _build_expanded_grid(grid: List[List[str]]) -> List[List[str]]:
    """
    Create the half-step expanded grid with 'x' spacers *and* a full 'x' border.

    For an R x C original grid, the expanded grid is (2R+1) x (2C+1):
      - Initialize everything to 'x'
      - Place each original cell at (2*r+1, 2*c+1)
    """
    if not grid:
        return []

    R = len(grid)
    C = len(grid[0])
    ER = 2 * R + 1
    EC = 2 * C + 1

    expan = [['x' for _ in range(EC)] for _ in range(ER)]
    for r in range(R):
        for c in range(C):
            expan[2 * r + 1][2 * c + 1] = grid[r][c]
    return expan


def parse_bff(path: str) -> Board:
    """Parse a .bff file from disk and return a Board object with expanded grid included."""
    with open(path, 'r', encoding='utf-8') as bff_file:
        lines = [ln.strip() for ln in bff_file]

    grid: List[List[str]] = []
    lasers: List[Tuple[int, int, int, int]] = []
    targets: List[Tuple[int, int]] = []
    counts: Dict[str, int] = {'A': 0, 'B': 0, 'C': 0}
    i = 0

    def is_comment_or_blank(string: str) -> bool:
        return (len(string) == 0) or (string[0] == '#')

    while i < len(lines):
        s = lines[i]
        i += 1
        if is_comment_or_blank(s):
            continue

        if s.upper() == 'GRID START':
            # Read rows until 'GRID STOP'
            while i < len(lines):
                row = lines[i].strip()
                i += 1
                if row.upper() == 'GRID STOP':
                    break
                if is_comment_or_blank(row):
                    continue
                cells = row.split()
                for c in cells:
                    if c not in ('o', 'x', 'A', 'B', 'C'):
                        raise ValueError(f"Invalid grid cell: {c!r}")
                grid.append(cells)
            continue

        # Counts line: "A 2", "B 1", "C 0", etc.
        if s and s[0] in 'ABC':
            p = s.split()
            if len(p) != 2:
                raise ValueError(f"Invalid count line: {s!r}")
            counts[p[0]] = int(p[1])
            continue

        # Laser: "L x y vx vy"
        if s.startswith('L'):
            p = s.split()
            if len(p) < 5:
                raise ValueError(f"Laser line needs 4 integers: {s!r}")
            x, y = int(p[1]), int(p[2])
            vx, vy = int(p[3]), int(p[4])
            lasers.append((x, y, vx, vy))
            continue

        # Target: "P x y"
        if s.startswith('P'):
            p = s.split()
            if len(p) < 3:
                raise ValueError(f"Target line needs 2 integers: {s!r}")
            x, y = int(p[1]), int(p[2])
            targets.append((x, y))
            continue

    # Build the expanded grid with 'x' spacers
    expan_grid = _build_expanded_grid(grid)
    return Board(expan_grid, grid, counts, lasers, targets)


class Block:
    kind: str
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        raise NotImplementedError


class ReflectBlock(Block):
    """
    A: reflect lazor at 90°.
        - vertical block face (even x, odd y): flip vx  -> (−vx,  vy)
        - horizontal block face  (odd x, even y): flip vy -> ( vx, −vy)
    """
    kind = 'A'
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        vx, vy = dir
        if vert_edge:
            return [(pos, (-vx, vy))]
        else:
            return [(pos, (vx, -vy))]


class OpaqueBlock(Block):
    """B: absorbs beam."""
    kind = 'B'
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        return []


class RefractBlock(Block):
    """
    C: refracts lazor, allows lazor to pass through AND reflects at 90° like ReflectBlock.
    """
    kind = 'C'
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        vx, vy = dir
        if vert_edge:
            # pass-through and a vertical reflection
            return [(pos, (vx, vy)), (pos, (-vx, vy))]
        else:
            # pass-through and a horizontal reflection
            return [(pos, (vx, vy)), (pos, (vx, -vy))]


BLOCKS: Dict[str, Block] = {
    'A': ReflectBlock(),
    'B': OpaqueBlock(),
    'C': RefractBlock(),
}


# === Laser simulation integrated with Block classes ===
from collections import deque
from typing import Dict, Tuple, List, Set

Vec = Tuple[int, int]

def _is_inside_expan(board: "Board", p: Vec) -> bool:
    x, y = p
    h, w = len(board.expan_grid), len(board.expan_grid[0])
    return 0 <= x < w and 0 <= y < h

def _is_edge(p: Vec) -> Tuple[bool, bool]:
    """Return (is_edge, is_vertical_edge) based on half-grid parity.
    Edge iff exactly one coord is odd. If x is odd and y is even => vertical edge.
    """
    x, y = p
    is_edge = (x % 2) != (y % 2)
    vert = (x % 2 == 1 and y % 2 == 0)
    return is_edge, vert

def _adjacent_center(p: Vec) -> Vec:
    """Map an edge coordinate to the adjacent block center coordinate (half-grid)."""
    x, y = p
    if x % 2 == 1 and y % 2 == 0:   # vertical edge -> center is (x, y+1) or (x, y-1); choose integer center next step along y? We use the nearest odd y
        return (x, y+1) if (y+1) % 2 == 1 else (x, y-1)
    elif x % 2 == 0 and y % 2 == 1: # horizontal edge
        return (x+1, y) if (x+1) % 2 == 1 else (x-1, y)
    else:
        return (x, y)

def build_block_instances(board: "Board", placements: Dict[Tuple[int,int], str]) -> Dict[Tuple[int,int], "Block"]:
    """Return dict mapping block-center (half-grid coords) -> Block instance.
    - Include fixed blocks in board.grid (A/B/C).
    - Include movable placements on 'o' cells provided in placements as letters.
    """
    blocks: Dict[Tuple[int,int], "Block"] = {}
    rows, cols = len(board.grid), len(board.grid[0])
    for r in range(rows):
        for c in range(cols):
            ch = board.grid[r][c]
            if ch in "ABC":
                center = (2*c+1, 2*r+1)
                blocks[center] = BLOCKS[ch]
    for (c, r), ch in placements.items():
        if ch in "ABC":
            center = (2*c+1, 2*r+1)
            blocks[center] = BLOCKS[ch]
    return blocks

def laser_paths(board: "Board", placements: Dict[Tuple[int,int], str], max_steps: int = 10000) -> List[List[Vec]]:
    """Trace all lasers on the expanded grid using Block classes.
    Returns a list of polyline paths (list of positions) for each originating laser ray,
    including branches from refract blocks.
    """
    block_map = build_block_instances(board, placements)
    all_paths: List[List[Vec]] = []
    # Each entry: (current position, direction, path_so_far)
    q: deque[Tuple[Vec, Vec, List[Vec]]] = deque()

    # Seed with the starting lasers
    for (x, y, vx, vy) in board.lasers:
        q.append(((x, y), (vx, vy), [(x, y)]))

    steps = 0
    visited: Set[Tuple[Vec, Vec]] = set()
    while q and steps < max_steps:
        pos, d, path = q.popleft()
        steps += 1
        # advance one half-grid step
        nxt = (pos[0] + d[0], pos[1] + d[1])

        if not _is_inside_expan(board, nxt):
            # Ray leaves board; finalize this path
            all_paths.append(path + [nxt])
            continue

        is_edge, vertical_edge = _is_edge(nxt)
        if is_edge:
            center = _adjacent_center(nxt)
            blk = block_map.get(center)
            if blk is not None:
                # interact; may branch
                outcomes = blk.interact(nxt, d, vertical_edge)
                # For opaque, interact returns empty list; we end path at impact point
                if not outcomes:
                    all_paths.append(path + [nxt])
                    continue
                # For each outcome, enqueue continuation starting at the same edge/impact point
                for p_out, d_out in outcomes:
                    state = (p_out, d_out)
                    if (state) in visited:
                        continue
                    visited.add(state)
                    q.append((p_out, d_out, path + [p_out]))
                # We already enqueued branches; continue loop
                continue

        # No block interaction; just continue straight
        q.append((nxt, d, path + [nxt]))

    # If queue drained or hit step limit, push any unfinished paths
    while q:
        pos, d, path = q.popleft()
        all_paths.append(path)

    return all_paths
