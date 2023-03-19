from mcstructure import Structure

with open(input("path:"), "rb") as f:
    struct = Structure.load(f)

print(struct)
