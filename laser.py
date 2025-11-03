# Laser Simulation #
'''
Defines a function for simulating the path of a laser for a given board configuration.
'''
from blocks import BLOCKS

def hit_block(blocks, x_laser, y_laser):
    '''
    Helper function that checks if a laser position would hit a block + returns the type of block hit as well as the edge (horizontal or vertical) that was hit.

    If no block would be hit, returns None, None.

    Assumes input of a "blocks" dictionary that has the (x, y) of the center of the block as keys and the type of the block as the value.

    **Arguments**

        blocks: *dict[tuple, str]*
            A dictionary of the blocks

        x_laser: *int*
            X-coordinate of the laser position.

        y_laser: *int*
            Y-coordinate of the laser position.

    **Returns**

        b_type: *str*
            A string "A", "B", or "C" that tells you the type of block that was hit by the provided laser.

        orientation: *str*
            A string "vertical" or "horizontal" that tells you the orientation of edge that was hit on the block.

    '''
    edges = [
         (-1, 0, "vertical"),
         (1, 0, "vertical"),
         (0, -1, "horizontal"),
         (0, 1, "horizontal")
    ]

    for dx, dy, orientation in edges:

        edge = (x_laser + dx, y_laser + dy)

        if edge in blocks:

            b_type = blocks[edge]

            return b_type, orientation

    return None, None 

def laser_path(board):
    '''
    Function that calculates the path a laser will take for the provided Lazor board.

    **Arguments**

        board: *object of class Board*
            Object of the class "Board" that contains the details of a particular Lazor board set-up.
            Obtained from parse_bff() function on a .bff file.

    **Returns**

        all_paths: *list, set, tuple, int*
            A list of sets, one for each laser on the board.
            Each set is a set of tuples containing the (x,y) points that the particular laser will pass through for the given board set-up.


    '''
    # Obtain dimensions of the board
    rows, cols = board.size()

    # Obtain list of lasers for the board
    lasers = list(board.lasers) #Changed and fixed

    # Obtain list of block positions for the board   ### NOT YET IN BFF PARSER FILE! Need to add? Or is this logic wrong; should this instead be a 2nd argument?
    blocks = board.blocks
    
    # Initialize empty variable to hold all hit paths calculated
    all_paths = []

    # While the queue of lasers to process is still not empty
    while lasers:

        # Pop off the next laser + sort information from the laser
        x, y, vx, vy = lasers.pop(0)
        
        # Initialize empty set to hold the points the laser hits
        hit_path = set()

        # Initialize empty set to hold already-visited "states" (both position and vx, vy) to prevent infinite loops
        visited_states = set()

        # Extrapolate path of lazer until it leaves the board or is absorbed
        while 0 <= x < (cols*2) and 0 <= y < (rows*2):

            # Add current (x,y) coordinates to "hit_path"
            hit_path.add((x, y))

            # Check for infinite loops
            state = (x, y, vx, vy)

            # If the current state has already been visited, break the loop, as no new paths will be discovered
            if state in visited_states:

                break

            # Otherwise, add the current state to "visited_states"
            visited_states.add(state)

            # Calculate the next position
            x_new = x + vx
            y_new = y + vy

            # Check that the laser is still inside the grid
            if not (0 <= x_new < (cols*2) and 0 <= y_new < (rows*2)):

                # If the laser has left the grid, break the loop and move onto the next laser
                break

            # Check to see if the laser intersects a block;  USING DICTIONARY FOR BLOCKS NOW FOR BETTER SEARCH EFFICIENCY

            # Check to see if the laser hits a block + get block type and hit orientation if so
            b_type, orientation = hit_block(blocks, x_new, y_new)

            # If type is not none, then the laser hits a block
            if b_type:

                # To integrate with Block class, set vert_edge as TRUE if orientation == "vertical"
                vert_edge = (orientation == "vertical")

                # Use the block type of the block hit to generate a Block class object
                block_hit = BLOCKS[b_type]

                # Use the block to object and the interact() method to determine what happens when the laser hits the block
                results = block_hit.interact((x_new, y_new), (vx, vy), vert_edge)

                # Use the generated results to generate the resulting laser beams from the interaction
                for new_pos, new_dir in results:

                    # Define the starting position of the new laser
                    nx, ny = new_pos

                    # Define the vx vy of the new laser
                    vx2, vy2 = new_dir

                    # Add the new laser(s) to the list of lasers; generates a copy of the original laser as well
                    lasers.append((nx, ny, vx2, vy2)) #changed -> fixed

                # Delete the current laser beam
                break                  

            # Advance the laser to the next position
            x, y = x_new, y_new

        # Add the hit path for the specific laser to the list of ALL laser paths
        all_paths.append(hit_path)

    # Return all calculated paths
    return all_paths




