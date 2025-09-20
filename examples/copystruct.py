from mcstructure import Structure
from pathlib import Path

here = Path(__file__).parent

with here.joinpath("../samples/large_nether.mcstructure").open("rb") as f:
    struct = Structure.load(f)

with here.joinpath("out/large_nether.mcstructure").open("wb") as f:
    struct.dump(f)
