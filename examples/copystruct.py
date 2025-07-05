from mcstructure import Structure

with open("examples/structures/large_nether.mcstructure", "rb") as f:
    struct = Structure.load(f)

with open("examples/pack/src/structures/large_nether.mcstructure", "wb") as f:
    struct.dump(f)
