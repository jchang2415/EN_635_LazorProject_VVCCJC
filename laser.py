# Lazer Simulation #
'''
Defines a function for simulating the path of a laser for a given board configuration.
'''

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
    lasers = board.lasers

    # Obtain list of block positions for the board   ### NOT YET IN BFF PARSER FILE! Need to add? Or is this logic wrong; should this instead be a 2nd argument?
    blocks = board.blocks
    
    # Initialize empty variable to hold all hit paths calculated
    all_paths = []

    # Iterate over all the lasers for the board
    for laser in lasers:

        # Sort information from the laser
        x, y, vx, vy = laser
        
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
            if not (0 <= x < (cols*2) and 0 <= y < (rows*2)):

                # If the laser has left the grid, break the loop and move onto the next laser
                break

            # Check to see if the laser intersects a block;  ASSUMING FOR NOW WE HAVE LIST OF BLOCK TYPES AND COORDINATES (in form (type, x, y))
            
            # Iterate through all blocks     <-- MAYBE NOT EFFICIENT
            for block in blocks:

                # Obtain block type and position
                type, x_block, y_block = block

                # Check to see if the laser is hitting the block on the top or bottom sides
                if (x_new, y_new) == (x_block, y_block + 1) or (x_new, y_new) == (x_block, y_block - 1):

                    # Check block type and proceed accordingly

                    # Reflect type block
                    if type == "A":

                        # If it hits, reflect the path of the laser accordingly (flip vy)
                        vy = -vy

                        # Break the for loop cause it can't hit any other blocks
                        break

                    # Opaque type block
                    elif type == "B":

                        # Absorb laser and stop loop
                        break

                    # Refract type block
                    elif type == "C":
                        
                        # Create a new lazor originating from that point with the same (unreflected) state
                        lasers.append((x_new, y_new, vx, vy))

                        # Reflect original lazer
                        vy = -vy


                # Check to see if the laser is hitting the block on the left or right sides
                elif (x_new, y_new) == (x_block + 1, y_block) or (x_new, y_new) == (x_block - 1, y_block):

                    # Check block type and proceed accordingly

                    # Reflect type block
                    if type == "A":

                        # If it hits, reflect the path of the laser accordingly (flip vx)
                        vx = -vx

                        # Break the for loop cause it can't hit any other blocks
                        break

                    # Opaque type block
                    elif type == "B":

                        # Absorb laser and stop loop
                        break

                    # Refract type block
                    elif type == "C":

                        # Create a new lazor originating from that point with the same (unreflected) state
                        lasers.append((x_new, y_new, vx, vy))
                        
                        # Reflect original lazer
                        vx = -vx

                # Otherwise if it doesn't hit the block, do nothing and move onto the next block
                else:

                    next

            # Advance the laser to the next position
            x, y = x_new, y_new

        # Add the hit path for the specific laser to the list of ALL laser paths
        all_paths.append(hit_path)

    # Return all calculated paths
    return all_paths

