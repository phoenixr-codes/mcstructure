from mcstructure import Block, Structure

struct = Structure(
    (2, 2, 2),  # Size of the Structure     声明结构大小，注意这是大小，其坐标从0开始
    Block("minecraft:air"),  # pre-fill blocks   预填充方块
)

# fill blocks  填充方块
struct.set_block((1, 1, 1), Block("minecraft:iron_block"))

# write into file  写入文件
with open("structures/my_simple.mcstructure", "wb") as f:
    struct.dump(f)
