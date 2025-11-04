# Lazor Project (Vedant, Cam, and Jason)
This repository contains code for solving problems in the "Lazors" game available on Steam and iPhone when provided with a ".bff" file describing the board set-up for the problem.

## Files
bff.py- Board class and .bff file parser. \n
blocks.py- Base block class and subclasses. \n
laser.py- Simulates laser movement on the board. \n
solver.py- Generates all possible placements of blocks on the board, simulates laser and checks weather target was hit. \n
output.py- Writes solution output. \n
main.py- Allows command line entry. \n
tests/test_*.py - Contains the various unit tests. \n

## Installation
pytest install, sys install, time install

## Usage
To solve a puzzle using this code, download the relevant .bff file and run the function using: \n
python main.py <filename.bff>  \n
The output will be generated in a folder called "outputs" as a txt file named filename_solution.txt containing the grid with blocks placed in the solution configuration in a format similar to the .bff file input.

## Running Unit Tests
To run unit tests, make sure pytest is installed. If not installed, install it using: \n
pip install pytest \n
Then run the unit tests using this command: \n
python -m pytest -v  \n
\n 
Example Output:  \n
'''
tests/test_bff.py::test_board_methods PASSED                                                                                                                   [  4%]
tests/test_bff.py::test_invalid_grid_cell PASSED                                                                                                               [  9%]
tests/test_bff.py::test_invalid_laser PASSED                                                                                                                   [ 14%] 
tests/test_bff.py::test_invalid_target PASSED                                                                                                                  [ 19%]
tests/test_bff.py::test_valid_bff_parsing PASSED                                                                                                               [ 23%] 
tests/test_bff.py::test_ignore_comments_and_blank_lines PASSED                                                                                                 [ 28%] 
tests/test_laser.py::test_btype_A PASSED                                                                                                                       [ 33%] 
tests/test_laser.py::test_btype_B PASSED                                                                                                                       [ 38%] 
tests/test_laser.py::test_btype_C PASSED                                                                                                                       [ 42%] 
tests/test_output.py::test_file_creation PASSED                                                                                                                [ 47%]
tests/test_output.py::test_file_content PASSED                                                                                                                 [ 52%] 
tests/test_output.py::test_empty_placement PASSED                                                                                                              [ 57%]
tests/test_solver.py::test_check_solution_all_targets_hit PASSED                                                                                               [ 61%] 
tests/test_solver.py::test_check_solution_target_missed PASSED                                                                                                 [ 66%] 
tests/test_solver.py::test_check_solution_empty_hits PASSED                                                                                                    [ 71%] 
tests/test_solver.py::test_generate_block_combinations_counts_and_types PASSED                                                                                 [ 76%] 
tests/test_solver.py::test_generate_block_combinations_zero_blocks PASSED                                                                                      [ 80%]
tests/test_solver.py::test_apply_blocks_to_board_adds_blocks_correctly PASSED                                                                                  [ 85%] 
tests/test_solver.py::test_apply_blocks_to_board_does_not_modify_original PASSED                                                                               [ 90%] 
tests/test_solver.py::test_solve_finds_solution PASSED                                                                                                         [ 95%] 
tests/test_solver.py::test_solve_no_solution PASSED                                                                                                            [100%] 

======================================================================== 21 passed in 0.30s ========================================================================= 
'''



## License
This project is licensed under the MIT License. See the license file for details.

## Acknowledgements
TAs  V. Matos, L. Oluoch, and T. Mellor

