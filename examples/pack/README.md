# `pack` directory

This directory is a Minecraft behaviour pack which can be used to test
structures.

## Usage

Update new structures with the following two commands.

```bash
rm -rf src/structures/*.mcstructure  # Remove old structures
cp ../structures/*.mcstructure src/structures  # Add new structures
./makepack.py  # Build the pack
```

## TODO

* use Makefile
* version will never change, remove it from the build
