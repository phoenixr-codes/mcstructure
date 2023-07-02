# Quickstart

## Loading a Structure

```python
from mcstructure import Structure

with open("house.mcstructure", "rb") as f:
    struct = Structure.load(f)
```


## Viewing a Structure

```python
struct.size  # The size of the structure
struct.get_block(1, 1, 1)  # Get the block at (1, 1, 1)
struct.get_structure()  # Get the numpy array representing the structure
```


## Modifying a Structure

```python
from mcstructure import Block

struct.mirrow("x")  # Mirrow the structure on the x axis
struct.rotate(90)  # Rotate the structure by 90 degrees
struct.set_block((1, 1, 1), Block("minecraft:wool", color="red"))  # Puts a red wool block at (1, 1, 1)
struct.set_blocks((1, 1, 1), (5, 5, 5), Block("minecraft:wool", color="red"))  # Puts red wool blocks from (1, 1, 1) to (5, 5, 5)
```


## Saving a Structure

```python
with open("mansion.mcstructure", "wb") as f:
    struct.dump(f)
```
