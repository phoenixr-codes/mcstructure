"""
Read and write Minecraft ``.mcstructure`` files.
"""

# TODO: support additional block data

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from functools import partial
from itertools import repeat
from typing import Any, BinaryIO, Tuple, Self, cast

import numpy as np
from numpy.typing import NDArray
import nbtx


Coordinate = Tuple[int, int, int]
BlockStateValue = str | bool | int


COMPABILITY_VERSION: int = 17959425
"""
The compability version for a block. The four bytes making up this
integer determine the game version number. For example, ``17879555`` is
``01 10 D2 03`` in hex meaning ``1.16.210.03``.
"""

STRUCTURE_MAX_SIZE: tuple[int, int, int] = (64, 384, 64)
"""
The maximum size a structure can have. This does not apply for
structures created externally and thus is not affect structures
created with this library.
"""


def is_valid_structure_name(name: str, *, with_prefix: bool = False) -> bool:
    """
    Validates the structure name.

    .. seealso: https://minecraft.fandom.com/wiki/Structure_Block

    Parameters
    ----------
    name
        The name of the structure.

    with_prefix
        Whether to take the prefix (e.g. ``mystructure:``)
        into account.
    """
    if with_prefix:
        name = name.replace(":", "", 1)

    return all((char.isalnum() and char in "-_") for char in name)


def has_suitable_size(size: tuple[int, int, int]) -> bool:
    """
    Returns ``False`` if ``size`` is greater than the size of
    structures that can be created within Minecraft.

    .. seealso:: :const:`STRUCTURE_MAX_SIZE`
    """
    return all(map(lambda n: n[0] <= n[1], zip(size, STRUCTURE_MAX_SIZE)))


@dataclass(init=False, slots=True)
class Block:
    """
    Attributes
    ----------
    name
        The name of the block.

    states
        The states of the block.

    Examples
    --------
    .. code-block::

        Block("minecraft:beehive", honey_level=4)
        Block("minecraft:grass")

    """

    identifier: str
    states: dict[str, BlockStateValue]
    waterlogged: bool = field(kw_only=True, default=False)

    def __init__(self, identifier: str, *, waterlogged: bool = False, **states: BlockStateValue):
        """
        Parameters
        ----------
        identifier
            The identifier of the block (e.g. "minecraft:wool").

        states
            The block states such as ``color`` or ``stone_type``.
            This varies by every block.

            .. seealso:: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockstateslist

        waterlogged
            Whether this block is waterlogged.
        """
        self.identifier = identifier
        self.states = states
        self.waterlogged = waterlogged

    def __str__(self) -> str:
        return self.stringify()

    def stringify(
        self,
        *,
        with_namespace: bool = True,
        with_states: bool = True,
    ) -> str:
        """Returns a human-readable representation of the block.

        This format matches the one used for commands like `setblock`.

        Parameters
        ----------
        with_namespace
            Whether to include the block's namespace.

        with_states
            Whether to include the block's states.
        """
        result = ""
        if with_namespace and (ns := self.namespace) is not None:
            result += ns + ":"
        result += self.name
        if with_states:
            result += " ["
            for key, value in self.states.items():
                result += f'"{key}"='
                if isinstance(value, str):
                    result += f'"{value}"'
                elif isinstance(value, bool):
                    result += str(value).lower()
                elif isinstance(value, int):
                    result += str(value)
                else:
                    raise ValueError("block state value must be str, bool or int")
            result += "]"
        return result

    @property
    def namespace_and_name(self) -> tuple[str | None, str]:
        """The namespace and the name of the block.

        Examples
        --------
        .. code-block:: python

            >>> from mcstructure import Block
            >>>
            >>> block = Block("minecraft:wool", color="red")
            >>> block.namespace_and_name
            ("minecraft", "wool")
            >>>
            >>> block = Block("foobar")
            >>> block.namespace_and_name
            (None, "foobar")

        """
        if ":" in self.identifier:
            ns, name = self.identifier.split(":", 1)
            return ns, name

        return (None, self.identifier)

    @property
    def name(self) -> str:
        """The name of the block.

        Examples
        --------
        .. code-block:: python

                >>> from mcstructure import Block
                >>>
                >>> block = Block("minecraft:wool", color="red")
                >>> block.name
                "wool"
                >>>
                >>> block = Block("foobar")
                >>> block.name
                "foobar"

        """
        return self.namespace_and_name[1]

    @property
    def namespace(self) -> str | None:
        """The namespace of the block.

        Examples
        --------
        .. code-block:: python

                >>> from mcstructure import Block
                >>>
                >>> block = Block("minecraft:wool", color="red")
                >>> block.namespace
                "minecraft"
                >>>
                >>> block = Block("foobar")
                >>> (block.namespace,)
                (None,)

        """
        return self.namespace_and_name[0]

