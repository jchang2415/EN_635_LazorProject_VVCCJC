"""
Defines block types for the Lazor puzzle and how each block type interacts with an
incoming laser ray at an impact point.
"""
from typing import Dict, Tuple, List

class Block:
    """
    Base block class.

    Attributes
        kind : str
            Single letter identifying the block type (e.g., 'A', 'B', 'C').
    Methods
        interact(pos, dir, vert_edge)
            Return outgoing ray(s) after impact.
    """
    kind: str
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        raise NotImplementedError

class ReflectBlock(Block):
    """
    A: reflect lazor at 90°.
        - vertical block face (even x, odd y): flip vx  -> (−vx,  vy)
        - horizontal block face  (odd x, even y): flip vy -> ( vx, −vy)
    
    Attributes
        kind : str
            'A'
    Methods
        interact(pos, dir, vert_edge)
            Return one reflected ray with flipped vx (vertical edge) or vy (horizontal edge).
    """
    kind = 'A'
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        vx, vy = dir
        if vert_edge:
            return [(pos, (-vx, vy))]
        else:
            return [(pos, (vx, -vy))]

class OpaqueBlock(Block):
    """
    B: absorbs beam

    Attributes
        kind : str
            'B'
    Methods
        interact(pos, dir, vert_edge)
            Returns an empty list (laser absorbed).
    """
    kind = 'B'

    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        return [] #returns empty list(the laser is absorbed)

class RefractBlock(Block):
    """
    C: refracts lazor, allows lazor to pass through and reflects at 90° like ReflectBlock class.

    Attributes
        kind : str
            'C'.
    Methods
        interact(pos, dir, vert_edge)
            Return two rays: straight-through and 90° reflection.
    """
    kind = 'C'
    def interact(self, pos: Tuple[int, int], dir: Tuple[int, int], vert_edge: bool):
        vx, vy = dir
        if vert_edge:
            return [(pos, dir), (pos, (-vx, vy))]
        else:
            return [(pos, dir), (pos, (vx, -vy))]

BLOCKS: Dict[str, Block] = { 'A': ReflectBlock(), 'B': OpaqueBlock(), 'C': RefractBlock(),}


