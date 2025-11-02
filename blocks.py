@dataclass(frozen=True)
class Vec:
    x: int
    y: int
    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)
    def tup(self) -> Tuple[int,int]:
        return (self.x, self.y)

class Block:
    kind: str
    def interact(self, pos, dir, vert_edge: bool) -> List[Tuple[Vec, Vec]]:
        raise NotImplementedError

class ReflectBlock(Block):
    """
    A: reflect lazor at 90°.
        - vertical block face (even x, odd y): flip vx  -> (−vx,  vy)
        - horizontal block face  (odd x, even y): flip vy -> ( vx, −vy)
    """
    kind = 'A'
    def interact(self, pos: Vec, dir: Vec, vert_edge: bool) -> List[Tuple[Vec, Vec]]:
        vx,vy = dir.x, dir.y
        if vert_edge:
            return [(pos, Vec(-vx, vy))]
        else:
            return [(pos, Vec(vx, -vy))]

class OpaqueBlock(Block):
    """
        B: absorbs beam.
    """
    kind = 'B'
    def interact(self, pos: Vec, dir: Vec, vert_edge: bool) -> List[Tuple[Vec, Vec]]:
        return []

class RefractBlock(Block):
    """
        C: refracts lazor, allows lazor to pass through and reflects at 90° like ReflectBlock class
    """
    kind = 'C'
    def interact(self, pos: Vec, dir: Vec, vert_edge: bool) -> List[Tuple[Vec, Vec]]:
        vx, vy = dir.x, dir.y
        if vert_edge:
            return [(pos,dir),(pos, Vec(-vx, vy))]
        else:
            return [(pos,dir),(pos, Vec(vx, -vy))]

BLOCKS: Dict[str, Block] = { 'A': ReflectBlock(), 'B': OpaqueBlock(), 'C': RefractBlock(),}
