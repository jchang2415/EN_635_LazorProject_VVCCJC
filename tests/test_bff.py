# Unit Testing for bff.py #

import pytest
from bff import parse_bff, Board

# Helper function for generating a sample bff file to test parsing


def write_bff(temp_path, text):

    # Generate the file path
    path = temp_path / "test.bff"

    # Write the provided text to the sample bff file
    path.write_text(text.strip(), encoding="utf-8")

    # Return the file path for the generated sample bff file
    return path

# Test methods of the Board class object


def test_board_methods():
    '''
    Test to ensure that methods for Board class objects are working as expected.
    '''

    # Generate example information for a Board class object
    grid = [['A', 'o'], ['x', 'C']]
    counts = {'A': 1, 'B': 0, 'C': 1}
    lasers = [(1, 0, 1, 1)]
    targets = [(5, 2)]

    # Generate a sample Board class object from that information
    board = Board(grid, counts, lasers, targets)

    # Check to see that the helper methods of the Board object return expected
    # values
    assert board.size() == (2, 2)
    assert board.fixed_blocks() == {(0, 0): 'A', (1, 1): 'C'}
    assert board.placeable_slots() == [(0, 1)]

# Test that an invalid grid cell will raise an error


def test_invalid_grid_cell(temp_path):
    '''
    Testing to make sure an invalid grid symbol raises an error.
    '''
    # Generate test content for the bff file with invalid symbol
    content = '''
    GRID START
    o z o
    GRID STOP
    '''

    # Make a test bff file with that content
    path = write_bff(temp_path, content)

    # Attempt to parse the test bff file and ensure that an accurate error is
    # raised
    with pytest.raises(ValueError, match="Invalid grid cell"):
        parse_bff(path)

# Test that parser will catch a missing argument for a laser object in the file


def test_invalid_laser(temp_path):
    '''
    Testing to make sure an invalid laser will raise an error.
    '''

    # Generate test content for the bff file with invalid laser details
    content = """
    GRID START
    o o o
    GRID STOP
    L 1 2 3
    """

    # Make a test bff file with that content
    path = write_bff(temp_path, content)

    # Attempt to parse the test bff file and ensure that an accurate error is
    # raised
    with pytest.raises(ValueError, match="Laser line needs 4 integers"):
        parse_bff(path)

# Test that a missing coordinate for a target will be caught and raise an error


def test_invalid_target(temp_path):
    '''
    Testing to make sure an invalid target will raise an error.
    '''
    # Generate test content for the bff file with invalid target details
    content = """
    GRID START
    o o o
    GRID STOP
    P 1
    """

    # Make a test bff file with that content
    path = write_bff(temp_path, content)

    # Attempt to parse the test bff file and ensure that an accurate error is
    # raised
    with pytest.raises(ValueError, match="Target line needs 2 integers"):
        parse_bff(path)

# Test overall parsing of the bff file


def test_valid_bff_parsing(temp_path):
    '''
    Test that a valid .bff file is parsed correctly and generates an accurate Board class object.
    '''
    # Generate test content for a sample valid bff file
    content = """
    GRID START
    o x o
    A o B
    GRID STOP

    A 1
    B 2
    C 0

    L 1 0 1 1
    P 2 3
    """

    # Make a test bff file with that content
    path = write_bff(temp_path, content)

    # Use the function to parse the test file
    board = parse_bff(path)

    # Check that correct information was extracted from the .bff file as
    # expected
    assert board.grid == [['o', 'x', 'o'], ['A', 'o', 'B']]
    assert board.movable_counts == {'A': 1, 'B': 2, 'C': 0}
    assert board.lasers == [(1, 0, 1, 1)]
    assert board.targets == [(2, 3)]

    # Check that helper methods are functional with Board class object parsed
    # from .bff file
    assert board.size() == (2, 3)
    assert board.fixed_blocks() == {(1, 0): 'A', (1, 2): 'B'}
    assert board.placeable_slots() == [(0, 0), (0, 2), (1, 1)]

# Test that the parser correctly ignores comments and blank lines in bff files


def test_ignore_comments_and_blank_lines(temp_path):
    '''
    Testing to ensure that the parser ignores comment lines (starting with "#") and blank lines.
    '''

    content = """
    # Ignorable comment at start
    GRID START

    o   x   o   # inline comment after row
    # This comment should be ignored too
    o   o   o

    GRID STOP

    # Define movable block counts
    A 2
    B 1
    C 0

    # Lasers and targets
    L 1 0 1 1

    # Another test comment

    P 2 3
    """

    # Make a test bff file with that content
    path = write_bff(temp_path, content)

    # Parse the test file
    board = parse_bff(path)

    # Verify correct parsing occurred
    assert board.grid == [['o', 'x', 'o'], ['o', 'o', 'o']]
    assert board.movable_counts == {'A': 2, 'B': 1, 'C': 0}
    assert board.lasers == [(1, 0, 1, 1)]
    assert board.targets == [(2, 3)]

    # Check board helper methods
    assert board.size() == (2, 3)
    assert board.placeable_slots() == [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]
