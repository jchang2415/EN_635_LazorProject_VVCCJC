# Main Block #
"""
Reads a .bff file from the `sample_bff_files/` folder,
parses the board, solves it, and writes the solution
to the `output/` folder.

Usage:
    python main.py <bff_filename>
Examples:
    python main.py dark_1.bff
    python main.py mad_1.bff
    python main.py tiny_5.bff
"""

import sys
import time
from pathlib import Path
from bff import parse_bff
from solver import solve
from output import write_solution


def main():
    """
    Runs the Lazor solver using a `.bff` filename supplied via sys.argv.
    Parameters
        None
            Arguments are read directly from sys.argv
    Returns
        None
    """
    if len(sys.argv) < 2:
        print("Error: Missing .bff filename.")
        print("Usage: python main.py <bff_filename>")
        print("Example: python main.py mad_1.bff")
        sys.exit(1)  #Exit with error code

    bff_name = sys.argv[1] #Filename from command line
    bff_path = Path("sample_bff_files") / bff_name #Full path to .bff file

    #Check that the file exists
    if not bff_path.exists():
        print(f"Error: File not found: {bff_path}")
        print("Make sure the file is inside the 'sample_bff_files/' folder.")
        sys.exit(1) #Exit with error code

    print(f"Parsing board file: {bff_path.name}") 
    try: #Parse the .bff file into a Board object
        board = parse_bff(bff_path)
    except Exception as e: #Catch parsing errors
        print(f"Failed to parse BFF file: {e}")
        sys.exit(1)

    print("Solving board...")
    start_time = time.time() #Start timer

    solution = solve(board) #Attempt to solve the board 

    elapsed = time.time() - start_time #Calculate elapsed time
    print(f"Solving completed in {elapsed:.2f} seconds.") #Report time taken

    #Prepare output folder
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"{bff_path.stem}_solution.txt"

    #Write the solution or report failure
    if solution:
        print("Valid solution found! Writing to output file...")
        write_solution(board, solution, output_file) #Write solution to file
        print(f"Solution saved to: {output_file.resolve()}")
    else: #No solution found
        print("No valid solution found for this board.")

    print("Program finished.")


if __name__ == "__main__":
    main()


