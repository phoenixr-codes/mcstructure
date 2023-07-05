#!/usr/bin/env python3

# copied from https://github.com/phoenixr-codes/transparent-pumpkin/blob/main/build.py

import json
import pathlib
import zipfile

NAME = "mcstructure-python"

src = pathlib.Path("src")

with (src / "manifest.json").open("r") as f:
    data = json.load(f)
    version = ".".join(map(str, data["header"]["version"]))

print(f"building v{version} ...")

with zipfile.ZipFile(f"build/{NAME}-v{version}.mcpack", "w") as archive:
    for path in src.rglob("*"):
        archive.write(path, arcname=path.relative_to(src))
