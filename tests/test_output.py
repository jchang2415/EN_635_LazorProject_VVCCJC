# Unit Testing #

# Unit testing function for writing solution to an output file in
# human-readable format (output.py)

import pytest
import os
from tempfile import NamedTemporaryFile
from types import SimpleNamespace
from output.py import write_solution

# Generate a sample board to grid to test the function


@pytest.fixture
def mock_board():
    '''
    Fixture to create a sample Lazor board for testing.
    '''
    return SimpleNamespace(
        grid=[
            ["x", "o", "o"],
            ["o", "o", "o"],
            ["x", "o", "x"]
        ]
    )

# Generate a sample solution (in the form of a "placement" dictionary that
# our solver would generate)


@pytest.fixture
def mock_placement():
    '''
    Fixture to create a sample Lazor board solution in the form of a "placement" dictionary for testing.
    '''
    return {
        (0, 1): "A",
        (0, 2): None,
        (1, 0): 'B',
        (1, 1): None,
        (1, 2): 'C',
        (2, 1): None
    }

# Test that an output file is indeed generated


def test_file_creation(mock_board, mock_placement):
    '''
    Tests that the write_solution() function successfully generates an output file.
    '''
    with NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    # Try to use the write_solution() function to generate an output file
    try:
        write_solution(mock_board, mock_placement, tmp_path)

        # Make sure that the output file path actually exists
        assert os.path.exists(tmp_path)

    # Remove the test file again
    finally:
        os.remove(tmp_path)

# Test that the generated output file has the expected contents written to it


def test_file_content(mock_board, mock_placement):
    '''
    Tests that the write_solution() function successfully writes the solution in the correct format to the output file.
    '''
    with NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp_path = tmp.name

    # Try to use the write_solution() function to generate an output file
    try:
        write_solution(mock_board, mock_placement, tmp_path)

        # Open the generated output file
        with open(tmp_path, "r", encoding="utf-8") as f:
            contents = f.read().strip()

        # Define what the expected file contents for the output file are
        expected_body = "\n".join([
            "x A o",
            "B o C",
            "x o x"
        ])

        expected_output = f"Lazor Problem Solution: \n\n{expected_body}"

        # Check that the generated output file does indeed contain the expected
        # contents
        assert expected_output in contents

    # Remove the test file again
    finally:
        os.remove(tmp_path)

# Test that the write_solution() function doesn't change the board if an
# empty placement function is provided


def test_empty_placement(mock_board):
    '''
    Test that an empty placement leaves the board unchanged.
    '''
    # Generate an empty placement for testing
    empty_placement = {}

    with NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp_path = tmp.name

    # Use the write_solution() function to generate an output file using the
    # empty placement variable
    try:
        write_solution(mock_board, empty_placement, tmp_path)

        # Open up the generated output file
        with open(tmp_path, "r", encoding="utf-8") as f:
            contents = f.read()

        # Check that the generated output file does not have added blocks in it
        assert "A" not in contents
        assert "B" not in contents
        assert "C" not in contents

    # Remove the test file again
    finally:
        os.remove(tmp_path)
