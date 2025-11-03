class Block:
    kind: str
    def interact(self, pos, dir, vert_edge: bool):
        raise NotImplementedError

class ReflectBlock(Block):
    """
    A: reflect lazor at 90°.
        - vertical block face (even x, odd y): flip vx  -> (−vx,  vy)
        - horizontal block face  (odd x, even y): flip vy -> ( vx, −vy)
    """
    kind = 'A'
    def interact(self, pos, dir, vert_edge: bool):
        vx,vy = dir.x, dir.y
        if vert_edge:
            return [(pos, (-vx, vy))]
        else:
            return [(pos, (vx, -vy))]

class OpaqueBlock(Block):
    """
        B: absorbs beam.
    """
    kind = 'B'

    def interact(self, pos, dir, vert_edge: bool):
        return []

class RefractBlock(Block):
    """
        C: refracts lazor, allows lazor to pass through and reflects at 90° like ReflectBlock class
    """
    kind = 'C'
    def interact(self, pos, dir, vert_edge: bool):
        vx, vy = dir.x, dir.y
        if vert_edge:
            return [(pos,dir),(pos,(-vx, vy))]
        else:
            return [(pos,dir),(pos,(vx, -vy))]

BLOCKS: Dict[str, Block] = { 'A': ReflectBlock(), 'B': OpaqueBlock(), 'C': RefractBlock(),}
