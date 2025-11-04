# Lazor Project (Vedant, Cam, and Jason)
This repository contains code for solving problems in the "Lazors" game available on Steam and iPhone when provided with a ".bff" file describing the board set-up for the problem.

## Files
*bff.py* - Board class and .bff file parser.  
*blocks.py* - Base block class and subclasses.  
*laser.py* - Simulates laser movement on the board.  
*solver.py* - Generates all possible placements of blocks on the board, simulates laser and checks weather target was hit.  
*output.py* - Writes solution output.  
*main.py* - Allows command line entry.  
*tests/test_<testname>.py* - Contains the various unit tests.  

## Features
The program will:
1. Parse the .bff file from the sample_bff_files/ folder  
2. Search for a valid configuration of blocks  
3. Simulate laser paths until all targets are hit  
4. Save a solution file as a .txt file to the output/ directory

Supported Lazor Block Types:  
- **A (Reflect) Blocks**
- **B (Opaque) Blocks**
- **C (Refract) Blocks**


## Installation
Download the GitHub repository as a .zip file.
For unit testing, install the pytest module by running the following command:  
pytest install

## Usage
To solve a puzzle using this code, download the relevant .bff file and run the function using:  
python main.py <filename.bff>  (e.g. python main.py dark_1.bff)  
The output will be generated in a folder called "outputs" as a txt file named filename_solution.txt containing the grid with blocks placed in the solution configuration in a format similar to the .bff file input.  
Sample Console Output:  
<img width="1247" height="202" alt="image" src="https://github.com/user-attachments/assets/563e02ae-9bd2-448a-b756-44cebdaff40d" />


## Running Unit Tests
To run unit tests, make sure pytest is installed. If not installed, install it using:  
pip install pytest  
Then run the unit tests using this command:  
python -m pytest -v  

Example Output:  
<img width="1503" height="550" alt="image" src="https://github.com/user-attachments/assets/00b62028-e666-4fcc-a2f5-f25df489521b" />

  

## Authors
Jason Chang  
Vedant Vaidya  
Cameron Cash  

EN.540.635 Software Carpentry
Johns Hopkins University, Chemical and Biomolecular Engineering Department

## License
This project is licensed under the MIT License. See the license file for details.

## Acknowledgements
TAs  V. Matos, L. Oluoch, and T. Mellor
