from mcstructure import Block, Structure
import nbtx
from pathlib import Path

here = Path(__file__).parent

struct = Structure((2, 2, 2), Block("minecraft:air"))

struct.set_block(
    (0, 0, 0),
    Block(
        "minecraft:birch_stairs",
        upside_down_bit=False,
        weirdo_direction=2,
        waterlogged=True
    )
)

with here.joinpath("out/waterlogged.mcstructure").open("wb") as f:
    struct.dump(f)
