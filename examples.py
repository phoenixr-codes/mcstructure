from src.mcstructure import Block, Structure

struct = Structure(
    (6, 6, 6),  # Size of the Structure     声明结构大小，注意这是大小，其坐标从0开始
    Block("minecraft:air")	# pre-fill blocks   预填充方块
)

# fill blocks  填充方块
struct.set_blocks((1,1,1),(4,1,4),Block("minecraft:iron_block"))

# display stuffs in it  显示一些东西
print(struct.get_structure())
print(struct._get_str_array(False,True))

# write into file  写入文件
with open("example.mcstructure", "wb") as f:
    struct.dump(f)