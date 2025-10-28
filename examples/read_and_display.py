from mcstructure import Structure
from pathlib import Path

here = Path(__file__).parent

with here.joinpath("../samples/dirt_house.mcstructure").open("rb") as f:
    struct = Structure.load(f)
    print("Dirt House")
    print(struct)

with here.joinpath("../samples/waterlogged.mcstructure").open("rb") as f:
    struct = Structure.load(f)
    print("Waterlogged Stairs")
    print(struct._palette)