_WATER = Block("minecraft:water", liquid_depth=0)

class Structure:
    """Class representing a Minecraft structure that consists of blocks and entities.

    Attributes
    ----------
    structure
        The numpy array representing the blocks in the structure. Each entry is an ID
        associated with a block present in :meth:`palette`.

    entities
        A list of entities the structure contains.

    _size
        Size of the structure stored internally.

    _palette
        Internal list of blocks that are used within the structure. The position of
        the block in the list represents its ID. Modification of this list should be
        done with caution and if you do so consider modifying :attr:`structure`
        appropriately. Instead use methods like :meth:`set_block`.
    """

    def __init__(
        self,
        size: tuple[int, int, int],
        fill: Block | None = Block("minecraft:air"),
    ) -> None:
        """
        Parameters
        ----------
        size
            The size of the structure.

        fill
            Fill the structure with this block at
            creation of a new structure object.

            If this is set to ``None`` the structure
            is filled with "Structure Void" blocks.

            ``'minecraft:air'`` is used as default.
        """
        self.structure: NDArray[np.intc]
        self.entities: list[nbtx.Tag[Any, Any]] = []

        self._size = size
        self._palette: list[Block] = []

        if fill is None:
            self.structure = np.full(size, -1, dtype=np.intc)

        else:
            self.structure = np.zeros(size, dtype=np.intc)
            self._palette.append(fill)

    @classmethod
    def load(cls, file: BinaryIO) -> Self:
        """
        Loads a structure from a file.

        Examples
        --------
        .. code-block:: python

            from mcstructure import Structure

            with open("house.mcstructure", "rb") as f:
                struct = Structure.load(f)

        Parameters
        ----------
        file
            File object to read.
        """
        nbt_root = nbtx.load(file, endianness="little")
        assert isinstance(nbt_root, nbtx.TagCompound)
        nbt_body = nbt_root.as_python()
        size: tuple[int, int, int] = tuple(nbt_body["size"])

        struct = cls(size, None)

        struct.structure = np.array(
            [x for x in nbt_body["structure"]["block_indices"][0]],
            dtype=np.intc,
        ).reshape(size)

        struct.entities = nbt_body["structure"]["entities"]

        waterlogged_mask: list[bool] = [value != -1 for value in nbt_body["structure"]["block_indices"][1]]

        struct._palette.extend(
            [
                Block(block["name"], **(block["states"]), waterlogged=waterlogged_mask[index])
                for (index, block) in enumerate(nbt_body["structure"]["palette"]["default"][
                    "block_palette"
                ])
            ]
        )

        return struct

    @property
    def size(self) -> tuple[int, int, int]:
        """The size of the structure."""
        return self._size

    @property
    def palette(self) -> list[Block]:
        """A copy of the palette."""
        palette = self._palette.copy()
        return palette

    def __repr__(self) -> str:
        return repr(self._get_str_array())

    def __str__(self) -> str:
        return str(self._get_str_array())

    def _get_str_array(
        self, *, with_namespace: bool = False, with_states: bool = False
    ) -> NDArray[Any]:
        """
        Returns a numpy array where each entry is a
        readable string of the corresponding block.

        Parameters
        ----------
        with_namespace
            Adds the namespace to the string if present.

        with_states
            Adds the block states to the string if present.
        """
        arr = self.get_structure().copy()
        vec = np.vectorize(
            partial(
                Block.stringify, with_namespace=with_namespace, with_states=with_states
            )
        )
        return cast(NDArray[Any], vec(arr))

    def _add_block_to_palette(self, block: Block | None) -> int:
        """
        Adds a block to the palette.

        Parameters
        ----------
        block
            The block to add. If this is set to ``None``
            "Structure Void" will be used.

        Returns
        -------
        The position of the block in the palette. This is
        ``-1`` when ``None`` is used as ``block``.
        """
        if block is None:
            return -1

        if block in self._palette:
            return self._palette.index(block)

        self._palette.append(block)
        return len(self._palette) - 1

    def _water_index(self) -> int:
        """
        Returns the index of water with liquid depth 0.

        If water is not present in the palette, then water will be added to the
        palette.
        """
        for (index, block) in enumerate(self._palette):
            if block == _WATER:
                return index
        return self._add_block_to_palette(_WATER)

    def get_structure(self) -> NDArray[Any]:
        """
        Returns the structure as a numpy array filled
        with the corresponding block objects.
        """
        arr = np.full(
            self.structure.shape, Block("minecraft:structure_void"), dtype=object
        )
        for key, block in enumerate(self._palette):
            arr[self.structure == key] = block
        return arr

    def as_nbt(self) -> nbtx.TagCompound[Any, Any]:
        """
        Serialize the structure as a NBT data.

        Examples
        --------
        .. code-block:: python

            from mcstructure import Structure

            struct = Structure((5, 5, 5), None)
            nbt = struct.as_nbt()
            print(nbt.pretty())
        """
        return nbtx.TagCompound[Any, Any](
            name="",
            value=[
                nbtx.TagInt(name="format_version", value=1),
                nbtx.TagList(
                    name="size",
                    child_id=nbtx.TagInt.id(),
                    value=[
                        nbtx.TagInt("", self._size[0]),
                        nbtx.TagInt("", self._size[1]),
                        nbtx.TagInt("", self._size[2]),
                    ],
                ),
                nbtx.TagCompound(
                    name="structure",
                    value=[
                        nbtx.TagList(
                            name="block_indices",
                            child_id=nbtx.TagList.id(),
                            value=[
                                nbtx.TagList(
                                    name="",
                                    child_id=nbtx.TagInt.id(),
                                    value=[
                                        nbtx.TagInt("", i.item())
                                        for i in self.structure.flatten()
                                    ],
                                ),
                                nbtx.TagList(
                                    name="",
                                    child_id=nbtx.TagInt.id(),
                                    value=[
                                        nbtx.TagInt(
                                            "",
                                            self._water_index() if self._palette[i.item()].waterlogged else -1
                                        )
                                        for i in self.structure.flatten()
                                    ],
                                ),
                            ],
                        ),
                        nbtx.TagList(
                            name="entities",
                            child_id=nbtx.TagCompound.id(),
                            value=self.entities,
                        ),
                        nbtx.TagCompound(
                            name="palette",
                            value=[
                                nbtx.TagCompound(
                                    name="default",
                                    value=[
                                        nbtx.TagList(
                                            name="block_palette",
                                            child_id=nbtx.TagCompound.id(),
                                            value=[
                                                nbtx.TagCompound(
                                                    name="",
                                                    value=[
                                                        nbtx.TagString(
                                                            name="name",
                                                            value=block.identifier,
                                                        ),
                                                        nbtx.TagCompound(
                                                            name="states",
                                                            value=[
                                                                (
                                                                    nbtx.TagInt(
                                                                        state_name,
                                                                        state_value,
                                                                    )
                                                                    if isinstance(
                                                                        state_value, int
                                                                    )
                                                                    else (
                                                                        nbtx.TagString(
                                                                            state_name,
                                                                            state_value,
                                                                        )
                                                                        if isinstance(
                                                                            state_value,
                                                                            str,
                                                                        )
                                                                        else nbtx.TagByte(
                                                                            state_name,
                                                                            state_value,
                                                                        )
                                                                    )
                                                                )
                                                                for state_name, state_value in block.states.items()
                                                            ],
                                                        ),
                                                        nbtx.TagInt(
                                                            name="version",
                                                            value=COMPABILITY_VERSION,
                                                        ),
                                                    ],
                                                )
                                                for block in self._palette
                                            ],
                                        ),
                                        nbtx.TagCompound(
                                            name="block_position_data", value=[]
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
                nbtx.TagList(
                    name="structure_world_origin",
                    value=[
                        nbtx.TagInt(name="", value=0),
                        nbtx.TagInt(name="", value=0),
                        nbtx.TagInt(name="", value=0),
                    ],
                    child_id=nbtx.TagInt.id(),
                ),
            ],
        )

    def dump(self, file: BinaryIO) -> None:
        """
        Serialize the structure as a NBT file.

        Examples
        --------
        .. code-block:: python

            from mcstructure import Structure

            struct = Structure((5, 5, 5), None)
            with open("house.mcstructure", "wb") as f:
                struct.dump(f)

        Parameters
        ----------
        file
            File object to write to.
        """
        nbt = self.as_nbt()
        nbtx.dump(nbt, file, endianness="little")

    def get_block(self, coordinate: Coordinate) -> Block | None:
        """
        Returns the block in a specific position.

        Parameters
        ----------
        coordinate
            The coordinte of the block.
        """
        x, y, z = coordinate
        return (
            self._palette[self.structure[x, y, z]]
            if self.structure[x, y, z] >= 0
            else Block("minecraft:structure_void")
        )

    def add_entity(self, nbt_data: nbtx.Tag[Any, Any]) -> Self:
        """
        Adds an entity to the structure.

        Parameters
        ----------
        nbt_data
            The NBT data of the entity to add.
            The best approach would be to export a structure from the game,
            display the NBT data and use that as a reference.
        """
        self.entities.append(nbt_data)
        return self

    def set_block(
        self,
        coordinate: Coordinate,
        block: Block | None,
    ) -> Self:
        """
        Places a block in the structure.

        Parameters
        ----------
        coordinate
            Relative coordinates of the block's position.

        block
            The block to place. If this is set to ``None``
            "Structure Void" blocks will be used.
        """
        x, y, z = coordinate

        ident = self._add_block_to_palette(block)

        self.structure[x, y, z] = ident
        return self

    def set_blocks(
        self,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        block: Block,
    ) -> Self:
        """
        Fills an area in the structure with blocks.

        Notes
        -----
        Both start and end points are included.

        Parameters
        ----------
        from_coordinate
            Relative coordinates of the start edge.

        to_coordinate
            Relative coordinates of the end edge.

        block
            The block to place. If this is set to ``None``
            "Structure Void" blocks will be used to fill.
        """
        fx, fy, fz = from_coordinate
        tx, ty, tz = to_coordinate

        ident = self._add_block_to_palette(block)
        self.structure[fx : tx + 1, fy : ty + 1, fz : tz + 1] = np.array(
            [
                [
                    [ident for k in range(abs(fz - tz) + 1)]
                    for j in range(abs(fy - ty) + 1)
                ]
                for i in range(abs(fx - tx) + 1)
            ],
            dtype=np.intc,
        ).reshape([abs(i) + 1 for i in (fx - tx, fy - ty, fz - tz)])
        return self

    def resize(
        self, size: tuple[int, int, int], fill: Block | None = Block("minecraft:air")
    ) -> Self:
        """
        Resizes the structure.

        This function erases blocks that are out of bounds and fill newly
        created space with ``fill`` (default is air).

        Parameters
        ----------
        size
            The new size of the structure.

        fill
            The block to fill newly created space with. If this is set to
            ``None`` (default) then "Structure Void" blocks will be used.
        """
        ident = self._add_block_to_palette(fill)
        self._size = size

        if self.structure.shape == size:
            # No need to resize
            return self

        # Create new structure filled with the fill block identifier
        if fill is not None:
            new_structure = np.full(size, ident, dtype=np.intc)
        else:
            new_structure = np.full(size, -1, dtype=np.intc)  # Fill Structure void

        # Calculate the overlap region (what we can copy from old to new)
        old_size = self.structure.shape
        copy_size = tuple(min(old_size[i], size[i]) for i in range(3))

        # Copy the existing Blocks that fits into the new size
        if all(s > 0 for s in copy_size):
            new_structure[: copy_size[0], : copy_size[1], : copy_size[2]] = (
                self.structure[: copy_size[0], : copy_size[1], : copy_size[2]]
            )

        self.structure = new_structure
        return self

    def combine(self, other: Structure, position: Coordinate = (0, 0, 0)) -> Structure:
        """
        Combines another structure into this structure.

        Parameters
        ----------
        other
            The other structure to combine with.

        position
            The position to place the other structure at.

            note: This position is relative to the
            current structure's origin. ( no negative coordinates allowed )

        Returns
        -------
        Structure
            The combined structure.
        """

        ox, oy, oz = position

        if ox < 0 or oy < 0 or oz < 0:
            raise ValueError("Negative coordinates are not allowed.")

        # Calculate the new size needed to accommodate both structures
        end_pos = (ox + other._size[0], oy + other._size[1], oz + other._size[2])
        new_size = (
            max(self._size[0], end_pos[0]),
            max(self._size[1], end_pos[1]),
            max(self._size[2], end_pos[2]),
        )

        combined = Structure(new_size, None)

        # Copy the current structure's palette
        combined._palette = self._palette.copy()

        # Copy the current structure
        combined.structure[: self._size[0], : self._size[1], : self._size[2]] = (
            self.structure
        )

        # Create mapping from other's palette indices to combined palette indices
        other_to_combined_mapping = {
            other_idx: combined._add_block_to_palette(block)
            for other_idx, block in enumerate(other._palette)
        }

        # Remap the entire other structure using vectorized operations
        remapped_structure = other.structure.copy()

        # For non-structure-void blocks, apply the palette mapping
        for other_idx, combined_idx in other_to_combined_mapping.items():
            block_mask = other.structure == other_idx
            remapped_structure[block_mask] = combined_idx

        # Overlay the remapped structure onto the combined structure
        combined.structure[ox:, oy:, oz:] = remapped_structure[:, :, :]

        return combined
