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

    def size(self):
        """
        Return (rows, cols) of the original block grid.
        """
        return (len(self.grid), len(self.grid[0]) if self.grid else 0)

    def size_expan(self):
        """
        Return (rows, cols) of the expanded grid.
        """
        return (len(self.expan_grid), len(self.expan_grid[0]) if self.expan_grid else 0)

    def fixed_blocks(self):
        """
        Return a dict {(r,c): 'A'/'B'/'C'} for fixed blocks present in the ORIGINAL grid.
        """
        fixed = {}
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell in ('A', 'B', 'C'):
                    fixed[(r, c)] = cell
        return fixed

    def placeable_slots(self):
        """
        Return a list of (r,c) indices in the ORIGINAL grid where movable blocks can be placed ('o' cells).
        """
        slots = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'o':
                    slots.append((r, c))
        return slots


def _build_expanded_grid(grid):
    """
    Create the half-step expanded grid with 'x' spacers *and* a full 'x' border.

    For an R x C original grid, the expanded grid is (2R+1) x (2C+1):
      - Initialize everything to 'x'
      - Place each original cell at (2*r+1, 2*c+1)

    Example (3x3) -> 7x7:
      originals at (1,1), (1,3), (1,5), (3,1), ..., (5,5)
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


def parse_bff(path):
    """Parse a .bff file from disk and return a Board object with expanded grid included."""
    with open(path, 'r', encoding='utf-8') as bff_file:
        lines = [ln.strip() for ln in bff_file]

    grid = []
    lasers = []
    targets = []
    counts = {'A': 0, 'B': 0, 'C': 0}
    i = 0

    def is_comment_or_blank(string):
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

board=parse_bff('dark_1.bff')
print(board.expan_grid)
print(board.grid)

class Block:
    kind: str
    def interact(self, pos, dir, vert_edge: bool):
        raise NotImplementedError

class ReflectBlock(Block):
    """
    A: reflect lazor at 90°.
        - vertical block face (even x, odd y): flip vx  -> (−vx,  vy)
        - horizontal block face  (odd x, even y): flip vy -> ( vx, −vy)
    """
    kind = 'A'
    def interact(self, pos, dir, vert_edge: bool):
        vx,vy = dir.x, dir.y
        if vert_edge:
            return [(pos, (-vx, vy))]
        else:
            return [(pos, (vx, -vy))]

class OpaqueBlock(Block):
    """
        B: absorbs beam.
    """
    kind = 'B'

    def interact(self, pos, dir, vert_edge: bool):
        return []

class RefractBlock(Block):
    """
        C: refracts lazor, allows lazor to pass through and reflects at 90° like ReflectBlock class
    """
    kind = 'C'
    def interact(self, pos, dir, vert_edge: bool):
        vx, vy = dir.x, dir.y
        if vert_edge:
            return [(pos,dir),(pos,(-vx, vy))]
        else:
            return [(pos,dir),(pos,(vx, -vy))]

BLOCKS: dict[str, Block] = { 'A': ReflectBlock(), 'B': OpaqueBlock(), 'C': RefractBlock(),}
