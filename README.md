# Lazor Project (Vedant, Cam, and Jason)
This repository contains code for solving problems in the "Lazors" game available on Steam and iPhone when provided with a ".bff" file describing the board set-up for the problem.

## Files
bff.py- Board class and .bff file parser.
blocks.py- Base block class and subclasses.
laser.py- Simulates laser movement on the board.
solver.py- Generates all possible placements of blocks on the board, simulates laser and checks weather target was hit. 
output.py- Writes solution output.
main.py- Allows command line entry.
tests.py- COntains unit tests.

## Installation
pytest install, sys install, time install

## Usage
The function can be called by main.py <filename.bff>
The output will be a txt file named filename_solution.txt containing the grid with blocks placed in the solution configuration in a format similar to the .bff file input.

## License
This project is licensed under the MIT License. See the license file for details.

## Acknowledgements
TAs  V. Matos, L. Oluoch, and T. Mellor

