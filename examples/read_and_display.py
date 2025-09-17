from mcstructure import Structure
from pathlib import Path

here = Path(__file__).parent

with here.joinpath("../structures/dirt_house.mcstructure").open("rb") as f:
    struct = Structure.load(f)

print(struct)
