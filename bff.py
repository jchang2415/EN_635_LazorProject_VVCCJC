# do we need to know the grid is rectangular? or check for it?    <- I don't think so, cause the games dimensions are set as far as I'm aware so it will always be square?
class Board(object):
    """
    Wrapper for a parsed .bff file.

    Attributes
    ----------
    grid : list[list[str]]
    movable_counts : dict
    lasers : list
    targets : list
    """

    def __init__(self, grid, movable_counts, lasers, targets):
        self.grid = grid
        self.movable_counts = movable_counts
        self.lasers = lasers
        self.targets = targets

    def size(self):
        """
        Return (rows, cols) of the block grid.
        """
        return len(self.grid), len(self.grid[0]) if self.grid else 0

    def fixed_blocks(self):
        """
        Return a dict {(r,c): 'A'/'B'/'C'} for fixed blocks present in the grid.
        """
        fixed = {}
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell in ('A', 'B', 'C'):
                    fixed[(r, c)] = cell
        return fixed

    def placeable_slots(self):
        """
        Return a list of (r,c) indices where movable blocks can be placed ('o' cells).
        """
        slots = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'o':
                    slots.append((r, c))
        return slots

def parse_bff(path):
    """Parse a .bff file from disk and return a Board object"""
    with open(path, 'r', encoding='utf-8') as bff_file:
        lines = [ln.strip() for ln in bff_file]

    grid = []
    lasers = []
    targets = []
    counts = {'A': 0, 'B': 0, 'C': 0}
    in_grid = False
    i = 0

    def is_comment_or_blank(string):
        if len(string) == 0:
            return True
        if string[0] == '#':
            return True
        return False

    while i < len(lines):
        s = lines[i]
        i += 1
        if is_comment_or_blank(s):
            continue
        if s.upper() == 'GRID START':
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
                        raise ValueError("Invalid grid cell: %r" % c)
                grid.append(cells)
            continue

        if s[0] in 'ABC':
            p = s.split()
            counts[p[0]] = int(p[1])
            continue

        if s.startswith('L'):
            p = s.split()
            if len(p) < 5:
                raise ValueError("Laser line needs 4 integers: %r" % s)
            x, y = int(p[1]), int(p[2])
            vx, vy = int(p[3]), int(p[4])
            lasers.append((x, y, vx, vy))
            continue

        if s.startswith('P'):
            p = s.split()
            if len(p) < 3:
                raise ValueError("Target line needs 2 integers: %r" % s)
            x, y = int(p[1]), int(p[2])
            targets.append((x, y))
            continue

    return Board(grid, counts, lasers, targets)
