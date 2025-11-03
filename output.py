# Solution Output Generation #
'''
Code containing a function that prints the generated solution to an output file.
Requires a generated solution using functions from solver.py
'''

def write_solution(board, placement, out_path = "solution.txt"):
    '''
    Function for writing the found solution for a given board to an easily interpretable ASCII file.

    **Arguments**

        board: *Board*
            Object of class "Board" that contains the information for the board that was solved; parsed from .bff file.

        placement: *dict*
            Dictionary containing the placement of all blocks generated from the solve() function

        out_path: *str*
            File path for output file, including the file extension ".txt".
            Default path is "solution.txt"
    '''
    # Copy original grid parsed from original .bff file
    grid = [row[:] for row in board.grid]

    # Replace open slots in grid with generated placement for solution
    # For all elements in placement
    for (r, c), b_type in placement.items():

        # If a block is in that position
        if b_type:

            # Replace the grid element at that position with the letter representing the block type
            grid[r][c] = b_type

    # Format generated grid to be human-readable

    # Join elements in each row of "grid" with a space separating elements
    lines = [" ".join(row) for row in grid]

    # Join each row of grid with a newline character (to make a single ASCII formatted string)
    out = "\n".join(lines)

    # Write generated + formatted output to text file
    with open(out_path, "w", encoding = "utf-8") as outfile:

        outfile.write("Lazor Problem Solution: \n\n")
        outfile.write(out + "\n")

    # Indicate that the solution has been printed out to a solution file
    print(f"Solution has been written to {out_path}!")
