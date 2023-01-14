<p align="center">
  <img
    src="https://raw.githubusercontent.com/phoenixr-codes/mcstructure/main/logo.png"
    width="120px"
    align="center" alt="mcstructure logo"
  />
  <h1 align="center">mcstructure</h1>
  <p align="center">
    Read and write Minecraft <code>.mcstructure</code> files.
  </p>
</p>

_In the entire project (and officially since 
the "Better Together Update") the term
"Minecraft" refers to the edition of Minecraft
that is also known as "Bedrock Edition"._

_Features that this library provide are only
useful for the above named edition of Minecraft._

> **Warning**
> This project is currently in BETA Version. Most
> features will probably not work.

This library lets you programmatically create
and edit Minecraft structures. You are able to
save these as ``.mcstructure`` files and for
example use them in behavior packs.

You may aswell read them and identify blocks and
and entities that were saved with a Structure
Block in-game.


Installation
------------

```bash
pip install mcstructure
```


Basic Usage
-----------

```python
from mcstructure import Block, Structure

struct = Structure(
    (7, 7, 7),
    Block("minecraft:wool", color = "red")
)

(struct
    .set_block((1, 1, 1), Block("minecraft:grass"))
    .set_block((2, 2, 2), Block("minecraft:grass"))
    .set_block((3, 3, 3), Block("minecraft:grass"))
    .set_block((4, 4, 4), Block("minecraft:grass"))
    .set_block((5, 5, 5), Block("minecraft:grass"))
    .set_block((6, 6, 6), Block("minecraft:grass"))
)

with open("house.mcstructure", "wb") as f:
    struct.dump(f)

```

```python
with open("house.mcstructure", "rb") as f:
    struct = Structure.load(f)

```

--------------------------------------------

NOT AN OFFICIAL MINECRAFT PRODUCT.
NOT APPROVED BY OR ASSOCIATED WITH MOJANG.
