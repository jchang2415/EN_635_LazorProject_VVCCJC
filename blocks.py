# Block Class Definition #

# Defines the "block" class

# Placeholder file for organization purposes

class Block: 
    def __init__(self, block_type, x, y): #block_type can be "A", "B", or "C"
        self.type = block_type
        self.x = x #Position of the block ON X axis
        self.y = y #Position of the block ON Y axis

    def interact(self, vx, vy):
        if self.type == "A":  #Need to Reflect
            return -vx, vy
        elif self.type == "B":  #Need to Absorb
            return None
        elif self.type == "C":  #Need to Reflect + Pass
            return [(-vx, vy), (vx, vy)]  #First reflect, then pass throuh
