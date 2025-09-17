from mcstructure import Block, Structure
from pathlib import Path

here = Path(__file__).parent

BLOCK = Block("minecraft:grass")

struct = Structure((10, 10, 10), BLOCK)
(
    struct.set_block((0, 0, 0), BLOCK)
    .set_block((1, 1, 1), BLOCK)
    .set_block((2, 2, 2), BLOCK)
    .set_block((3, 3, 3), BLOCK)
    .set_block((4, 4, 4), BLOCK)
    .set_block((5, 5, 5), BLOCK)
)

with here.joinpath("out/diagonal.mcstructure").open("wb") as f:
    struct.dump(f)
