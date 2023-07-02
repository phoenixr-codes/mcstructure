from mcstructure import Structure

with open("structures/dirt_house.mcstructure", "rb") as f:
    struct = Structure.load(f)

print(struct)
