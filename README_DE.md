<p align="center">
  <img
    src="https://raw.githubusercontent.com/phoenixr-codes/mcstructure/main/logo.png"
    width="120px"
    align="center" alt="mcstructure logo"
  />
  <h1 align="center">mcstructure</h1>
  <p align="center">
    Lesen und Schreiben von Minecraft <code>.mcstructure</code>-Dateien.
  </p>
</p>

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Diese README-Datei ist auch in den folgenden
Sprachen verfügbar:

* [🇨🇳 Chinesisch](https://github.com/phoenixr-codes/mcstructure/blob/main/README_CN.md)
* [🇬🇧 Englisch](https://github.com/phoenixr-codes/mcstructure/blob/main/README.md)

_Im gesamten Projekt (und offiziell seit dem
"Better Together Update") ist mit "Minecraft"
die Version gemeint, welche auch als "Bedrock
Edition" bekannt ist._

_Features dieser Bibliothek sind nur in der
oben genannten Edition von Minecraft nützlich._

> **Warning**
> Dieses Projekt ist momentan in der BETA Version.
> Die meisten Features sind somit instabil.

Diese Bibliothek ermöglicht es innerhalb eines
Programmes Minecraft Strukturen zu editieren.
Diese können dann als ``.mcstructure``-Datei
gespeichert werden und beispielsweise in einem
Verhaltenspaket genutzt werden.

Es ist auch möglich Blöcke und Entitäten zu
identifizieren, welche mit einem Konstruktionsblock
innerhalb des Spiels gespeichert wurden.


Installation
------------

```bash
pip install mcstructure
```


Demonstration
-------------

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

KEIN OFFIZIELLES MINECRAFT PRODUKT.
NICHT VON MOJANG GENEHMIGT ODER MIT MOJANG
ASSOZIIERT.
