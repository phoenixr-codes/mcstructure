# `pack` directory

This directory is a Minecraft behaviour pack which can be used to test
structures.

```text
pack
├── README.md          # This file
├── build/             # Built behaviour pack
├── makepack.py        # Builds the pack
└── src/               # Content of the pack
    ├── manifest.json
    └── structures
```

## Usage

Update new structures with the following three commands.

```bash
mkdir -p build # Create output directory if not present yet
rm -rf src/structures/*.mcstructure  # Remove old structures
cp ../structures/*.mcstructure src/structures  # Add new structures
./makepack.py  # Build the pack
```

## TODO

* use Makefile
* version will never change, remove it from the build
