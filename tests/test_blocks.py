# Unit Testing blocks.py #

import pytest
from blocks import ReflectBlock, OpaqueBlock, RefractBlock, BLOCKS

# Testing to make sure that our type A blocks correctly reflect lasers
# when hit on vertical edge


def test_btype_A_vert_reflect():
    '''
    Test to ensure our A type blocks correctly reflect vertical edge laser hits.
    '''

    # Make a sample Reflect Block using the class function
    block = ReflectBlock()

    # Add sample attributes for a laser beam
    pos = (2, 3)
    dir_in = (1, 1)

    # Use the interact() method of the block
    result = block.interact(pos, dir_in, vert_edge=True)

    # Check to see if the result of the interaction is as expected
    # (horizontally flipped direction)
    assert result == [(pos, (-1, 1))]

# Testing to make sure that our type A blocks correctly reflect horizontal
# hits from lasers


def test_btype_A_hor_reflect():
    '''
    Test to ensure our A type blocks correctly reflect horizontal edge laser hits.
    '''
    # Make a sample Reflect Block using the class function
    block = ReflectBlock()

    # Add sample attributes for a laser beam
    pos = (1, 2)
    dir_in = (1, 1)

    # Use the interact() method of the block
    result = block.interact(pos, dir_in, vert_edge=False)

    # Check to see if the result of the interaction is as expected (vertically
    # flipped direction)
    assert result == [(pos, (1, -1))]

# Testing to make sure our type A block has a functional "kind" attribute


def test_btype_A_kind():
    '''
    Test to ensure the .kind attribute is functional for btype A blocks
    '''
    # Make a sample Reflect Block using the class function
    block = ReflectBlock()

    # Check that the .kind attribute returns the correct block type
    assert block.kind == "A"

# Repeat for other two block types, with their own expected interact() effect

# Testing to ensure that our type B block absorbs laser beams


def test_btype_B_absorb():
    '''
    Test to ensure that the Type B Opaque block obsorbs laser beams and returns an empty list.
    '''
    # Create a sample Opaque Block object
    block = OpaqueBlock()

    # Generate sample attributes for laser
    pos = (3, 4)
    dir_in = (1, -1)

    # Try interacting laser beam with Opaque block on both edge types
    result_vert = block.interact(pos, dir_in, vert_edge=True)
    result_horz = block.interact(pos, dir_in, vert_edge=False)

    # Check that the beam is absorbed in both cases
    assert result_vert == []
    assert result_horz == []

# Test that the .kind attribute is functional for Type B blocks as well as
# above


def test_opaque_block_kind():
    '''
    Check that the OpaqueBlock has the correct 'kind' attribute.
    '''
    # Create a sample Opaque Block object
    block = OpaqueBlock()

    # Check that the .kind attribute is functional and returns as expected
    assert block.kind == 'B'

# Test that the refract block correctly refracts lasers on vertical edge hit


def test_btype_C_vert():
    '''
    Test to ensure that the Refract Block correctly splits a laser into a reflected beam and a transmitted beam when hit on the vertical edge.
    '''
    # Generate a sample Refract Block object
    block = RefractBlock()

    # Generate sample laser
    pos = (3, 4)
    dir_in = (1, 1)

    # Interact laser beam with sample refract block
    result = block.interact(pos, dir_in, vert_edge=True)

    # Check that the interaction occurs as expected (2 beams result; one
    # reflected, one passing through)
    assert len(result) == 2
    assert (pos, (1, 1)) in result
    assert (pos, (-1, 1)) in result

# Test refract block for the same thing on a horizontal edge hit


def test_btype_C_hor():
    '''
    Test to ensure that the Refract Block correctly splits a laser into a reflected beam and a transmitted beam when hit on the horizontal edge.
    '''
    # Generate a sample Refract Block object
    block = RefractBlock()

    # Generate sample laser
    pos = (3, 4)
    dir_in = (1, 1)

    # Interact laser beam with sample refract block
    result = block.interact(pos, dir_in, vert_edge=False)

    # Check that the interaction occurs as expected (2 beams result; one
    # reflected, one passing through)
    assert len(result) == 2
    assert (pos, (1, 1)) in result
    assert (pos, (1, -1)) in result

# Test that the .kind attribute is functional for Refract Blocks


def test_btype_C_kind():
    '''
    Test to ensure the .kind attribute is functional for type C blocks
    '''
    # Generate sample Refract Block
    block = RefractBlock()

    # Check that the .kind attribute returns the expected result
    assert block.kind == 'C'

# Test to ensure that the BLOCKS dictionary has correct mapping of btypes


def test_blocks_dict_contains_correct_types():
    '''
    Ensure BLOCKS dictionary maps the correct string keys to block instances.
    '''
    assert set(BLOCKS.keys()) == {'A', 'B', 'C'}

    # Check that the types of the dictionary values are correct
    assert isinstance(BLOCKS['A'], ReflectBlock)
    assert isinstance(BLOCKS['B'], OpaqueBlock)
    assert isinstance(BLOCKS['C'], RefractBlock)
