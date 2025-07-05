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

🌍 Diese README-Datei ist auch in den folgenden
Sprachen verfügbar:

* [🇨🇳 Chinesisch](./README_CN.md)
* [🇬🇧 Englisch](./README.md)

<h2></h2>

[![Code-Stil](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![Dokumentationsstatus](https://readthedocs.org/projects/mcstructure/badge/?style=for-the-badge&version=latest)](https://mcstructure.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/mcstructure?style=for-the-badge)](https://pypi.org/project/mcstructure)

_Im gesamten Projekt (und offiziell seit dem
"Better Together Update") ist mit "Minecraft"
die Version gemeint, welche auch als "Bedrock
Edition" bekannt ist._

_Features dieser Bibliothek sind nur in der
oben genannten Edition von Minecraft nützlich._

> [!WARNING]
> Dieses Projekt ist momentan in der BETA Version.
> Die meisten Features sind somit instabil.

Diese Bibliothek ermöglicht es innerhalb eines
Programmes Minecraft Strukturen zu editieren.
Diese können dann als ``.mcstructure``-Datei
gespeichert werden und beispielsweise in einem
Verhaltenspaket genutzt werden.

Es ist auch möglich, Blöcke und Entitäten zu
identifizieren, welche mit einem Konstruktionsblock
innerhalb des Spiels gespeichert wurden.


Installation
------------

```console
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


Nützliche Links
---------------

* [📖 Dokumentation](https://mcstructure.readthedocs.io/en/latest/)
* [📁 Quellcode](https://github.com/phoenixr-codes/mcstructure)
* [🐍 PyPI](https://pypi.org/project/mcstructure/)

### Externe Resourcen

* [👋 Einführung zu Konstruktionsblöcken](https://learn.microsoft.com/en-us/minecraft/creator/documents/introductiontostructureblocks)
* [📖 Bedrock Wiki](https://wiki.bedrock.dev/nbt/mcstructure.html#file-format)


--------------------------------------------

NOT AN OFFICIAL MINECRAFT PRODUCT.
NOT APPROVED BY OR ASSOCIATED WITH MOJANG.

KEIN OFFIZIELLES MINECRAFT PRODUKT.
NICHT VON MOJANG GENEHMIGT ODER MIT MOJANG
ASSOZIIERT.
