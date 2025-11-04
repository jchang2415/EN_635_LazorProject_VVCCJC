"""
Lazor board data and .bff parser.

This module contains:
  • Board — container for grid, movable block counts, lasers, and targets.
  • parse_bff(path) — reads a .bff file and returns a Board.

Raises:
  ValueError on invalid tokens or malformed lines.
"""

class Board(object):
    """
    Lightweight container for a Lazor puzzle parsed from a .bff file.

    Attributes
    ----------
    grid : list[list[str]]          # 'x','o','A','B','C'
    movable_counts : dict           # {'A': int, 'B': int, 'C': int}
    lasers : list[tuple[int,int,int,int]]  # (x, y, vx, vy)
    targets : list[tuple[int,int]]  # (x, y)

    Typical usage: produced by parse_bff(path) and passed to solver/laser code.
    """

    def __init__(self, grid, movable_counts, lasers, targets): # initialize Board
        self.grid = grid # 2D list of grid cells
        self.movable_counts = movable_counts # dict of movable block counts
        self.lasers = lasers # list of lasers (x, y, vx, vy)
        self.targets = targets # list of targets (x, y)

    def size(self): # return board dimensions
        """
        Return (rows, cols) of the block grid.
        """
        return len(self.grid), len(self.grid[0]) if self.grid else 0

    def fixed_blocks(self):
        """
        Return a dict {(r,c): 'A'/'B'/'C'} for fixed blocks present in the grid.
        """
        fixed = {} # initialize empty dict
        for r, row in enumerate(self.grid): 
            for c, cell in enumerate(row):
                if cell in ('A', 'B', 'C'):
                    fixed[(r, c)] = cell
        return fixed # return dict of fixed blocks

    def placeable_slots(self):
        """
        Return a list of (r,c) indices where movable blocks can be placed ('o' cells).
        """
        slots = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell == 'o': # if cell is empty
                    slots.append((r, c)) # add to slots list
        return slots # return list of slots

def parse_bff(path):
    """
    Parses a .bff file from disk and returns a Board object

    Parameters
        path: str
    Returns
        Board: Board(grid, movable_counts, lasers, targets)
    """
    with open(path, 'r', encoding='utf-8') as bff_file:
        lines = [ln.strip() for ln in bff_file]

    grid = []
    lasers = []
    targets = []
    counts = {'A': 0, 'B': 0, 'C': 0}
    in_grid = False # flag for grid section
    i = 0 # line index

    def is_comment_or_blank(string): 
        """
        Checks if line is comment or blank

        Parameters
            string: str

        Returns
            Boolean
        """
        if len(string) == 0:
            return True
        if string[0] == '#':
            return True
        return False 

    while i < len(lines): # iterate through lines
        s = lines[i]
        i += 1
        if is_comment_or_blank(s): # skip comments and blank lines
            continue
        if s.upper() == 'GRID START': # start of grid section
            while i < len(lines):
                row = lines[i].strip()
                i += 1
                if row.upper() == 'GRID STOP': # end of grid section
                    break
                if is_comment_or_blank(row): # skip comments and blank lines
                    continue
                cells = row.split() # split row into cells
                for c in cells:
                    if c not in ('o', 'x', 'A', 'B', 'C'): # validate cell
                        raise ValueError("Invalid grid cell: %r" % c) # raise error for invalid cell
                grid.append(cells)
            continue

        if s[0] in 'ABC': # block count line
            p = s.split()
            counts[p[0]] = int(p[1])
            continue

        if s.startswith('L'): # laser line
            p = s.split()
            if len(p) < 5:
                raise ValueError("Laser line needs 4 integers: %r" % s) # validate laser line
            x, y = int(p[1]), int(p[2])
            vx, vy = int(p[3]), int(p[4])
            lasers.append((x, y, vx, vy)) # add laser to list
            continue

        if s.startswith('P'):
            p = s.split()
            if len(p) < 3:
                raise ValueError("Target line needs 2 integers: %r" % s) # validate target line
            x, y = int(p[1]), int(p[2])
            targets.append((x, y)) # add target to list
            continue

    return Board(grid, counts, lasers, targets) # return Board object
