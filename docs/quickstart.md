# Quickstart

## Loading/Initializing a Structure

You can load a pre-existing structure by using the {py:meth}`mcstructure.Structure.load` method.

```python
from mcstructure import Structure

with open("house.mcstructure", "rb") as f:
    struct = Structure.load(f)
```

Alternatively, create a new empty structure:

```python
from mcstructure import Block, Structure

struct = Structure(
    (12, 20, 5),  # size of the structure
    Block("minecraft:wool", color="red")  # fill the structure with red wool
)
```


## Inspecting a Structure

```python
struct.size  # The size of the structure
struct.get_block(1, 1, 1)  # Get the block at (1, 1, 1)
struct.get_structure()  # Get the numpy array representing the structure
```


## Viewing a Structure

You can simply print the structure object:

```python
print(struct)
```


## Modifying a Structure

Simple modifications such as placing blocks:

```python
from mcstructure import Block

struct.set_block((1, 1, 1), Block("minecraft:wool", color="red"))  # Places a red wool block at (1, 1, 1)
struct.set_blocks((1, 1, 1), (5, 5, 5), Block("minecraft:wool", color="red"))  # Places red wool blocks from (1, 1, 1) to (5, 5, 5)
```

Advanced modifications can be achieved with [numpy](https://numpy.org/doc/stable/index.html).
A structure object consists of an array of integers representing IDs. Each ID is associated
with a {py:class}`mcstructure.Block` in a list.

```python
import numpy as np

np.rot90(struct.structure)
struct.structure = np.transpose(struct.structure)
```


## Saving a Structure

```python
with open("mansion.mcstructure", "wb") as f:
    struct.dump(f)
```
