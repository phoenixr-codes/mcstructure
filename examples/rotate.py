from mcstructure import Block, Structure

def get() -> Structure:
    with open("structures/dirt_house.mcstructure", "rb") as f:
        return Structure.load(f)

struct = get()
struct.rotate(90)
with open("structures/my_house90.mcstructure", "wb") as f:
    struct.dump(f)

struct = get()
struct.rotate(180)
with open("structures/my_house180.mcstructure", "wb") as f:
    struct.dump(f)

struct = get()
struct.rotate(270)
with open("structures/my_house270.mcstructure", "wb") as f:
    struct.dump(f)
